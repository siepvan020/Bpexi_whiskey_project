# Third party imports
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from unittest.mock import patch
from datetime import datetime
from django.contrib.messages import get_messages

# Local imports
from hielander_whiskey_app.models import BottelingReserveringen, FestivalData, MasterclassReserveringen


class TestDashboardPage(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('dashboard')

        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.festival_data_botteling = FestivalData.objects.create(
            type='botteling',
            naam='Ardmore (Ardlair) 2014 57.5%',
            tijd=None,
            sessie=None,
            datum=None,
            aantal_beschikbaar=150,
            prijs=102.5
        )
        self.festival_data_masterclass = FestivalData.objects.create(
            type='masterclass 1',
            naam='Kenny MacDonald - Dram Mhor Group LTD',
            tijd=datetime.now().time(),
            sessie=1,
            datum=datetime.now().date(),
            aantal_beschikbaar=30,
            prijs=15.0
        )
        self.bottelingreservering = BottelingReserveringen.objects.create(
            voornaam='John',
            achternaam='Doe',
            e_mailadres='john.doe@example.com',
            aantal_flessen=2,
            totaalprijs=205
        )
        self.mcreservering = MasterclassReserveringen.objects.create(
            voornaam='Jane',
            achternaam='Doe',
            e_mailadres='jane.doe@example.com',
            aantal_kaarten=3,
            totaalprijs=45,
            masterclass='masterclass 1',
            sessie_nummer=1
        )
    

    def test_get_request(self):
        response = self.client.get(self.url)
        self.assertIsNotNone(response.context)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertIn('aantallen', response.context)
        self.assertIn(self.festival_data_botteling, response.context['festivaldata'])
        self.assertIn(self.bottelingreservering, response.context['botteling'])
        self.assertIn(self.festival_data_masterclass, response.context['festivaldata'])
        self.assertIn(self.mcreservering, response.context['masterclass'])
    

    def test_get_request_uitgelogd(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/dashboard/')
        self.assertTemplateNotUsed(response, 'dashboard.html')
    

    @patch('hielander_whiskey_app.views.dashboard.FestivalData.save')
    def test_post_value_error(self, mock_save):
        mock_save.side_effect = ValueError("Test ValueError")
        data = {
            'naam_1': 'Ardmore (Ardlair) 2014 57.5%',
            'aantal_beschikbaar_1': 150,
            'prijs_1': 102.5
        }        
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Value error voor" in message.message for message in messages))
    

    @patch('hielander_whiskey_app.views.dashboard.FestivalData.save')
    def test_post_general_exception(self, mock_save):
        mock_save.side_effect = Exception("Test Exception")
        data = {
            'naam_1': 'Ardmore (Ardlair) 2014 57.5%',
            'aantal_beschikbaar_1': 150,
            'prijs_1': 102.5
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Error bij het updaten van" in message.message for message in messages))

    
    def test_post_valid_data(self):
        data = {
            'naam_1': 'Nieuwe botteling naam',
            'aantal_beschikbaar_1': 180,
            'prijs_1': 120.0
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.message == "Festival Data succesvol geüpdatet!" for message in messages))
        self.festival_data_botteling.refresh_from_db()
        self.assertEqual(self.festival_data_botteling.naam, 'Nieuwe botteling naam')
        self.assertEqual(self.festival_data_botteling.aantal_beschikbaar, 180)
        self.assertEqual(self.festival_data_botteling.prijs, 120.0)
