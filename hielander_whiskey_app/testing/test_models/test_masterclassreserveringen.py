from django.db import IntegrityError
from django.forms import ValidationError
from django.test import TestCase
from datetime import datetime
from hielander_whiskey_app.models import MasterclassReserveringen

class test_MasterclassReserveringen(TestCase):
    """
    Test class voor het testen van het MasterclassReserveringen model.
    Erft over van TestCase.

    Overzicht van de testcases in deze klasse:
    1. test_string_functie_met_tussenvoegsel: Test de __str__ functie van MasterclassReserveringen met een tussenvoegsel.
    2. test_string_functie_zonder_tussenvoegsel: Test de __str__ functie van MasterclassReserveringen zonder tussenvoegsel.
    3. test_default_waarde_reserve: Test de default waarde van het reserve-field.
    4. test_auto_datefield: Test het automatisch aanmaken van het datum field.
    5. test_auto_timefield: Test het automatisch aanmaken van het tijd field.
    6. test_email_validatie1: Test e-mail validatie met een fout e-mail format.
    7. test_email_validatie2: Test e-mail validatie met een ander fout e-mail format.
    8. test_positief_fields: Test de type constraints van aantal_flessen en totaalprijs.
    9. test_max_length_namen: Test de maximale lengte van de voornaam en achternaam fields.
    10. test_ordering: Test de ordering van de meta class van het model.
    """

    def maak_instance(self, 
                      voornaam, 
                      tussenvoegsel, 
                      achternaam, 
                      e_mailadres, 
                      sessie_nummer=1, 
                      masterclass="masterclass 1", 
                      aantal_kaarten=2, 
                      totaalprijs=30, 
                      opmerking=None):
        """
        Initialiseert een instance van MasterclassReserveringen zodat deze niet bij elke test opnieuw hoeft te worden aangemaakt.

        :param voornaam: De voornaam van de reservering.
        :type voornaam: str
        :param tussenvoegsel: Het tussenvoegsel van de reservering.
        :type tussenvoegsel: str
        :param achternaam: De achternaam van de reservering.
        :type achternaam: str
        :param e_mailadres: Het e-mailadres van de reservering.
        :type e_mailadres: str
        :param sessie_nummer: Het gekozen sessienummer van de reservering (default: 1).
        :type sessie_nummer: int
        :param masterclass: De gekozen masterclass van de reservering (default: "masterclass 1").
        :type masterclass: str
        :param aantal_kaarten: Het aantal geselecteerde kaarten dat is gereserveerd (default: 2).
        :type aantal_kaarten: int
        :param totaalprijs: De totaalprijs van de reservering (default: 30).
        :type totaalprijs: int
        :param opmerking: De opmerking bij de reservering, deze is optioneel (default: None).
        :type opmerking: str or None
        :return: Een instantie van MasterclassReserveringen.
        :rtype: MasterclassReserveringen
        """
        
        return MasterclassReserveringen.objects.create(
            voornaam=voornaam,
            tussenvoegsel=tussenvoegsel,
            achternaam=achternaam,
            e_mailadres=e_mailadres,
            sessie_nummer=sessie_nummer,
            masterclass=masterclass,
            aantal_kaarten=aantal_kaarten,
            totaalprijs=totaalprijs,
            opmerking=opmerking,
        )

    def test_string_functie_met_tussenvoegsel(self):
        """
        Test de __str__ functie van MasterclassReserveringen met een tussenvoegsel.

        Deze test controleert of de __str__ functie van MasterclassReserveringen het juiste resultaat returned
        als er een tussenvoegsel aanwezig is in de naam van de klant.
        """
        instance = self.maak_instance("John", "van", "Doe", "john@doe.com")
        self.assertEqual(str(instance), "John van Doe - masterclass 1 ")

    def test_string_functie_zonder_tussenvoegsel(self):
        """
        Test de __str__ functie van MasterclassReserveringen zonder tussenvoegsel.

        Deze test controleert of de __str__ functie van MasterclassReserveringen het juiste resultaat returned
        als er geen tussenvoegsel aanwezig is in de naam van de klant.
        """
        instance = self.maak_instance("Foo", "", "Bar", "foo@bar.com")
        self.assertEqual(str(instance), "Foo  Bar - masterclass 1 ")

    def test_default_waarde_reserve(self):
        """
        Test de default waarde van het reserve-field.

        Deze test controleert of het reserve-field van MasterclassReserveringen de juiste defaultwaarde heeft.
        """
        instance = self.maak_instance("Foo", "", "Bar", "foo@bar.com")
        self.assertFalse(instance.reserve)

    def test_auto_datefield(self):
        """
        Test het automatisch aanmaken van het datum field.

        Deze test controleert of het datum field van MasterclassReserveringen automatisch wordt aangemaakt met de
        huidige datum.
        """
        instance = self.maak_instance("Foo", "", "Bar", "foo@bar.com")
        self.assertEqual(instance.datum, datetime.now().date())

    def test_auto_timefield(self):
        """
        Test het automatisch aanmaken van het tijd field.

        Deze test controleert of het tijd field van MasterclassReserveringen automatisch wordt aangemaakt met de
        huidige tijd.
        """
        instance = self.maak_instance("Foo", "", "Bar", "foo@bar.com")
        self.assertEqual(instance.tijd, datetime.now().time())

    def test_email_validatie1(self):
        """
        Test e-mail validatie met een fout e-mail format.

        Deze test controleert of de e-mail validatie van MasterclassReserveringen een ValidationError
        veroorzaakt wanneer er een ongeldig e-mailadres wordt opgegeven.
        """
        instance = self.maak_instance("Foo", "", "Bar", "foobar.com")
        self.assertRaises(ValidationError, instance.full_clean)
    def test_email_validatie2(self):
        """
        Test e-mail validatie met een fout e-mail format.

        Deze test controleert of de e-mail validatie van MasterclassReserveringen een ValidationError
        veroorzaakt wanneer er een ander ongeldig e-mailadres wordt opgegeven.
        """
        instance2 = self.maak_instance("Foo", "", "Bar", "foo@barcom")
        self.assertRaises(ValidationError, instance2.full_clean)

    def test_sessie_nummer_positive_constraint(self):
        """
        Test de positieve constraint van sessie_nummer.

        Deze test controleert of MasterclassReserveringen de juiste constraint maakt op het sessie_nummer field,
        door te controleren of het aanmaken van een instance met een negatieve waarde een IntegrityError geeft.
        """
        with self.assertRaises(IntegrityError):
            self.maak_instance("Foo", "", "Bar", "foo@bar.com", sessie_nummer=-1)

    def test_aantal_kaarten_positive_constraint(self):
        """
        Test de positieve constraint van aantal_kaarten.

        Deze test controleert of MasterclassReserveringen de juiste constraint maakt op het aantal_kaarten field,
        door te controleren of het aanmaken van een instance met een negatieve waarde een IntegrityError geeft.
        """
        with self.assertRaises(IntegrityError):
            self.maak_instance("Foo", "", "Bar", "foo@bar.com", aantal_kaarten=-2)

    def test_totaalprijs_positive_constraint(self):
        """
        Test de positieve constraint van totaalprijs.

        Deze test controleert of MasterclassReserveringen de juiste constraint maakt op het totaalprijs field,
        door te controleren of het aanmaken van een instance met een negatieve waarde een IntegrityError geeft.
        """
        with self.assertRaises(IntegrityError):
            self.maak_instance("Foo", "", "Bar", "foo@bar.com", totaalprijs=-30)

    def test_max_length_namen(self):
        """
        Test de maximale lengte van de voornaam en achternaam fields.

        Deze test controleert of MasterclassReserveringen de juiste constraints geeft aan de 
        voornaam en achternaam, door te controleren of het aanmaken van een instance met te lange namen
        een ValidationError geeft.
        """
        instance = MasterclassReserveringen(
            voornaam="Foo" * 256,
            tussenvoegsel="",
            achternaam="Bar" * 256,
            e_mailadres="foo@bar.com",
        )
        with self.assertRaises(ValidationError):
            instance.full_clean()

    def test_ordering(self):
        """
        Test de ordering van de meta class van het model.

        Deze test controleert of de meta class van MasterclassReserveringen de juiste ordering heeft
        door te controleren of de ordering eigenschap gelijk is aan ["-datum", "-tijd"].
        """
        instance = self.maak_instance("Foo", "", "Bar", "foo@bar.com")
        self.assertEqual(instance._meta.ordering, ["-datum", "-tijd"])
