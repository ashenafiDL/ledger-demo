from rest_framework import serializers

from .models.attachment import Attachment, LedgerDoumentAttachment
from .models.carrier import Carrier
from .models.delivery import Delivery
from .models.document import Document
from .models.ledger import Ledger
from .models.metadata import Metadata
from .models.recipient import Recipient
from .models.sender import Sender


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ["file", "description"]


class LedgerDocumentAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LedgerDoumentAttachment
        fields = ["file", "description"]


class CarrierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrier
        fields = "__all__"


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = "__all__"


class DocumentSerializer(serializers.ModelSerializer):
    attachment = AttachmentSerializer(read_only=True, many=True)
    letter = LedgerDocumentAttachmentSerializer(read_only=True, many=True)

    class Meta:
        model = Document
        fields = [
            "ledger",
            "document_owner",
            "additional_message",
            "letter",
            "attachment",
            "document_type",
            "document_type",
        ]


class MetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metadata
        fields = "__all__"


class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = "__all__"


class LedgerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ledger
        fields = "__all__"


class SenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sender
        fields = "__all__"


class LedgerDetailSerializer(serializers.ModelSerializer):
    metadatas = MetadataSerializer()
    carrier = CarrierSerializer(read_only=True)
    delivery = DeliverySerializer(read_only=True)
    recipient = RecipientSerializer(read_only=True)
    document = DocumentSerializer(read_only=True)
    sender = SenderSerializer(read_only=True)

    class Meta:
        model = Ledger
        fields = [
            "id",
            "ledger_subject",
            "ledger_description",
            "ledger_type",
            "received_at",
            "status",
            "priority",
            "metadatas",
            "carrier",
            "delivery",
            "recipient",
            "document",
            "sender",
            "ledger_pdf",
        ]


class DocumentSerializer(serializers.ModelSerializer):
    attachments = serializers.ListField(
        child=serializers.FileField(),
        required=False,
        write_only=True,
    )
    letters = serializers.ListField(
        child=serializers.FileField(),
        required=False,
        write_only=True,
    )

    class Meta:
        model = Document
        fields = "__all__"


class LedgerSerializer(serializers.Serializer):
    ledger_description = serializers.CharField(required=False)
    ledger_subject = serializers.CharField(required=False)
    ledger_type = serializers.ChoiceField(choices=["INCOMING", "OUTGOING", "PERSONAL"], required=False)
    received_at = serializers.DateTimeField()
    approved_at = serializers.DateTimeField(required=False)
    approved_by = serializers.CharField(required=False)  # user ID
    status = serializers.ChoiceField(choices=["PENDING", "APPROVED", "REJECTED", "COMPLETED"], default="PENDING")
    reference_number = serializers.CharField(required=False)
    deadline = serializers.CharField(required=False)
    category = serializers.CharField(required=False)
    priority = serializers.ChoiceField(choices=["HIGH", "MEDIUM", "LOW"], required=False)
    tracking_number = serializers.CharField(required=False, allow_blank=True)


class LedgerNewSerializer(serializers.Serializer):
    carrier_person_first_name = serializers.CharField()
    carrier_person_middle_name = serializers.CharField()
    carrier_person_last_name = serializers.CharField()
    carrier_phone_number = serializers.CharField()
    carrier_type = serializers.CharField()
    carrier_organization_id = serializers.CharField(required=False, allow_blank=True)
    carrier_plate_number = serializers.CharField(required=False, allow_blank=True)
    letters = serializers.ListField(child=serializers.FileField())
    attachments = serializers.ListField(child=serializers.FileField(), required=False)
    additional_message = serializers.CharField(required=False, allow_blank=True)
    document_type = serializers.CharField(required=False, allow_blank=True)
    document_date = serializers.DateTimeField(required=False)
    document_owner = serializers.CharField(required=False, allow_blank=True)
    ledger_subject = serializers.CharField(required=False, allow_blank=True)
    ledger_description = serializers.CharField(required=False, allow_blank=True)
    ledger_type = serializers.CharField(required=False, allow_blank=True)
    delivery_medium = serializers.CharField(required=False, allow_blank=True)
    delivery_channel = serializers.CharField(required=False, allow_blank=True)
    delivery_organization = serializers.CharField(required=False, allow_blank=True)
    tracking_number = serializers.CharField(required=False, allow_blank=True)
    expected_delivery_date = serializers.DateTimeField(required=False)
    delivery_status = serializers.CharField(required=False, allow_blank=True)

    metadata_title = serializers.CharField(required=False, allow_blank=True)
    metadata_description = serializers.CharField(required=False, allow_blank=True)
    metadata_author = serializers.CharField(required=False, allow_blank=True)
    metadata_date_created = serializers.DateTimeField(required=False)
    metadata_last_modified = serializers.DateTimeField(required=False)
    metadata_version = serializers.CharField(required=False, allow_blank=True)
    metadata_keywords = serializers.CharField(required=False, allow_blank=True)
    metadata_tags = serializers.CharField(required=False, allow_blank=True)
    metadata_category = serializers.CharField(required=False, allow_blank=True)
    metadata_file_type = serializers.CharField(required=False, allow_blank=True)
    metadata_language = serializers.CharField(required=False, allow_blank=True)
    metadata_status = serializers.CharField(required=False, allow_blank=True)
    metadata_confidentiality = serializers.CharField(required=False, allow_blank=True)
    metadata_source_system = serializers.CharField(required=False, allow_blank=True)

    recipient_name = serializers.CharField(required=False, allow_blank=True)
    recipient_phone_number = serializers.CharField(required=False, allow_blank=True)
    job_title = serializers.CharField(required=False, allow_blank=True)
    department = serializers.CharField(required=False, allow_blank=True)
    sector = serializers.CharField(required=False, allow_blank=True)
    received_at = serializers.DateTimeField(required=False)
    status = serializers.CharField(required=False, allow_blank=True)
    reference_number = serializers.CharField(required=False, allow_blank=True)
    external_reference_id = serializers.CharField(required=False, allow_blank=True)
    priority = serializers.CharField(required=False, allow_blank=True)
    approved_by = serializers.CharField(required=False, allow_blank=True)
    approved_at = serializers.DateTimeField(required=False)
    deadline = serializers.DateTimeField(required=False)
    category = serializers.CharField(required=False, allow_blank=True)
    sender_name = serializers.CharField(required=False, allow_blank=True)
    sender_phone_number = serializers.CharField(required=False, allow_blank=True)
    sender_email = serializers.CharField(required=False, allow_blank=True)
    sender_address = serializers.CharField(required=False, allow_blank=True)
    sender_type = serializers.CharField(required=False, allow_blank=True)
