# Third-party imports
from django.db import models


class FestivalData(models.Model):
    naam = models.CharField(
        max_length=255
    )
    tijd = models.TimeField(
        blank=True,
        null=True
    )
    sessie = models.PositiveSmallIntegerField(
        blank=True,
        null=True
    )
    datum = models.DateField(
        blank=True,
        null=True
    )
    aantal_beschikbaar = models.PositiveSmallIntegerField()

    prijs = models.PositiveSmallIntegerField()