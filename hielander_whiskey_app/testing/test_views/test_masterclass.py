# Third party imports
import datetime
from django.test import Client, TestCase
from django.urls import reverse

# Local imports
from hielander_whiskey_app.models import FestivalData, MasterclassReserveringen
from hielander_whiskey_app.views.masterclass_reservering import masterclass_reservering_page


class TestMasterclassReserveringPage(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('masterclass_reservering')
        # Dummy, de view skipt namelijk de eerste instance
        FestivalData.objects.create(    
            type='botteling',
            aantal_beschikbaar=1,
            prijs=1
        )
        # Instantie waarmee wordt getest
        self.festival_data = FestivalData.objects.create(
            type='masterclass 1',
            naam='Kenny MacDonald - Dram Mhor Group LTD',
            tijd=datetime.datetime.now().time(),
            sessie=1,
            datum=datetime.datetime.now().date(),
            aantal_beschikbaar=30,
            prijs=15.0
        )
    

    def test_get_request(self):
        response = self.client.get(self.url)
        self.assertIsNotNone(response.context)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'masterclass_reservering.html')
        self.assertIn('masterclass_prijzen', response.context)
        self.assertEqual(response.context['masterclass_prijzen'], {'masterclass 1': 15.0})


    def test_post_valid_form(self):
        data = {
            'voornaam': 'Foo',
            'tussenvoegsel': '',
            'achternaam': 'Bar',
            'e_mailadres': 'foo.bar@example.com',
            'opmerking': '',
            'sessie_nummer': 1,
            'masterclass': 'masterclass 1',
            'aantal_kaarten': 2
            
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('masterclass_bevestiging'))
        self.assertEqual(MasterclassReserveringen.objects.count(), 1)
        reservation = MasterclassReserveringen.objects.first()
        self.assertEqual(reservation.totaalprijs, 30)
    