import io

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.files.storage import default_storage
from django.template.loader import render_to_string
from django_weasyprint.utils import django_url_fetcher
from rest_framework.exceptions import ValidationError
from weasyprint import HTML

from core.ledgers.selectors import ledger_details

logger = get_task_logger(__name__)


@shared_task(bind=True, soft_time_limit=60, time_limit=120)
def generate_ledger_pdf(self, ledger_id):
    ledger = ledger_details(ledger_id=ledger_id)
    try:
        context = {
            "ledger": ledger,
        }

        template = "ledger_templates/incoming_ledger_template.html"
        html_content = render_to_string(template_name=template, context=context)
        pdf_io = io.BytesIO()

        # Generate PDF from HTML content
        weasy_html = HTML(
            string=html_content,
            url_fetcher=django_url_fetcher,
            base_url=settings.MEDIA_ROOT,
        )
        weasy_html.write_pdf(pdf_io)
        pdf_io.seek(0)

        ledger_pdf_path = f"ledger/incoming/pdf/{ledger.ledger_type}/{ledger.ledger_subject}.pdf"

        if default_storage.exists(ledger_pdf_path):
            default_storage.delete(ledger_pdf_path)

        default_storage.save(ledger_pdf_path, pdf_io)

        ledger.ledger_pdf = ledger_pdf_path

        ledger.save(update_fields=["ledger_pdf"])

        logger.info(f"PDF generation completed successfully for id: {ledger.id}")

        return

    except ValueError as e:
        raise ValidationError(e)

    except Exception as e:
        raise e
