from django.test import TestCase
from hielander_whiskey_app.models import BottelingReserveringen


class test_BottelingReserveringen(TestCase):

    def setUp(self):
        self.botteling = BottelingReserveringen.objects.create(
            voornaam="John",
            tussenvoegsel="van",
            achternaam="Doe",
            e_mailadres="john.doe@example.com",
            aantal_flessen=2,
            totaalprijs=102.5
        )

    def test_string_functie_met_tussenvoegsel(self):
        self.assertEqual(str(self.botteling), "John van Doe - 2 flessen")


    def test_string_functie_zonder_tussenvoegsel(self):
        botteling_zonder_tussenvoegsel = BottelingReserveringen.objects.create(
            voornaam="Foo",
            achternaam="Bar",
            e_mailadres="foo.bar@example.com",
            aantal_flessen=2,
            totaalprijs=102.5
        )
        self.assertEqual(str(botteling_zonder_tussenvoegsel), "Foo Bar - 2 flessen")