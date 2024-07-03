from django.db import DataError, IntegrityError
from django.test import TestCase
from django.core.exceptions import ValidationError
from hielander_whiskey_app.models import FestivalData

class test_FestivalData(TestCase):
    """
    Testklasse voor het testen van de FestivalData modelklasse.
    Erft over van TestCase.

    Overzicht van de testcases in deze klasse:
    1. test_instantie_maken: Test of een instantie van FestivalData aangemaakt kan worden.
    2. test_type_none_constraint: Test of een IntegrityError wordt gegeven wanneer het type van FestivalData None is.
    3. test_naam_none_constraint: Test of een IntegrityError wordt gegeven wanneer de naam van FestivalData None is.
    4. test_aantal_beschikbaar_none_constraint: Test of een IntegrityError wordt gegeven wanneer het aantal beschikbare festivaldata None is.
    5. test_prijs_none_constraint: Test of een IntegrityError wordt gegeven wanneer de prijs van FestivalData None is.
    6. test_sessie_positive_constraint: Test of een IntegrityError wordt gegeven wanneer de sessie van FestivalData negatief is.
    7. test_aantal_beschikbaar_positive_constraint: Test of een IntegrityError wordt gegeven wanneer het aantal beschikbare festivaldata negatief is.
    8. test_type_maxlength_constraint: Test of een ValidationError wordt gegeven wanneer het type van FestivalData de maximale lengte overgaat.
    9. test_naam_maxlength_constraint: Test of een ValidationError wordt gegeven wanneer de naam van FestivalData de maximale lengte overgaat.

    """

    def maak_instance(self, 
                      type: str, 
                      naam: str, 
                      aantal_beschikbaar: int = 100, 
                      prijs: float = 100.0, 
                      tijd: str = None, 
                      sessie: int = None, 
                      datum: str = None) -> FestivalData:
        """
        Maakt een instantie van FestivalData aan met de opgegeven parameters.

        :param type: Het type van de festivaldata instantie.
        :type type: str
        :param naam: De naam van de festivaldata instantie.
        :type naam: str
        :param aantal_beschikbaar: Het aantal beschikbare festivaldata (optioneel, default:100).
        :type aantal_beschikbaar: int
        :param prijs: De prijs van de instantie (optioneel, default: 100.0).
        :type prijs: float
        :param tijd: De tijd van de instantie (optioneel).
        :type tijd: str
        :param sessie: De sessie van de instantie (optioneel).
        :type sessie: int
        :param datum: De datum van de instantie (optioneel).
        :type datum: str
        :return: De aangemaakte instantie van FestivalData.
        :rtype: FestivalData
        """
        return FestivalData.objects.create(
            type=type,
            naam=naam,
            tijd=tijd,
            sessie=sessie,
            datum=datum,
            aantal_beschikbaar=aantal_beschikbaar,
            prijs=prijs
        )

    def test_instantie_maken(self):
        """
        Test of een instantie van FestivalData aangemaakt kan worden.
        """
        instance = self.maak_instance("Botteling", "Lekker flesje")
        self.assertIsInstance(instance, FestivalData)

    def test_type_none_constraint(self):
        """
        Test of een IntegrityError wordt gegeven wanneer het type van FestivalData None is.
        """
        with self.assertRaises(IntegrityError):
            self.maak_instance(type=None, naam="Festival Botteling fles")
    
    def test_naam_none_constraint(self):
        """
        Test of een IntegrityError wordt gegeven wanneer de naam van de instantie None is.
        """
        with self.assertRaises(IntegrityError):
            self.maak_instance(type="Botteling", naam=None)
    
    def test_aantal_beschikbaar_none_constraint(self):
        """
        Test of een IntegrityError wordt gegeven wanneer het aantal beschikbare tickets None is.
        """
        with self.assertRaises(IntegrityError):
            self.maak_instance(type="Botteling", naam="Festival Botteling fles", aantal_beschikbaar=None)
    
    def test_prijs_none_constraint(self):
        """
        Test of een IntegrityError wordt gegeven wanneer de prijs van de instantie None is.
        """
        with self.assertRaises(IntegrityError):
            self.maak_instance(type="Botteling", naam="Festival Botteling fles", prijs=None)


    def test_sessie_positive_constraint(self):
        """
        Test of een IntegrityError wordt gegeven wanneer het sessienummer van de instantie negatief is.
        """
        with self.assertRaises(IntegrityError):
            self.maak_instance(type="Botteling", naam="Festival Botteling fles", sessie=-1)
    
    def test_aantal_beschikbaar_positive_constraint(self):
        """
        Test of een IntegrityError wordt gegeven wanneer het aantal beschikbare tickets negatief is.
        """
        with self.assertRaises(IntegrityError):
            self.maak_instance(type="Botteling", naam="Festival Botteling fles", aantal_beschikbaar=-150)
    
    def test_type_maxlength_constraint(self):
        """
        Test of een ValidationError wordt gegeven wanneer het type field de maximale lengte overschrijdt.
        """
        instance = self.maak_instance(type="Botteling" * 256, naam="Festival Botteling fles")
        with self.assertRaises(ValidationError):
            instance.full_clean()
            
    def test_naam_maxlength_constraint(self):
        """
        Test of een ValidationError wordt gegeven wanneer de naam van de instantie de maximale lengte overschrijdt.
        """
        instance = self.maak_instance(type="Botteling", naam="Festival Botteling fles" * 256)
        with self.assertRaises(ValidationError):
            instance.full_clean()
