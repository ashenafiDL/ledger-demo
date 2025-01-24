from rest_framework import serializers
from .models import Attachment, LedgerDoumentAttachment, Ledger, LedgerSharing


class AttachmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attachment
        fields = (
            "id",
            "file",
            "file_name",
            "file_type",
            "file_size",
            "description",
            "uploaded_at",
        )


class LedgerDoumentAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LedgerDoumentAttachment
        fields = (
            "id",
            "file",
            "file_name",
            "file_type",
            "file_size",
            "description",
            "uploaded_at",
        )


class LedgerDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ledger
        fields = '__all__'


class LedgerNewSerializer(serializers.Serializer):
    letter = LedgerDoumentAttachmentSerializer(many=True)
    attachment = AttachmentSerializer(many=True, required=False)
    sender_name = serializers.CharField()
    sender_phone_number = serializers.CharField()
    sender_email = serializers.CharField()
    carrier_person_first_name= serializers.CharField(required=False)
    carrier_person_middle_name= serializers.CharField(required=False)
    ledger_subject = serializers.CharField(required=False)
    carrier_phone_number= serializers.CharField(required=False)
    recipient_name = serializers.CharField( required=False)
    recipient_phone_number = serializers.CharField( required=False)
    job_title = serializers.CharField()
    department = serializers.CharField()
    written_at = serializers.CharField()
    ledger_status = serializers.CharField( required=False)
    priority = serializers.CharField( required=False)
    metadata_keywords = serializers.CharField( required=False)
    metadata_tags = serializers.CharField( required=False)
    metadata_fileType = serializers.CharField( required=False)
    metadata_confidentiality = serializers.CharField(required=False)
    tracking_number = serializers.CharField(required=False)


class LedgerListSerializer(serializers.Serializer):
    sender_name = serializers.CharField()
    sender_email = serializers.CharField()
    recipient_name = serializers.CharField( required=False)
    job_title = serializers.CharField()
    department = serializers.CharField()
    metadata_keywords = serializers.CharField( required=False)
    metadata_tags = serializers.CharField( required=False)
    priority = serializers.CharField( required=False)
    tracking_number = serializers.CharField(required=False)
    ledger_status = serializers.CharField( required=False)
    written_at = serializers.CharField()
    metadata_confidentiality = serializers.CharField(required=False)


class LedgerSharingSerializer(serializers.ModelSerializer):
    ledger = LedgerDetailSerializer()

    class Meta:
        model = LedgerSharing
        fields = ["ledger", "shared_to", "shared_at"]
        read_only_fields = ["shared_at"]
