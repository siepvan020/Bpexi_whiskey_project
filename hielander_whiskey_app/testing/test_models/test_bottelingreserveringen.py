from django.db import IntegrityError
from django.forms import ValidationError
from django.test import TestCase
from datetime import datetime
from hielander_whiskey_app.models import BottelingReserveringen

class test_BottelingReserveringen(TestCase):
    """
    Test class voor het testen van het BottelingReserveringen model.
    Erft over van TestCase.

    Overzicht van de testcases in deze klasse:
    1. test_string_functie_met_tussenvoegsel: Test de __str__ functie van BottelingReserveringen met een tussenvoegsel.
    2. test_string_functie_zonder_tussenvoegsel: Test de __str__ functie van BottelingReserveringen zonder tussenvoegsel.
    3. test_default_waarde_reserve: Test de default waarde van het reserve field.
    4. test_auto_datefield: Test het automatisch aanmaken van het datum field.
    5. test_auto_timefield: Test het automatisch aanmaken van het tijd field.
    6. test_email_validatie1: Test e-mail validatie met een fout e-mail format.
    7. test_email_validatie2: Test e-mail validatie met een ander fout e-mail format.
    8. test_positief_fields: Test de positieve constraints van aantal_flessen en totaalprijs.
    9. test_max_length_namen: Test de maximale lengte van de voornaam en achternaam fields.
    10. test_ordering: Test de ordering van de meta class van het model.
    """

    def maak_instance(self, 
                      voornaam, 
                      tussenvoegsel, 
                      achternaam, 
                      e_mailadres, 
                      aantal_flessen=2, 
                      totaalprijs=205, 
                      opmerking=None):
        """
        Initialiseert een instantie van Bottelingreserveringen zodat deze niet bij elke test opnieuw hoeft te worden aangemaakt.

        :param voornaam: De voornaam van de reservering.
        :type voornaam: str
        :param tussenvoegsel: Het tussenvoegsel van de reservering.
        :type tussenvoegsel: str
        :param achternaam: De achternaam van de reservering.
        :type achternaam: str
        :param e_mailadres: Het e-mailadres van de reservering.
        :type e_mailadres: str
        :param aantal_flessen: Het aantal flessen dat is gereserveerd (default: 2).
        :type aantal_flessen: int
        :param totaalprijs: De totaalprijs van de reservering (default: 205).
        :type totaalprijs: int
        :param opmerking: Optionele opmerking bij de reservering (default: None).
        :type opmerking: str or None
        :return: Instance van BottelingReserveringen.
        :rtype: BottelingReserveringen
        """
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
        """
        Test de __str__ functie van BottelingReserveringen met een tussenvoegsel.

        Deze testcase controleert of de __str__ functie van BottelingReserveringen het juiste resultaat returned
        wanneer er een tussenvoegsel aanwezig is in de naam van de reservering.
        """
        instance = self.maak_instance("John", "van", "Doe", "john@doe.com")
        self.assertEqual(str(instance), "John van Doe - 2 flessen")

    def test_string_functie_zonder_tussenvoegsel(self):
        """
        Test de __str__ functie van BottelingReserveringen zonder tussenvoegsel.

        Deze testcase controleert of de __str__ functie van BottelingReserveringen het juiste resultaat returned
        wanneer er geen tussenvoegsel aanwezig is in de naam van de reservering.
        """
        instance = self.maak_instance("Foo", "", "Bar", "foo@bar.com")
        self.assertEqual(str(instance), "Foo Bar - 2 flessen")

    def test_default_waarde_reserve(self):
        """
        Test de default waarde van het reserve field.

        Deze testcase controleert of het reserve field van BottelingReserveringen de juiste default waarde heeft.
        """
        instance = self.maak_instance("Foo", "", "Bar", "foo@bar.com")
        self.assertFalse(instance.reserve)

    def test_auto_datefield(self):
        """
        Test het automatisch aanmaken van het datum field.

        Deze testcase controleert of het datum field van BottelingReserveringen automatisch wordt aangemaakt met de
        huidige datum.
        """
        instance = self.maak_instance("Foo", "", "Bar", "foo@bar.com")
        self.assertEqual(instance.datum, datetime.now().date())

    def test_auto_timefield(self):
        """
        Test het automatisch aanmaken van het tijd field.

        Deze testcase controleert of het tijd field van BottelingReserveringen automatisch wordt aangemaakt met de
        huidige tijd.
        """
        instance = self.maak_instance("Foo", "", "Bar", "foo@bar.com")
        self.assertEqual(instance.tijd, datetime.now().time())

    def test_email_validatie1(self):
        """
        Test e-mail validatie met een fout e-mail formaat.

        Deze testcase controleert of de e-mail validatie van BottelingReserveringen een ValidationError
        veroorzaakt wanneer er een ongeldig e-mailadres wordt opgegeven.
        """
        instance = self.maak_instance("Foo", "", "Bar", "foobar.com")
        self.assertRaises(ValidationError, instance.full_clean)

    def test_email_validatie2(self):
        """
        Test e-mail validatie met een fout e-mail formaat.

        Deze testcase controleert of de e-mail validatie van BottelingReserveringen een ValidationError
        veroorzaakt wanneer er een ander ongeldig e-mailadres wordt opgegeven.
        """
        instance2 = self.maak_instance("Foo", "", "Bar", "foo@barcom")
        self.assertRaises(ValidationError, instance2.full_clean)

    def test_positief_fields(self):
        """
        Test de positieve beperkingen van aantal_flessen en totaalprijs.

        Deze testcase controleert of BottelingReserveringen de juiste constraints heeft op de fields
        aantal_flessen en totaalprijs, door te controleren of het aanmaken van een instantie met negatieve
        waarden een IntegrityError geeft.
        """
        with self.assertRaises(IntegrityError):
            self.maak_instance("Foo", "", "Bar", "foo@bar.com", -2, -205)

    def test_max_length_namen(self):
        """
        Test de maximale lengte van de voornaam en achternaam fields.

        Deze testcase controleert of BottelingReserveringen de juiste beperkingen oplegt aan de fields
        voornaam en achternaam, door te controleren of het aanmaken van een instantie met te lange namen
        een ValidationError geeft.
        """
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
        """
        Test de ordering van de meta class van het model.

        Deze testcase controleert of de meta class van BottelingReserveringen de juiste volgorde heeft
        door te controleren of de ordering eigenschap gelijk is aan ["-datum", "-tijd"].
        """
        instance = self.maak_instance("Foo", "", "Bar", "foo@bar.com")
        self.assertEqual(instance._meta.ordering, ["-datum", "-tijd"])
