# Third party imports
from datetime import timedelta

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Local imports
from hielander_whiskey_app.models import FestivalData


def stuur_botteling_email(volledige_naam, ontvanger_email, datum, aantal_flessen, totaalprijs):
    betaal_datum = datum + timedelta(days=14)
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
    


def stuur_masterclass_email(voornaam, tussenv, achternaam, ontvanger_email, datum, mc_naam, sessie, mc_tijd, mc_prijs, aantal_tickets, totaalprijs):

    context = {
        'volledige_naam': f'{voornaam} {tussenv} {achternaam}',
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
    