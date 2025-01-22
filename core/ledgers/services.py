from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction

from core.departments.models import Department, JobTitle
from core.users.models.user import User

from .models.attachment import Attachment, LedgerDoumentAttachment
from .models.carrier import Carrier
from .models.delivery import Delivery
from .models.document import Document
from .models.ledger import Ledger
from .models.metadata import Metadata
from .models.recipient import Recipient
from .models.sender import Sender


@transaction.atomic
def create_ledger(
    current_user: User,
    carrier_person_first_name: str,
    carrier_person_last_name: str,
    carrier_phone_number: str,
    carrier_type: str,
    delivery_channel: str,
    delivery_medium: str,
    received_at: str = None,
    ledger_subject: str = None,
    ledger_description: str = None,
    status: str = "PENDING",
    ledger_type: str = "INCOMING",
    recipient_phone_number: str = None,
    recipient_name: str = None,
    department: str = None,
    job_title: str = None,
    document_type: str = None,
    document_owner: str = None,
    document_date: str = None,
    expected_delivery_date: str = None,
    metadata_title: str = None,
    metadata_date_created: str = None,
    letters=None,
    attachments=None,
    carrier_person_middle_name: str = None,
    additional_message: str = None,
    carrier_organization_id: str = None,
    delivery_organization: str = None,
    carrier_plate_number: str = None,
    tracking_number: str = None,
    delivery_status: str = None,
    metadata_description: str = None,
    metadata_author: str = None,
    metadata_last_modified: str = None,
    metadata_version: str = None,
    metadata_keywords: str = None,
    metadata_tags: str = None,
    metadata_category: str = None,
    metadata_file_type: str = None,
    metadata_language: str = None,
    metadata_status: str = "DRAFT",
    metadata_confidentiality: str = "INTERNAL",
    metadata_source_system: str = None,
    sector: str = None,
    reference_number: str = None,
    external_reference_id: str = None,
    priority: str = None,
    approved_by: str = None,
    approved_at: str = None,
    deadline: str = None,
    category: str = None,
    sender_name: str = None,
    sender_phone_number: str = None,
    sender_email: str = None,
    sender_address: str = None,
    sender_type: str = "ORGANIZATION",
):
    # Create Ledger using helper function
    ledger = create_ledger_entry(
        ledger_description=ledger_description,
        ledger_subject=ledger_subject,
        ledger_type=ledger_type,
        approved_at=approved_at,
        approved_by=approved_by,
        status=status,
        received_at=received_at,
        reference_number=reference_number,
        deadline=deadline,
        category=category,
        priority=priority,
    )

    create_carrier(
        ledger=ledger,
        carrier_person_first_name=carrier_person_first_name,
        carrier_person_last_name=carrier_person_last_name,
        carrier_person_middle_name=carrier_person_middle_name,
        carrier_phone_number=carrier_phone_number,
        carrier_type=carrier_type,
        carrier_organization_id=carrier_organization_id,
        carrier_plate_number=carrier_plate_number,
    )

    create_recipient(
        ledger=ledger,
        recipient_name=recipient_name,
        recipient_phone_number=recipient_phone_number,
        department=department,
        job_title=job_title,
        sector=sector,
    )

    create_document_with_attachments_and_letters(
        ledger=ledger,
        document_type=document_type,
        document_date=document_date,
        document_owner=document_owner,
        additional_message=additional_message,
        attachments_data=attachments,
        letters_data=letters,
        current_user=current_user,
        external_reference_id=external_reference_id,
    )

    create_delivery(
        ledger=ledger,
        expected_delivery_date=expected_delivery_date,
        delivery_medium=delivery_medium,
        delivery_channel=delivery_channel,
        delivery_organization=delivery_organization,
        delivery_status=delivery_status,
    )

    create_metadata(
        ledger=ledger,
        metadata_title=metadata_title,
        metadata_description=metadata_description,
        metadata_author=metadata_author,
        metadata_date_created=metadata_date_created,
        metadata_last_modified=metadata_last_modified,
        metadata_version=metadata_version,
        metadata_keywords=metadata_keywords,
        metadata_tags=metadata_tags,
        metadata_category=metadata_category,
        metadata_file_type=metadata_file_type,
        metadata_language=metadata_language,
        metadata_status=metadata_status,
        metadata_confidentiality=metadata_confidentiality,
        metadata_source_system=metadata_source_system,
    )

    create_sender(
        ledger=ledger,
        sender_name=sender_name,
        sender_phone_number=sender_phone_number,
        sender_email=sender_email,
        sender_address=sender_address,
        sender_type=sender_type,
    )

    return ledger


def create_ledger_entry(
    received_at: str,
    ledger_description: str = None,
    ledger_subject: str = None,
    ledger_type: str = None,
    approved_at: str = None,
    approved_by: str = None,
    status: str = "PENDING",
    reference_number: str = None,
    deadline: str = None,
    category: str = None,
    priority: str = None,
    tracking_number: str = None,
) -> Ledger:
    ledger = Ledger.objects.create(
        ledger_description=ledger_description,
        ledger_subject=ledger_subject,
        ledger_type=ledger_type,
        approved_at=approved_at,
        approved_by=approved_by,
        status=status,
        received_at=received_at,
        reference_number=reference_number,
        deadline=deadline,
        category=category,
        priority=priority,
        tracking_number=tracking_number,
    )

    ledger.full_clean()

    ledger.save()

    return ledger


def create_carrier(
    ledger,
    carrier_person_first_name: str,
    carrier_person_last_name: str,
    carrier_person_middle_name: str,
    carrier_phone_number: str,
    carrier_type: str,
    carrier_organization_id: str = None,
    carrier_plate_number: str = None,
) -> Carrier:
    carrier = Carrier.objects.create(
        ledger=ledger,
        carrier_person_first_name=carrier_person_first_name,
        carrier_person_last_name=carrier_person_last_name,
        carrier_person_middle_name=carrier_person_middle_name,
        carrier_phone_number=carrier_phone_number,
        carrier_type=carrier_type,
        carrier_organization_id=carrier_organization_id,
        carrier_plate_number=carrier_plate_number,
    )

    carrier.full_clean()

    carrier.save()

    return carrier


def create_recipient(
    ledger,
    recipient_name: str,
    recipient_phone_number: str,
    department: str,
    job_title: str,
    sector: str,
) -> Recipient:
    try:
        recipient_department = Department.objects.get(id=department)
    except Department.DoesNotExist:
        raise ValueError(f"Department with id '{department}' does not exist.")

    try:
        recipient_job_title = JobTitle.objects.get(id=job_title)
    except JobTitle.DoesNotExist:
        raise ValueError(f"Job title with id '{job_title}' does not exist.")

    recipient = Recipient.objects.create(
        ledger=ledger,
        recipient_name=recipient_name,
        recipient_phone_number=recipient_phone_number,
        department=recipient_department,
        job_title=recipient_job_title,
        sector=sector,
    )

    recipient.full_clean()

    recipient.save()

    return recipient


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


def create_document_with_attachments_and_letters(
    ledger,
    current_user,
    letters_data: list,
    document_type: str = None,
    document_date: str = None,
    document_owner: str = None,
    additional_message: str = None,
    external_reference_id: str = None,
    attachments_data: list = None,
) -> Document:
    if attachments_data is None:
        attachments_data = []

    if letters_data is None:
        raise ValueError("letter is required!")

    document = Document.objects.create(
        ledger=ledger,
        document_type=document_type,
        document_date=document_date,
        document_owner=document_owner,
        additional_message=additional_message,
        external_reference_id=external_reference_id,
    )

    # Handle Attachments
    for attachment_file in attachments_data:
        attachment = create_attachment(
            file_data={"file": attachment_file},
            current_user=current_user,
            model_class=Attachment,
        )
        if attachment:
            document.attachment.add(attachment)

    # Handle Letters
    for letter_file in letters_data:
        letter_attachment = create_attachment(
            file_data={"file": letter_file},
            current_user=current_user,
            model_class=LedgerDoumentAttachment,
        )
        if letter_attachment:
            document.letter.add(letter_attachment)

    document.save()

    return document


def create_metadata(
    ledger,
    metadata_title: str = None,
    metadata_description: str = None,
    metadata_author: str = None,
    metadata_date_created: str = None,
    metadata_last_modified: str = None,
    metadata_version: str = None,
    metadata_keywords: str = None,
    metadata_tags: str = None,
    metadata_category: str = None,
    metadata_file_type: str = None,
    metadata_language: str = None,
    metadata_status: str = None,
    metadata_confidentiality: str = None,
    metadata_source_system: str = None,
) -> Metadata:
    metadata = Metadata.objects.create(
        ledger=ledger,
        metadata_title=metadata_title,
        metadata_description=metadata_description,
        metadata_author=metadata_author,
        metadata_date_created=metadata_date_created,
        metadata_last_modified=metadata_last_modified,
        metadata_version=metadata_version,
        metadata_keywords=metadata_keywords,
        metadata_tags=metadata_tags,
        metadata_category=metadata_category,
        metadata_file_type=metadata_file_type,
        metadata_language=metadata_language,
        metadata_status=metadata_status,
        metadata_confidentiality=metadata_confidentiality,
        metadata_source_system=metadata_source_system,
    )

    metadata.full_clean()

    metadata.save()

    return metadata


def create_delivery(
    ledger,
    expected_delivery_date,
    delivery_medium: str = None,
    delivery_channel: str = None,
    delivery_organization: str = None,
    delivery_status: str = None,
) -> Delivery:
    delivery = Delivery.objects.create(
        ledger=ledger,
        expected_delivery_date=expected_delivery_date,
        delivery_medium=delivery_medium,
        delivery_channel=delivery_channel,
        delivery_organization=delivery_organization,
        delivery_status=delivery_status,
    )

    delivery.full_clean()

    delivery.save()

    return delivery


def create_sender(
    *,
    ledger,
    sender_name,
    sender_phone_number,
    sender_email,
    sender_address,
    sender_type,
) -> Sender:
    sender = Sender.objects.create(
        ledger=ledger,
        sender_name=sender_name,
        sender_phone_number=sender_phone_number,
        sender_email=sender_email,
        sender_address=sender_address,
        sender_type=sender_type,
    )

    sender.full_clean()

    sender.save()

    return sender
