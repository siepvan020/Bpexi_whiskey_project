from django.db import IntegrityError, transaction
from django.test import TestCase
from django.db import models
from datetime import datetime
from hielander_whiskey_app.models import FestivalData
from django.core.exceptions import ValidationError

class test_FestivalData(TestCase):

    def maak_instance(self, 
                      type, 
                      naam, 
                      aantal_beschikbaar=100, 
                      prijs=100.0, 
                      tijd=None, 
                      sessie=None, 
                      datum=None):
        return FestivalData.objects.create(
            type=type,
            naam=naam,
            tijd=tijd,
            sessie=sessie,
            datum=datum,
            aantal_beschikbaar=aantal_beschikbaar,
            prijs=prijs
        )

    def test_type_none_constraint(self):
        with self.assertRaises(IntegrityError):
            self.maak_instance(type=None, 
                               naam="Festival Botteling fles", 
                               aantal_beschikbaar=150, 
                               prijs=100.0
        )
    
    def test_naam_none_constraint(self):
        with self.assertRaises(IntegrityError):
            self.maak_instance(type="Botteling", 
                               naam=None, 
                               aantal_beschikbaar=150, 
                               prijs=100.0
        )
    
    def test_aantal_beschikbaar_none_constraint(self):
        with self.assertRaises(IntegrityError):
            self.maak_instance(type="Botteling", 
                               naam="Festival Botteling fles", 
                               aantal_beschikbaar=None, 
                               prijs=100.0
        )
    
    def test_prijs_none_constraint(self):
        with self.assertRaises(IntegrityError):
            self.maak_instance(type="Botteling", 
                               naam="Festival Botteling fles", 
                               aantal_beschikbaar=150, 
                               prijs=None
        )


    def test_sessie_positive_constraint(self):
        with self.assertRaises(IntegrityError):
            self.maak_instance(type="Botteling", 
                               naam="Festival Botteling fles", 
                               aantal_beschikbaar=150, 
                               prijs=100.0,
                               sessie=-1
        )
    
    def test_aantal_beschikbaar_positive_constraint(self):
        with self.assertRaises(IntegrityError):
            self.maak_instance(type="Botteling", 
                               naam="Festival Botteling fles", 
                               aantal_beschikbaar=-150, 
                               prijs=100.0
        )