from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel


class Carrier(BaseModel):
    class CarrierType(models.TextChoices):
        INDIVIDUAL = "INDIVIDUAL", _("Individual")
        ORGANIZATION = "ORGANIZATION", _("Organization")

    ledger = models.OneToOneField("ledgers.Ledger", on_delete=models.CASCADE, related_name="carrier")

    carrier_person_first_name = models.CharField(max_length=200)
    carrier_person_middle_name = models.CharField(max_length=200)
    carrier_person_last_name = models.CharField(max_length=200)
    carrier_phone_number = models.PositiveBigIntegerField()
    carrier_type = models.CharField(max_length=200, choices=CarrierType.choices, default=CarrierType.ORGANIZATION)
    carrier_organization_id = models.CharField(max_length=200, null=True, blank=True)
    carrier_plate_number = models.CharField(max_length=200, null=True, blank=True)

    @property
    def carrier_person_full_name(self):
        first_name = self.carrier_person_first_name or ""
        middle_name = self.carrier_person_middle_name or ""
        last_name = self.carrier_person_last_name or ""
        return " ".join(part for part in [first_name, middle_name, last_name] if part).strip()

    def __str__(self):
        return f"{self.carrier_person_full_name} - {self.carrier_type}"

    class Meta:
        verbose_name = _("Carrier")
        verbose_name_plural = _("Carriers")
