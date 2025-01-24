import os
from datetime import datetime

from django.core.files.storage import default_storage
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ApiAuthMixin

from .models.ledger import Ledger
from .selectors import ledger_details
from .serializers import (
    CarrierSerializer,
    DeliverySerializer,
    DocumentSerializer,
    LedgerDetailSerializer,
    LedgerListSerializer,
    LedgerNewSerializer,
    LedgerSerializer,
    LedgerSharingSerializer,
    MetadataSerializer,
    RecipientSerializer,
)
from .services import (
    create_carrier,
    create_delivery,
    create_document_with_attachments_and_letters,
    create_ledger,
    create_ledger_entry,
    create_metadata,
    create_recipient,
    share_ledger,
)
from .tasks import generate_ledger_pdf


class LedgerCreate(ApiAuthMixin, APIView):
    def post(self, request):
        serializer = LedgerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ledger = create_ledger_entry(**serializer.validated_data)

        return Response(
            {"message": "Ledger created successfully", "ledger_id": ledger.id},
            status=status.HTTP_201_CREATED,
        )


class CarrierCreateAPIView(ApiAuthMixin, APIView):
    def post(self, request, *args, **kwargs):
        serializer = CarrierSerializer(data=request.data)
        if serializer.is_valid():
            try:
                carrier = create_carrier(**serializer.validated_data)
                return Response(CarrierSerializer(carrier).data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipientCreateAPIView(ApiAuthMixin, APIView):
    def post(self, request, *args, **kwargs):
        serializer = RecipientSerializer(data=request.data)

        if serializer.is_valid():
            try:
                create_recipient(**serializer.validated_data)

                return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocumentCreateAPIView(ApiAuthMixin, APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        attachments = [file for key, file in request.FILES.items() if key.startswith("attachments")]
        letters = [file for key, file in request.FILES.items() if key.startswith("letters")]

        data = request.data.copy()

        document_date = datetime.fromisoformat(data["document_date"])

        try:
            document = create_document_with_attachments_and_letters(
                ledger=data["ledger"],
                document_type=data["document_type"],
                document_date=document_date,
                document_owner=data["document_owner"],
                additional_message=data.get("additional_message", ""),
                attachments_data=attachments,
                letters_data=letters,
                current_user=request.user,
            )
            return Response(DocumentSerializer(document).data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MetadataCreateAPIView(ApiAuthMixin, APIView):
    def post(self, request, *args, **kwargs):
        serializer = MetadataSerializer(data=request.data)
        if serializer.is_valid():
            try:
                metadata = create_metadata(**serializer.validated_data)
                return Response(MetadataSerializer(metadata).data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeliveryCreateAPIView(ApiAuthMixin, APIView):
    def post(self, request, *args, **kwargs):
        serializer = DeliverySerializer(data=request.data)
        if serializer.is_valid():
            try:
                delivery = create_delivery(**serializer.validated_data)
                return Response(DeliverySerializer(delivery).data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LedgerNewAPIView(ApiAuthMixin, APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = LedgerNewSerializer

    def post(self, request, *args, **kwargs):
        serializer = LedgerNewSerializer(data=request.data)
        try:
            serializer.is_valid()
            ledger = create_ledger(
                current_user=request.user,
                **serializer.validated_data,
            )
            generate_ledger_pdf.delay_on_commit(ledger_id=ledger.id)
            return Response(
                {"id": ledger.id, "message": "Ledger created successfully."},
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "An unexpected error occurred.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LedgerPdfDownloadAPIView(ApiAuthMixin, APIView):
    def get(self, request, ledger_id):
        ledger = get_object_or_404(Ledger, id=ledger_id)
        pdf_path = ledger.ledger_pdf
        try:
            if not pdf_path:
                return Response({"error": "PDF file not found."}, status=status.HTTP_404_NOT_FOUND)
            file = default_storage.open(pdf_path, "rb")
            return FileResponse(file, as_attachment=True, filename=os.path.basename(pdf_path))
        except FileNotFoundError:
            return Response({"error": "PDF file not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LedgerListApi(ApiAuthMixin, APIView):
    required_object_perms = ["can_view_letter", "can_submit_letter"]

    serializer_class = LedgerListSerializer

    def get(self, request) -> Response:
        ledgers = Ledger.objects.all()
        output_serializer = LedgerListSerializer(ledgers, many=True)

        try:
            response_data = {"ledgers": output_serializer.data}

            return Response(data=response_data, status=status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class LedgerDetailAPIView(ApiAuthMixin, APIView):
    serializer_class = LedgerDetailSerializer

    def get(self, request, ledger_id) -> Response:
        try:
            ledger = ledger_details(ledger_id=ledger_id)
            serializer = LedgerDetailSerializer(ledger)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ShareLedgerAPIView(ApiAuthMixin, APIView):
    serializer_class = LedgerSharingSerializer

    def post(self, request, *args, **kwargs):
        ledger_id = request.data.get("ledger")
        shared_to_id = request.data.get("shared_to")

        try:
            sharing_instance = share_ledger(
                ledger_id=ledger_id,
                shared_to_id=shared_to_id,
            )

            serializer = LedgerSharingSerializer(sharing_instance)

            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
