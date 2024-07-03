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
    """
    Test class voor de dashboard pagina.
    Erft over van TestCase.

    Overzicht van de testcases in deze klasse:
    1. test_get_request: Test het uitvoeren van een GET-request naar de dashboard pagina.
    2. test_get_request_uitgelogd: Test het uitvoeren van een GET-request naar de dashboard pagina als de gebruiker is uitgelogd.
    3. test_post_value_error: Test het submitten van data die een ValueError geeft via een POST request naar de dashboard pagina.
    4. test_post_exception: Test het submitten van data die een algemene Exception geeft via een POST request naar de dashboard pagina.
    5. test_post_valid_data: Test het submitten van valid data via een POST request naar de dashboard pagina.
    6. test_grafiek_functies: Test het aanroepen van grafiek functies bij het uitvoeren van een GET-request naar de dashboard pagina.
    """

    def setUp(self):
        """
        Setup methode wordt uitgevoerd voor elke testcase.
        Initialiseert de testclient en de URL van de dashboard pagina.
        Logt een testgebruiker in en creëert dummy data voor FestivalData, BottelingReserveringen en MasterclassReserveringen.
        """
        self.client = Client()
        self.url = reverse('dashboard')

        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        festival_data_botteling_data = {
            'type': 'botteling',
            'naam': 'Ardmore (Ardlair) 2014 57.5%',
            'tijd': None,
            'sessie': None,
            'datum': None,
            'aantal_beschikbaar': 150,
            'prijs': 102.5
        }
        festival_data_masterclass_data = {
            'type': 'masterclass 1',
            'naam': 'Kenny MacDonald - Dram Mhor Group LTD',
            'tijd': datetime.now().time(),
            'sessie': 1,
            'datum': datetime.now().date(),
            'aantal_beschikbaar': 30,
            'prijs': 15.0
        }
        bottelingreservering_data = {
            'voornaam': 'John',
            'achternaam': 'Doe',
            'e_mailadres': 'john.doe@example.com',
            'aantal_flessen': 2,
            'totaalprijs': 205
        }
        mcreservering_data = {
            'voornaam': 'Jane',
            'achternaam': 'Doe',
            'e_mailadres': 'jane.doe@example.com',
            'aantal_kaarten': 3,
            'totaalprijs': 45,
            'masterclass': 'masterclass 1',
            'sessie_nummer': 1
        }

        self.festival_data_botteling = FestivalData.objects.create(**festival_data_botteling_data)
        self.festival_data_masterclass = FestivalData.objects.create(**festival_data_masterclass_data)
        self.bottelingreservering = BottelingReserveringen.objects.create(**bottelingreservering_data)
        self.mcreservering = MasterclassReserveringen.objects.create(**mcreservering_data)
    

    def test_get_request(self):
        """
        Testcase voor het uitvoeren van een GET-request naar de dashboard pagina.
        Controleert of de response:
        - Valid context heeft
        - Een statuscode van 200 heeft
        - De goede template gebruikt
        - De juiste context data bevat voor aantallen, botteling, masterclass en festivaldata.
        """
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
        """
        Testcase voor het uitvoeren van een GET-request naar de dashboard pagina als de gebruiker is uitgelogd.
        Controleert of de response:
        - Een statuscode van 302 heeft
        - De gebruiker wordt doorgestuurd naar de login pagina
        - De 'dashboard.html' template niet gebruikt.
        """
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/dashboard/')
        self.assertTemplateNotUsed(response, 'dashboard.html')
    

    @patch('hielander_whiskey_app.views.dashboard.FestivalData.save')
    def test_post_value_error(self, mock_save):
        """
        Testcase voor het triggeren van de ValueError via een POST request naar de dashboard pagina.
        Controleert of de response:
        - Een statuscode van 200 heeft
        - De goede template gebruikt
        - Een juiste foutmelding in de messages bevat.
        """
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
    def test_post_exception(self, mock_save):
        """
        Testcase voor het triggeren van de algemene Exception via een POST request naar de dashboard pagina.
        Controleert of de response:
        - Een statuscode van 200 heeft
        - De goede template gebruikt
        - Een juiste foutmelding in de messages bevat.

        :param mock_save: Het mock object voor de save method van FestivalData.
        :type mock_save: MagicMock
        :param data: De data die wordt meegestuurd in het POST request.
        :type data: dict
        :return: None
        """
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
        """
        Testcase voor het submitten van geldige data via een POST request naar de dashboard pagina.
        Controleert of de response:
        - Een statuscode van 200 heeft
        - De goede template gebruikt
        - Een succesvolle update melding in de messages bevat
        - De FestivalData objecten correct geüpdatet zijn.
        """
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

    
    @patch('hielander_whiskey_app.views.dashboard.bottel_piechart')
    @patch('hielander_whiskey_app.views.dashboard.masterclass_barplot')
    def test_grafiek_functies(self, mock_masterclass_barplot, mock_bottel_piechart):
        """
        Testcase voor het controleren of de grafiek functies worden aangeroepen bij het uitvoeren van een GET-request naar de dashboard pagina.
        
        :param mock_masterclass_barplot: Het mock object voor de functie masterclass_barplot.
        :type mock_masterclass_barplot: MagicMock
        :param mock_bottel_piechart: Het mock object voor de functie bottel_piechart.
        :type mock_bottel_piechart: MagicMock

        Controleert of de response:
        - Een statuscode van 200 heeft
        - De goede template gebruikt
        - De grafiek functies bottel_piechart en masterclass_barplot worden aangeroepen.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        mock_bottel_piechart.assert_called_once()
        mock_masterclass_barplot.assert_called_once()
