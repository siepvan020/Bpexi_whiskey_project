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
    max_flessen = FestivalData.objects.get(type="botteling").aantal_beschikbaar
    fles_naam = FestivalData.objects.get(type="botteling").naam

    fles_line = f"{totaal_flessen}/{max_flessen} van de {fles_naam} gereserveerd"
    aantallen.append(fles_line)

    # counts = MasterclassReserveringen.objects.values('masterclass', 'sessie_nummer').annotate(totaal_kaarten=Sum('aantal_kaarten'))

    # for row in counts:
        # max_flessen = FestivalData.objects.get(type=f"botteling").aantal_beschikbaar
        # print(f"{row['totaal_kaarten']}/{max_flessen} van de {row['masterclass']} sessie {row['sessie_nummer']}")


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