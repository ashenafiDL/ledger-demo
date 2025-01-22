from django.urls import path

from .apis import (
    LedgerDetailAPIView,
    LedgerListApi,
    LedgerNewAPIView,
    LedgerPdfDownloadAPIView,
)

app_name = "ledgers"

urlpatterns = [
    # path("create/ledger/", LedgerCreate.as_view(), name="createledger"),
    path("", LedgerListApi.as_view(), name="ledger_list"),
    path("<uuid:ledger_id>/detail/", LedgerDetailAPIView.as_view(), name="ledger_detail"),
    path("<uuid:ledger_id>/pdf/", LedgerPdfDownloadAPIView.as_view(), name="ledger_pdf"),
    path("create/", LedgerNewAPIView.as_view(), name="ledger-create"),
    # path("create/carrier/", CarrierCreateAPIView.as_view(), name="createcarrier"),
    # path("create/recipient/", RecipientCreateAPIView.as_view(), name="rec"),
    # path("create/document/", DocumentCreateAPIView.as_view(), name="doc"),
    # path("create/delivery/", DeliveryCreateAPIView.as_view(), name="delivery"),
]
