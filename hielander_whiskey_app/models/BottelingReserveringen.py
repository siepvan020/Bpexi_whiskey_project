# Third-party imports
from django.db import models


class BottelingReserveringen(models.Model):
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
    aantal_flessen = models.PositiveSmallIntegerField()

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
        if self.tussenvoegsel:
            return f"{self.voornaam} {self.tussenvoegsel} {self.achternaam} - {self.aantal_flessen} flessen"
        return f"{self.voornaam} {self.achternaam} - {self.aantal_flessen} flessen"


    class Meta:
        verbose_name_plural = "Botteling Reserveringen"
        ordering = ["-datum", "-tijd"]
