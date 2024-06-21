# Third party imports
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
from django.contrib.auth.decorators import login_required
from django.conf import settings

import plotly.graph_objs as go
import plotly.io as pio

import os

# Local imports
from hielander_whiskey_app.models import BottelingReserveringen
from hielander_whiskey_app.models import MasterclassReserveringen
from hielander_whiskey_app.models import FestivalData


@login_required
def dashboard_page(request: WSGIRequest) -> HttpResponse:

    if request.method == 'POST':

        for item in FestivalData.objects.all():
            item_id = item.id

            # Stop POST data in variabelen
            naam_value = request.POST.get(f'naam_{item_id}')
            tijd_value = request.POST.get(f'tijd_{item_id}')
            datum_value = request.POST.get(f'datum_{item_id}')
            aantal_value = request.POST.get(f'aantal_beschikbaar_{item_id}')
            prijs_value = request.POST.get(f'prijs_{item_id}')

            # Update item met nieuwe data
            item.naam = naam_value if naam_value else item.naam
            item.tijd = tijd_value if tijd_value else item.tijd
            item.datum = datum_value if datum_value else item.datum
            item.aantal_beschikbaar = aantal_value \
                if aantal_value else item.aantal_beschikbaar
            item.prijs = prijs_value if prijs_value else item.prijs
            
            item.save()

    templijst = list(FestivalData.objects.values_list('type', 'sessie', 'aantal_beschikbaar'))
    templijst.pop(0)
    tempdict = dict()
    for i in templijst:
        tempdict[i[0]] = [i[0], f"sessie {i[1]}", 0, i[2]]

    totaal_flessen = BottelingReserveringen.objects.aggregate(
        totaal_flessen=Coalesce(Sum('aantal_flessen'), Value(0))
    )['totaal_flessen']
    max_flessen = FestivalData.objects.get(type="botteling").aantal_beschikbaar
    fles_naam = FestivalData.objects.get(type="botteling").naam
    tempdict[fles_naam] = [fles_naam, "n.v.t.", totaal_flessen, max_flessen]

    counts = MasterclassReserveringen.objects.values('masterclass', 'sessie_nummer').annotate(
        totaal_kaarten=Sum('aantal_kaarten'))

    for row in counts:
        max_kaarten = FestivalData.objects.get(type=f"{row['masterclass']}").aantal_beschikbaar
        tempdict[row['masterclass']] = [row['masterclass'], f"sessie {row['sessie_nummer']}", row['totaal_kaarten'], max_kaarten]


    aantallen = list(tempdict.values())


    bottel_piechart(totaal_flessen, max_flessen)
    masterclass_barplot(aantallen)


    botteling = BottelingReserveringen.objects.all()
    masterclass = MasterclassReserveringen.objects.all()
    festivaldata = FestivalData.objects.all()
    for data in festivaldata:
        data.type = data.type.capitalize()
    
    return render(request, 'dashboard.html', {
        'aantallen': aantallen,
        'botteling': botteling,
        'masterclass': masterclass,
        'festivaldata': festivaldata
    })


def bottel_piechart(aantal_reserv: int, max_flessen: int):
    labels = ['Gereserveerd', 'Beschikbaar']
    values = [aantal_reserv, (max_flessen-aantal_reserv)]

    layout = go.Layout(autosize=False, width=625, height=500)

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)], layout=layout)

    templates_dir = os.path.join(settings.BASE_DIR, 'hielander_whiskey_app', 'templates', 'plots')
    save_path = os.path.join(templates_dir, 'bottel_piechart.html')
    pio.write_html(fig, file=save_path, auto_open=False, config={'displayModeBar': False})


def masterclass_barplot(aantallen: list):
    aantallen_m = aantallen[:-1]
    counter = 0
    x = []
    y = []
    for i in aantallen_m:
        x.append(aantallen_m[counter][0])
        y.append(aantallen_m[counter][2])
        counter += 1
    layout = go.Layout(autosize=False, width=625, height=500)
    fig = go.Figure([go.Bar(x=x, y=y)], layout=layout)

    templates_dir = os.path.join(settings.BASE_DIR, 'hielander_whiskey_app', 'templates', 'plots')
    save_path = os.path.join(templates_dir, 'masterclass_barchart.html')
    fig.write_html(file=save_path, auto_open=False, config={'displayModeBar': False})