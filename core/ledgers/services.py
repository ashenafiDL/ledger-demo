from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction

from core.departments.models import Department, JobTitle
from .models import Ledger, Attachment, LedgerDoumentAttachment, LedgerSharing
from core.users.models import Member


def create_attachment(file_data, current_user, model_class):
    file = file_data.get("file")
    description = file_data.get("description", "")

    if isinstance(file, InMemoryUploadedFile):
        return model_class.objects.create(
            file=file,
            file_name=file.name,
            file_type=file.content_type,
            file_size=file.size,
            description=description,
            uploaded_by=current_user,
        )
    return None


@transaction.atomic
def create_ledger(
    current_user: Member,
    carrier_person_first_name: str = None,
    carrier_person_middle_name: str = None,
    carrier_phone_number: str = None,
    written_at: str = None,
    ledger_subject: str = None,
    ledger_status: str = Ledger.LedgerStatus.PENDING,
    recipient_name: str = None,
    recipient_phone_number: str = None,
    job_title: str = None,
    department: str = None,
    priority: str = None,
    metadata_keywords: str = None,
    metadata_tags: str = None,
    metadata_file_type: str = None,
    metadata_confidentiality: str = Ledger.MetadataConfidenciaity.INTERNAL,
    tracking_number: str = None,
    letter=None,
    attachment=None,
    sender_name: str = None,
    sender_phone_number: str = None,
    sender_email: str = None,
):
    try:
        recipient_department = Department.objects.get(id=department)
    except Department.DoesNotExist:
        raise ValueError(f"Department with id '{department}' does not exist.")

    try:
        recipient_job_title = JobTitle.objects.get(id=job_title)
    except JobTitle.DoesNotExist:
        raise ValueError(f"Job title with id '{job_title}' does not exist.")

    if letter is None:
        raise ValueError("letter is required!")

    ledger = Ledger.objects.create(
        sender_name=sender_name,
        sender_phone_number=sender_phone_number,
        sender_email=sender_email,
        carrier_person_first_name=carrier_person_first_name,
        carrier_person_middle_name=carrier_person_middle_name,
        carrier_phone_number=carrier_phone_number,
        ledger_subject=ledger_subject,
        written_at=written_at,
        ledger_status=ledger_status,
        recipient_name=recipient_name,
        recipient_phone_number=recipient_phone_number,
        job_title=recipient_job_title,
        department=recipient_department,
        priority=priority,
        metadata_keywords=metadata_keywords,
        metadata_tags=metadata_tags,
        metadata_fileType=metadata_file_type,
        metadata_confidentiality=metadata_confidentiality,
        tracking_number=tracking_number,
    )

    if attachment:
        for attachment_file in attachment:
            attachment = create_attachment(
                file_data={"file": attachment_file},
                current_user=current_user,
                model_class=Attachment,
            )
            if attachment:
                ledger.attachment.add(attachment)

    for letter_file in letter:
        letter_attachment = create_attachment(
            file_data={"file": letter_file},
            current_user=current_user,
            model_class=LedgerDoumentAttachment,
        )
        if letter_attachment:
            ledger.letter.add(letter_attachment)

    return ledger


def share_ledger(ledger_id: str, shared_to: Member, shared_by_id: str) -> LedgerSharing:
    ledger = Ledger.objects.get(id=ledger_id)
    shared_by = Member.objects.get(id=shared_by_id)

    sharing_instance = LedgerSharing.objects.create(
        ledger=ledger,
        shared_to=shared_to,
        shared_by=shared_by
    )

    sharing_instance.full_clean()

    sharing_instance.save()

    return sharing_instance
