# Third party imports
from datetime import datetime, timedelta
from unittest.mock import patch
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django_pony_express.services.tests import EmailTestService

# Local imports
from hielander_whiskey_app.models import FestivalData, MasterclassReserveringen


class TestMasterclassReserveringPage(TestCase):
    """
    Test class voor de masterclass reserveringspagina.
    Erft over van TestCase.

    Overzicht van de testcases in deze klasse:
    1. test_get_request: Test het uitvoeren van een GET-request naar de reserveringspagina.
    2. test_post_valid_form: Test het submitten van valid data via een POST request naar de reserveringspagina.
    3. test_post_lege_voornaam: Test het submitten van invalid data met een lege voornaam via een POST request naar de reserveringspagina.
    4. test_post_lege_achternaam: Test het submitten van data met een lege achternaam via een POST request naar de reserveringspagina.
    5. test_post_foute_email: Test het submitten van data met een ongeldig e-mailadres via een POST request naar de reserveringspagina.
    6. test_email_gestuurd: Test het sturen/ontvangen van een e-mail na het invullen van een valid form.

    """

    def setUp(self):
        """
        Setup methode wordt uitgevoerd voor elke testcase.
        Initialiseert de testclient en de URL van de reserveringspagina.
        Maakt een dummy instantie van FestivalData aan (omdat de eerste wordt geskipt) en een instantie waarmee wordt getest.
        Pre-defined een instance van MasterclassReserveringen om te gebruiken in de testcases.

        """
        self.client = Client()
        self.url = reverse('masterclass_reservering')
        self.email_test_service = EmailTestService()

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
            tijd=datetime.now().time(),
            sessie=1,
            datum=datetime.now().date(),
            aantal_beschikbaar=30,
            prijs=15.0
        )

        self.data = {
            'voornaam': 'Foo',
            'tussenvoegsel': '',
            'achternaam': 'Bar',
            'e_mailadres': 'foo.bar@example.com',
            'opmerking': '',
            'sessie_nummer': 1,
            'masterclass': 'masterclass 1',
            'aantal_kaarten': 2    
        }


    def test_get_request(self):
        """
        Testcase voor het uitvoeren van een GET-request naar de reserveringspagina.
        Controleert of de response:
        - Valid context heeft
        - Een statuscode van 200 heeft
        - De goede template gebruikt
        - De juiste masterclass prijs bevat.
        """
        response = self.client.get(self.url)
        self.assertIsNotNone(response.context)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'masterclass_reservering.html')
        self.assertIn('masterclass_prijzen', response.context)
        self.assertEqual(response.context['masterclass_prijzen'], {'masterclass 1': 15.0})


    @patch('hielander_whiskey_app.views.masterclass_reservering.setup_masterclass_email')
    def test_post_valid_form(self, mock_send_email):
        """
        Test of het verzenden van een geldig formulier een succesvolle POST-request oplevert.

        Deze functie simuleert het verzenden van een POST request naar de URL van de masterclass reservering view met valid data.
        Het controleert of de response:
        - Een status code van 200 heeft
        - De juiste template gebruikt
        - Een nieuwe reservering aanmaakt
        Daarnaast wordt gecontroleerd of de totaalprijs van de reservering correct is en of de functie setup_masterclass_email wordt aangeroepen.

        :param mock_send_email: Een mock object voor de functie setup_masterclass_email
        """
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'masterclass_bevestiging.html')
        self.assertEqual(MasterclassReserveringen.objects.count(), 1)
        reservation = MasterclassReserveringen.objects.first()
        self.assertEqual(reservation.totaalprijs, 30)
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
        self.assertTemplateUsed(response, 'masterclass_reservering.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.message == 'Reservering niet correct' for message in messages))

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
        self.assertTemplateUsed(response, 'masterclass_reservering.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.message == 'Reservering niet correct' for message in messages))

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
        self.assertTemplateUsed(response, 'masterclass_reservering.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.message == 'E-mailadres is niet correct' for message in messages))

    def test_email_gestuurd(self):
        """
        Testcase voor het sturen/ontvangen van een e-mail na het invullen van een valid form.
        Controleert of de email:
        - Naar het juiste e-mailadres is gestuurd.
        - Één keer is verstuurd.
        - Het juiste onderwerp heeft.
        """
        factuurdatum = datetime.now().date() + timedelta(days=14)

        response = self.client.post(self.url, self.data)
        self.email_test_service.filter(to='foo.bar@example.com'
                                       ).assert_quantity(1)
        self.email_test_service.filter(to='foo.bar@example.com'
                                       )[0].assert_subject(
                                           'HWF - Festival Masterclass Factuur')