import os

from django.core.files.storage import default_storage
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from .models.ledger import Ledger


def ledger_list():
    return Ledger.objects.all()


def ledger_details(*, ledger_id):
    try:
        return Ledger.objects.select_related(
            "carrier",
            "delivery",
            "document",
            "recipient",
            "metadatas",
            "sender",
        ).get(id=ledger_id)

    except Ledger.DoesNotExist:
        raise ValueError("Ledger Doesn't exist")


def ledgers_pdf(
    *,
    ledger_id,
):
    ledger = get_object_or_404(Ledger, id=ledger_id)
    if ledger.ledger_pdf:
        try:
            if default_storage.exists(ledger.ledger_pdf):
                response = FileResponse(
                    ledger.ledger_pdf,
                    as_attachment=True,
                    filename=os.path.basename(ledger.ledger_pdf),
                )
            return response
        except FileNotFoundError:
            raise Http404("PDF file not found.")
        except Exception as e:
            raise ValidationError(f"Failed to open the file: {str(e)}")

    raise ValueError("Ledger PDF not found.")
