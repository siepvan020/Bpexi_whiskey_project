from django.db import DataError, IntegrityError
from django.forms import ValidationError
from django.test import TestCase
from django.core.validators import validate_email
from datetime import datetime
from hielander_whiskey_app.models import BottelingReserveringen

class test_BottelingReserveringen(TestCase):

    def maak_instance(self, voornaam, tussenvoegsel, achternaam, e_mailadres, aantal_flessen=2, totaalprijs=205, opmerking=None):
        return BottelingReserveringen.objects.create(
            voornaam=voornaam,
            tussenvoegsel=tussenvoegsel,
            achternaam=achternaam,
            e_mailadres=e_mailadres,
            aantal_flessen=aantal_flessen,
            totaalprijs=totaalprijs,
            opmerking=opmerking,
        )

    def test_string_functie_met_tussenvoegsel(self):
        # Test de __str__ functie met
        instance = self.maak_instance("John", "van", "Doe", "john@doe.com")
        self.assertEqual(str(instance), "John van Doe - 2 flessen")


    def test_string_functie_zonder_tussenvoegsel(self):
        # Test de __str__ functie zonder tussenvoegsel
        instance = self.maak_instance("Foo", "", "Bar", "foo@bar.com")
        self.assertEqual(str(instance), "Foo Bar - 2 flessen")

    
    def test_default_waarde_reserve(self):
        # Test de default value van het reserve field
        instance = self.maak_instance("Foo", "", "Bar", "foo@bar.com")
        self.assertFalse(instance.reserve)

    
    def test_auto_datefield(self):
        # Test het automatisch aanmaken van het datum field
        instance = self.maak_instance("Foo", "", "Bar", "foo@bar.com")
        self.assertEqual(instance.datum, datetime.now().date())

    
    def test_auto_timefield(self):
        # Test het automatisch van het tijd field
        instance = self.maak_instance("Foo", "", "Bar", "foo@bar.com")
        self.assertEqual(instance.tijd, datetime.now().time())

    
    def test_email_validatie1(self):
        # Test e-mail validatie met een fout e-mail format
        instance = self.maak_instance("Foo", "", "Bar", "foobar.com")
        self.assertRaises(ValidationError, instance.full_clean)
    def test_email_validatie2(self):
        # Test e-mail validatie met een fout e-mail format
        instance2 = self.maak_instance("Foo", "", "Bar", "foo@barcom")
        self.assertRaises(ValidationError, instance2.full_clean)
           

    def test_positief_fields(self):
        # Test de positive constraints van aantal_flessen en totaalprijs
        with self.assertRaises(IntegrityError):
            self.maak_instance("Foo", "", "Bar", "foo@bar.com", -2, -205)

    
    def test_max_length_namen(self):
        # Test de maximale lengte van de voornaam en achternaam fields
        instance = BottelingReserveringen(
            voornaam="Foo" * 256,
            tussenvoegsel="",
            achternaam="Bar" * 256,
            aantal_flessen=2,
            totaalprijs=205,
            e_mailadres="foo@bar.com",
        )
        with self.assertRaises(ValidationError):
            instance.full_clean()


    def test_ordering(self):
        # Test de volgorde van de meta class van het model
        instance = self.maak_instance("Foo", "", "Bar", "foo@bar.com")
        self.assertEqual(instance._meta.ordering, ["-datum", "-tijd"])
