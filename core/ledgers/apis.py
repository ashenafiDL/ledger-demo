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
from .models import LedgerSharing

from .models import Ledger
from .selectors import ledger_details
from .serializers import (

    LedgerDetailSerializer,
    LedgerListSerializer,
    LedgerNewSerializer,
    LedgerSharingSerializer,
)
from .services import (
    share_ledger,
    create_ledger,
)
from .tasks import generate_ledger_pdf


class LedgerNewAPIView(ApiAuthMixin, APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = LedgerNewSerializer

    def post(self, request, *args, **kwargs):
        serializer = LedgerNewSerializer(data=request.data)
        try:
            serializer.is_valid()
            attachments = [file for key, file in request.FILES.items() if key.startswith("attachment")]
            letters = [file for key, file in request.FILES.items() if key.startswith("letter")]
            ledger = create_ledger(
                current_user=request.user,
                attachment=attachments,
                letter=letters,
                **serializer.validated_data,
            )
            # generate_ledger_pdf.delay(ledger_id=ledger.id)
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
        shared_by_id = request.user.id

        try:
            sharing_instance = share_ledger(
                ledger_id=ledger_id,
                shared_to_id=shared_to_id,
                shared_by_id=shared_by_id
            )

            serializer = LedgerSharingSerializer(sharing_instance)

            return Response(
                {"id": sharing_instance.id, "message": "Ledger shared successfully."},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class SharedLedgersAPIView(ApiAuthMixin, APIView):
    serializer_class = LedgerSharingSerializer

    def get(self, request) -> Response:
        try:
            user_id = request.user.id

            shared_ledgers = LedgerSharing.objects.filter(shared_to=user_id).select_related("ledger")
            serializer = LedgerSharingSerializer(shared_ledgers, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
