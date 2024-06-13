# Third party imports
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Count, Sum
from django.contrib.auth.decorators import login_required
from django.conf import settings

import plotly.graph_objs as go
import plotly.io as pio

import os

from hielander_whiskey_app.models import BottelingReserveringen
from hielander_whiskey_app.models import MasterclassReserveringen
from hielander_whiskey_app.models import FestivalData

# Local imports


# @login_required
def dashboard_page(request: WSGIRequest) -> HttpResponse:
    aantallen = []
    totaal_flessen = BottelingReserveringen.objects.aggregate(totaal_flessen=Sum('aantal_flessen'))['totaal_flessen']
    max_flessen = FestivalData.objects.get(naam="Ardmore (Ardlair) 2014 57.5%").aantal_beschikbaar # deze naam staat er momenteel hardcoded in omdat er geen andere manier is om dit te koppelen. Dit is een probleem in onze "erd". Dit geld voor flessen als masterclasses.
    fles_naam = FestivalData.objects.get(naam="Ardmore (Ardlair) 2014 57.5%").naam # zelfde probleem als hierboven. Deze line is nu namelijk wel erg overbodig.

    fles_line = f"{totaal_flessen}/{max_flessen} van de {fles_naam} gereserveerd"
    aantallen.append(fles_line)

    # counts = MasterclassReserveringen.objects.values('sessie_nummer', 'masterclass').annotate(count=Count('id'))


    bottel_piechart(totaal_flessen, max_flessen)
    # masterclass_barplot()




    botteling = BottelingReserveringen.objects.all()
    masterclass = MasterclassReserveringen.objects.all()
    return render(request, 'dashboard.html', {
        'aantallen': aantallen,
        'botteling': botteling,
        'masterclass': masterclass,
    })


def bottel_piechart(aantal_reserv: int, max_flessen: int):
    labels = ['Gereserveerd', 'Beschikbaar']
    values = [aantal_reserv, (max_flessen-aantal_reserv)]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

    templates_dir = os.path.join(settings.BASE_DIR, 'hielander_whiskey_app', 'templates')
    save_path = os.path.join(templates_dir, 'bottel_piechart.html')
    pio.write_html(fig, file=save_path, auto_open=False)


def masterclass_barplot():
    pass