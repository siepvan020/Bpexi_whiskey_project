# Third-party imports
from django.db import models


class MasterclassReserveringen(models.Model):
    voornaam = models.CharField(
        max_length=255
    )
    tussenvoegsel = models.CharField(
        max_length=255, 
        blank=True,
        null=True
    )
    achternaam = models.CharField(
        max_length=255
    )
    e_mailadres = models.EmailField()

    opmerking = models.TextField(
        max_length=500,
        blank=True,
        null=True
    )
    sessie_nummer = models.PositiveSmallIntegerField()

    masterclass = models.CharField(
        max_length=255
    )

    aantal_kaarten = models.PositiveSmallIntegerField()

    totaalprijs = models.PositiveSmallIntegerField()

    reserve = models.BooleanField(
        default=False
    )
    datum = models.DateField(
        auto_now_add=True
    )
    tijd = models.TimeField(
        auto_now_add=True
    )


    def __str__(self):
        return f"{self.voornaam} {self.tussenvoegsel} {self.achternaam} - {self.masterclass} "


    class Meta:
        verbose_name_plural = "Masterclass Reserveringen"
        ordering = ["-datum", "-tijd"]
