# Third party imports
from datetime import datetime, timedelta
from email.mime.image import MIMEImage

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.staticfiles import finders
from django.utils.safestring import SafeString

# Local imports
from hielander_whiskey_app.models import FestivalData


def setup_botteling_email(volledige_naam: str, 
                          ontvanger_email: str, 
                          datum: datetime.date, 
                          aantal_flessen: int, 
                          totaalprijs: str
                          ):
    """Maakt de e-mail voor een botteling reservering klaar.

    Deze functie bepaalt hier eerst de uiterste betaaldatum door +14 dagen 
    bij de factuurdatum op te tellen. Vervolgens wordt de e-mail opgesteld
    met de juiste gegevens en wordt de stuur_email functie aangeroepen.

    - De uiterste betaaldatum kan worden aangepast op regel 42.
    - Het onderwerp van de e-mail kan worden aangepast op regel 61.

    :param volledige_naam: De volledige naam van de ontvanger
    :type volledige_naam: str
    :param ontvanger_email: Het e-mailadres van de ontvanger
    :type ontvanger_email: str
    :param datum: De datum van de factuur
    :type datum: datetime.date
    :param aantal_flessen: Het aantal gereserveerde flessen
    :type aantal_flessen: int
    :param totaalprijs: De totaalprijs van de bestelling
    :type totaalprijs: str
    """

    # Pas hier de uiterste betaaldatum aan!!
    betaal_datum = datum + timedelta(days=14)
    naam_fles = FestivalData.objects.get(type='botteling').naam

    context = {
        'volledige_naam': volledige_naam,
        'factuur_datum': datum,
        'betaal_datum': betaal_datum,
        'aantal_flessen': aantal_flessen,
        'totaalprijs': totaalprijs,
        'naam_fles': naam_fles,
    }

    html_content = render_to_string('email_templates/botteling_email.html', 
                                    context)
    
    plain_message = strip_tags(html_content)

    # Pas hier het onderwerp van de e-mail aan
    subject = 'HWF - Festival Botteling Factuur'
    
    stuur_email(plain_message, html_content, ontvanger_email, subject)


def setup_masterclass_email(volledige_naam: str, 
                            ontvanger_email: str, 
                            datum: datetime.date, 
                            mc_naam: str, 
                            sessie: int, 
                            mc_tijd: datetime.time, 
                            mc_prijs: float, 
                            aantal_tickets: int, 
                            totaalprijs: float
                            ):
    """Maakt de e-mail voor een masterclass reservering klaar.

    De email wordt opgesteld met de juiste gegevens de functie stuur_email wordt aangeroepen.

    - De uiterste betaaldatum kan worden aangepast in het bestand "masterclass_email.html" op regel 77.
    - Het onderwerp van de e-mail kan worden aangepast op regel 120.

    :param volledige_naam: De volledige naam van de ontvanger
    :type volledige_naam: str
    :param ontvanger_email: Het e-mailadres van de ontvanger
    :type ontvanger_email: str
    :param datum: De datum van de factuur
    :type datum: datetime.date
    :param mc_naam: De naam van de masterclass
    :type mc_naam: str
    :param sessie: Het sessienummer van de masterclass
    :type sessie: int
    :param mc_tijd: De tijd van de masterclass
    :type mc_tijd: datetime.time
    :param mc_prijs: De prijs van de masterclass
    :type mc_prijs: float
    :param aantal_tickets: Het aantal gereserveerde tickets
    :type aantal_tickets: int
    :param totaalprijs: De totaalprijs van de bestelling
    :type totaalprijs: float
    """

    context = {
        'volledige_naam': volledige_naam,
        'factuur_datum': datum,
        'mc_naam': mc_naam,
        'sessie': sessie,
        'mc_tijd': mc_tijd,
        'mc_prijs': mc_prijs,
        'aantal_tickets': aantal_tickets,
        'totaalprijs': totaalprijs,
        }

    html_content = render_to_string('email_templates/masterclass_email.html', 
                                    context)
    
    plain_message = strip_tags(html_content)

    # Pas hier het onderwerp van de e-mail aan
    subject = 'HWF - Festival Masterclass Factuur'

    stuur_email(plain_message, html_content, ontvanger_email, subject)


def stuur_email(plain_message: str, 
                html_content: SafeString, 
                ontvanger_email: str,
                subject: str):
    """Verstuurt de bevestigings email.

    Deze functie krijgt de informatie die nodig is om een e-mail te sturen met Django.
    Voegt nog 3 afbeeldingen toe aan de e-mail en stuurt deze vervolgens naar de ontvanger.

    :param plain_message: De plain text inhoud van de e-mail
    :type plain_message: str
    :param html_content: De HTML-inhoud van de e-mail
    :type html_content: SafeString
    :param ontvanger_email: Het e-mailadres van de ontvanger
    :type ontvanger_email: str
    :param subject: Het onderwerp van de e-mail
    :type subject: str
    """

    # Hier verzender e-mailadres handmatig aanpassen
    msg = EmailMultiAlternatives(
        subject= subject,
        body=plain_message,
        from_email='hwf.djangotest@gmail.com', # !Hier!
        to=[ontvanger_email]
    )

    msg.attach_alternative(html_content, "text/html") 
    
    image_paths = {
        'website.png': 'img/img_email/website.png',
        'email.png': 'img/img_email/email.png',
        'card.png': 'img/img_email/card.png'
    }

    for cid, static_path in image_paths.items():
        absolute_path = finders.find(static_path)
        if absolute_path:
            with open(absolute_path, 'rb') as img:
                mime_image = MIMEImage(img.read())
                mime_image.add_header('Content-ID', f'<{cid}>')
                mime_image.add_header('Content-Disposition', 'inline', filename=cid)
                msg.attach(mime_image)
        else:
            print(f'Path not found: {static_path}')
    
    msg.send()