# Third party imports
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json

import plotly.graph_objs as go
import plotly.io as pio

import os

# Local imports
from hielander_whiskey_app.models import BottelingReserveringen
from hielander_whiskey_app.models import MasterclassReserveringen
from hielander_whiskey_app.models import FestivalData


@login_required
def dashboard_page(request: WSGIRequest) -> HttpResponse:
    """Deze functie haalt alle benodigde variabelen en data op en roept bottel_piechart en masterclass_barchart
    aan. Vervolgens rendert deze functie de dashboard pagina.

    :param request: Een HttpRequest-object.
    :type request: HttpRequest
    :return: Een render-object dat de admin dashboard toont nadat succesvol ingelogd is.
    :rtype: render
    """

    if request.method == 'POST':
        update_success = True

        for item in FestivalData.objects.all():
            item_id = item.id

            # Stop POST data in variabelen
            naam_value = request.POST.get(f'naam_{item_id}')
            tijd_value = request.POST.get(f'tijd_{item_id}')
            datum_value = request.POST.get(f'datum_{item_id}')
            aantal_value = request.POST.get(f'aantal_beschikbaar_{item_id}')
            prijs_value = request.POST.get(f'prijs_{item_id}')

            try:
                # Update item met nieuwe data
                item.naam = naam_value if naam_value else item.naam
                item.tijd = tijd_value if tijd_value else item.tijd
                item.datum = datum_value if datum_value else item.datum
                item.aantal_beschikbaar = aantal_value \
                    if aantal_value else item.aantal_beschikbaar
                item.prijs = prijs_value if prijs_value else item.prijs
                
                item.save()
            except ValueError as e:
                messages.error(request, 
                               f"Value error voor {item.type}: {e}")
                update_success = False
            except Exception as e:
                messages.error(request, 
                               f"Error bij het updaten van {item.type}: {e}")
                update_success = False
        
        if update_success:
            messages.success(request, "Festival Data succesvol geüpdatet!")

    # Haalt alle waardes uit festivaldata op.
    templijst = list(FestivalData.objects.values_list('type', 'sessie', 'aantal_beschikbaar'))
    templijst.pop(0)
    tempdict = dict()
    for i in templijst:
        tempdict[i[0]] = [i[0], f"{i[1]}", 0, i[2]]

    # Berekent het totaal aantal gereserveerde flessen.
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
        tempdict[row['masterclass']] = [row['masterclass'], f"{row['sessie_nummer']}", row['totaal_kaarten'], max_kaarten]


    aantallen = list(tempdict.values())

    # Roept de plot functies aan.
    bottel_piechart(totaal_flessen, max_flessen)
    masterclass_barplot(aantallen)

    # Haalt de volledige databases op voor gebruik in tabellen op de dashboard pagina.
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
    """Gebruikt het aantal gereserveerde flessen en het maximaal aantal beschikbare flessen om eenpiechart
    te genereren. Deze wordt vervolgens als html bestand opgeslagen in de plots folder in templates.

    :param aantal_reserv: Het aantal gereserveerde flessen.
    :type aantal_reserv: int
    :param max_flessen: Het maximaal aantal flessen.
    :type max_flessen: int
    """
    labels = ['Gereserveerd', 'Beschikbaar']
    values = [aantal_reserv, (max_flessen-aantal_reserv)]

    layout = go.Layout(autosize=False, width=625, height=500)
    kleurtjes = ['#9c7731', '#242363']

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=kleurtjes))], layout=layout)

    # slaat de plot als html op in de plots folder in templates
    templates_dir = os.path.join(settings.BASE_DIR, 'hielander_whiskey_app', 'templates', 'plots')
    save_path = os.path.join(templates_dir, 'bottel_piechart.html')
    pio.write_html(fig, file=save_path, auto_open=False, config={'displayModeBar': False})


def masterclass_barplot(aantallen: list):
    """Gebruikt de lijst met aantallen van verkochte tickets van de masterclasses om een barplot te genereren.
    Deze barplot wordt vervolgens als html bestand opgeslagen in de plots folder in templates.

    :param aantallen: Een lijst met de aantallen tickets per masterclass.
    :type aantallen: list
    """
    aantallen_m = aantallen[:-1]
    counter = 0
    x = []
    y = []
    for i in aantallen_m:
        x.append(aantallen_m[counter][0])
        y.append(aantallen_m[counter][2])
        counter += 1
    layout = go.Layout(autosize=False, width=625, height=500, dragmode=False)
    kleurtjes = ['#9c7731', '#242363', '#9c7731', '#242363', '#9c7731', '#242363', '#9c7731', '#242363']
    fig = go.Figure([go.Bar(x=x, y=y, marker=dict(color=kleurtjes))], layout=layout)

    # slaat de plot als html op in de plots folder in templates
    templates_dir = os.path.join(settings.BASE_DIR, 'hielander_whiskey_app', 'templates', 'plots')
    save_path = os.path.join(templates_dir, 'masterclass_barchart.html')
    fig.write_html(file=save_path, auto_open=False, config={'displayModeBar': False})


@csrf_exempt
def delete_rij(request):
    """Verwijdert rijen uit de database met behulp van de bijbehorende functies in dashboard.js.


    :param request: Een HttpRequest-object.
    :type request: HttpRequest
    :return: Een JsonResponse-object mey hierin: False en een error message als er iets fout gaat, anders True.
    :rtype: JsonResponse
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ids = data.get('ids', [])
            type = data.get('type')
            if not ids:
                return JsonResponse({'success': False, 'error': 'No IDs provided'})
            if type == 'botteling':
                BottelingReserveringen.objects.filter(id__in=ids).delete()
            elif type == 'masterclass':
                MasterclassReserveringen.objects.filter(id__in=ids).delete()
            else:
                return JsonResponse({'success': False, 'error': 'Invalid type'})
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})