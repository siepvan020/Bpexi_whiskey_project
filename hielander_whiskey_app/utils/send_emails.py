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

    betaal_datum = datum + timedelta(days=14)
    naam_fles = FestivalData.objects.get(type='botteling').naam
    print(naam_fles)

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
    subject = 'HWF - Festival Masterclass Factuur'

    stuur_email(plain_message, html_content, ontvanger_email, subject)


def stuur_email(plain_message: str, 
                html_content: SafeString, 
                ontvanger_email: str,
                subject: str):

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