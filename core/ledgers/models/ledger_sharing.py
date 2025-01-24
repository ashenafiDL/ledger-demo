from django.db import models

from core.common.models import BaseModel
from core.users.models import Member

from .ledger import Ledger


class LedgerSharing(BaseModel):
    ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE, related_name="shared_ledger")
    shared_to = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="shared_ledgers")

    shared_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("ledger", "shared_to")

    def __str__(self):
        return f"Ledger {self.ledger.id} shared to {self.shared_to}"
