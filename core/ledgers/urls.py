from django.urls import path

from .apis import (
    LedgerDetailAPIView,
    LedgerListApi,
    LedgerNewAPIView,
    LedgerPdfDownloadAPIView,
    SearchLedgerAPIView,
    ShareLedgerAPIView,
    SharedLedgersAPIView,
)

app_name = "ledgers"

urlpatterns = [
    path("", LedgerListApi.as_view(), name="ledger_list"),
    path("create/", LedgerNewAPIView.as_view(), name="ledger-create"),
    path("<uuid:ledger_id>/detail/", LedgerDetailAPIView.as_view(), name="ledger_detail"),
    path("<uuid:ledger_id>/pdf/", LedgerPdfDownloadAPIView.as_view(), name="ledger_pdf"),
    path("<uuid:ledger_id>/share/", ShareLedgerAPIView.as_view(), name="share-ledger"),
    path("shared/", SharedLedgersAPIView.as_view(), name="shared-ledgers"),
    path("search/<tracking_number>", SearchLedgerAPIView.as_view(), name='search-ledger'),
]
