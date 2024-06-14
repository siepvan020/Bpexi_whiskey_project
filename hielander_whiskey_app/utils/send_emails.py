# Third party imports
from datetime import datetime

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Local imports
from hielander_whiskey_app.models import FestivalData


def stuur_botteling_email(volledige_naam: str, 
                          ontvanger_email: str, 
                          datum: datetime.date, 
                          aantal_flessen: int, 
                          totaalprijs: str
                          ):

    betaal_datum = datum + datetime.timedelta(days=14)
    naam_fles = FestivalData.objects.get(pk=1).naam

    context = {
        'volledige_naam': volledige_naam,
        'factuur_datum': datum,
        'betaal_datum': betaal_datum,
        'aantal_flessen': aantal_flessen,
        'totaalprijs': totaalprijs,
        'naam_fles': naam_fles,
    }

    html_content = render_to_string('email_templates/botteling_email.html', context)
    
    plain_message = strip_tags(html_content)
    
    send_mail(
        subject='HWF - Festival Botteling Factuur',
        message=plain_message,
        from_email='nog niet bestaand',
        recipient_list=[ontvanger_email],
        fail_silently=False,
    )
    


def stuur_masterclass_email(volledige_naam: str, 
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

    html_content = render_to_string('email_templates/masterclass_email.html', context)
    
    plain_message = strip_tags(html_content)

    send_mail(
        subject='HWF - Masterclass Factuur',
        message=plain_message,
        from_email='nog niet bestaand',
        recipient_list=[ontvanger_email],
        fail_silently=False,
    )
    