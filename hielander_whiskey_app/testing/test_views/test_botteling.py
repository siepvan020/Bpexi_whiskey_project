# Third party imports
from unittest.mock import patch
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.messages import get_messages

# Local imports
from hielander_whiskey_app.models import BottelingReserveringen, FestivalData


class TestBottelingReserveringPage(TestCase):
    """
    Testklasse voor de BottelingReserveringPage.
    """

    def setUp(self):
        """
        Set up functie die wordt uitgevoerd voor elke testmethode.
        Initialiseert de testclient en de URL voor de botteling reserveringspagina.
        Maakt ook een instantie van FestivalData aan voor testdoeleinden.
        """
        self.client = Client()
        self.url = reverse('botteling_reservering')
        # Instantie waarmee wordt getest
        self.festival_data = FestivalData.objects.create(
            type='botteling',
            naam='Ardmore (Ardlair) 2014 57.5%',
            tijd=None,
            sessie=None,
            datum=None,
            aantal_beschikbaar=150,
            prijs=102.5
        )

        self.data = {
            'voornaam': 'Foo',
            'tussenvoegsel': '',
            'achternaam': 'Bar',
            'e_mailadres': 'foo.bar@example.com',
            'opmerking': '',
            'aantal_flessen': 2    
        }


    def test_get_request(self):
        """
        Test de GET request voor de botteling view.

        Deze test controleert het volgende:
        - De context van de response is niet None.
        - De statuscode van de response is 200.
        - De goede template ('botteling_reservering.html') wordt gebruikt.
        - De key 'flessen_over' is aanwezig in de context van de response.
        - De value van 'flessen_over' is 150, zoals ingesteld in de setUp methode.
        - De key 'fles' is aanwezig in de context van de response.
        - De value van 'fles' is een instance van de klasse FestivalData.
        """
        response = self.client.get(self.url)
        self.assertIsNotNone(response.context)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'botteling_reservering.html')
        self.assertIn('flessen_over', response.context)
        self.assertEqual(response.context['flessen_over'], 150)
        self.assertIn('fles', response.context)
        self.assertIsInstance(response.context['fles'], FestivalData)


    @patch('hielander_whiskey_app.views.botteling_reservering.setup_botteling_email')
    def test_post_valid_form(self, mock_send_email):
        """
        Test de POST request met valid data.

        Deze test controleert het volgende:
        - De statuscode van de response is 200.
        - De goede template ('botteling_bevestiging.html') wordt gebruikt.
        - Het aantal BottelingReserveringen objecten is 1.
        - De totaalprijs van de reservering is 205.
        - De functie setup_botteling_email wordt aangeroepen.
        """
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'botteling_bevestiging.html')
        self.assertEqual(BottelingReserveringen.objects.count(), 1)
        reservation = BottelingReserveringen.objects.first()
        self.assertEqual(reservation.totaalprijs, 205)
        mock_send_email.assert_called_once()

    
    def test_post_lege_voornaam(self):
        """
        Testcase voor het submitten van invalid data met een lege voornaam via een POST request naar de reserveringspagina.
        Controleert of de response:
        - Een statuscode van 200 heeft
        - De goede template gebruikt
        - De juiste foutmelding weergeeft.
        """
        data = self.data.copy()
        data['voornaam'] = ''
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'botteling_reservering.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.message == 'Reservering niet correct' \
                            for message in messages))


    def test_post_lege_achternaam(self):
        """
        Testcase voor het submitten van data met een lege achternaam via een POST request naar de reserveringspagina.
        Controleert of de response:
        - Een statuscode van 200 heeft
        - De goede template gebruikt
        - De juiste foutmelding weergeeft.
        """
        data = self.data.copy()
        data['achternaam'] = ''
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'botteling_reservering.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.message == 'Reservering niet correct' \
                            for message in messages))

    
    def test_post_foute_email(self):
        """
        Testcase voor het submitten van een formulier met een ongeldig e-mailadres via een POST request naar de reserveringspagina.
        Controleert of de response:
        - Een statuscode van 200 heeft
        - De goede template gebruikt
        - De juiste foutmelding weergeeft.
        """
        data = self.data.copy()
        data['e_mailadres'] = 'foobar'
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'botteling_reservering.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.message == 'E-mailadres is niet correct' \
                            for message in messages))


    def test_post_teveel_flessen(self):
        """
        Testcase voor het submitten van een formulier met teveel flessen via een POST request naar de reserveringspagina.
        Controleert of de response:
        - Een statuscode van 302 heeft (redirect).
        - De juiste redirect URL heeft.
        - De juiste foutmelding weergeeft.
        """
        data = self.data.copy()
        data['aantal_flessen'] = 3

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.url)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.message == \
                            'Kan niet meer dan 2 flessen per persoon reserveren'\
                                  for message in messages))


    def test_post_reservelijst(self):
        """
        Testcase voor het submitten van een formulier terwijl er al een reservering bestaat met hetzelfde e-mailadres.
        Controleert of de response:
        - Een statuscode van 200 heeft.
        - De goede template gebruikt.
        - De juiste reservering wordt bijgewerkt.
        """
        BottelingReserveringen.objects.create(
            voornaam='Jane',
            achternaam='Doe',
            e_mailadres='jane.doe@example.com',
            aantal_flessen=150,
            totaalprijs=15000.0
        )
        response = self.client.post(self.url, self.data)
        reservering = BottelingReserveringen.objects.get(e_mailadres=
                                                         'foo.bar@example.com')
        self.assertTrue(reservering.reserve)