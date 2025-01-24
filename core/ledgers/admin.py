from django.contrib import admin
from .models import Ledger
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


class LedgerAdmin(admin.ModelAdmin):
    list_display = (
        "sender_name",
        "ledger_subject",
        "tracking_number",
        "ledger_status",
        "recipient_name",
        "priority",
        "metadata_confidentiality",
        "pdf_view_link",
    )
    search_fields = (
        "sender_name",
        "sender_email",
        "tracking_number",
        "ledger_subject",
        "recipient_name",
        "recipient_phone_number",
        "job_title",
        "department",
        "metadata_keywords",
        "metadata_tags",
        "metadata_fileType",
    )
    list_filter = (
        "ledger_status",
        "priority",
        "metadata_confidentiality",
        "written_at",
    )
    ordering = [
        "-updated_at",
    ]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "sender_name",
                    "sender_phone_number",
                    "sender_email",
                    "ledger_subject",
                    "tracking_number",
                    "ledger_status",
                )
            },
        ),
        (
            _("Recipient Information"),
            {
                "fields": (
                    "recipient_name",
                    "recipient_phone_number",
                    "job_title",
                    "department",
                )
            },
        ),
        (
            _("Document Information"),
            {
                "fields": (
                    "letter", 
                    "attachment", 
                    "written_at", 
                    "priority"),
            },
        ),
        (
            _("Metadata"),
            {
                "fields": (
                    "metadata_keywords",
                    "metadata_tags",
                    "metadata_fileType",
                    "metadata_confidentiality",
                )
            },
        ),
    )
    readonly_fields = ("written_at",)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("tracking_number",)
        return self.readonly_fields

    def pdf_view_link(self, obj):
        if obj.ledger_pdf:
            return format_html(
                '<a href="{}" target="_blank">View PDF</a>', obj.ledger_pdf
            )
        return "-"

    pdf_view_link.short_description = "PDF Version"


admin.site.register(Ledger, LedgerAdmin)
