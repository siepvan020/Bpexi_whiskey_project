# Third party imports
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from bokeh.plotting import figure, output_file, show
from django.db.models import Count
from django.contrib.auth.decorators import login_required

from hielander_whiskey_app.models import BottelingReserveringen
from hielander_whiskey_app.models import MasterclassReserveringen

# Local imports

@login_required
def dashboard_page(request: WSGIRequest) -> HttpResponse:
    Aant_botteling = BottelingReserveringen.objects.all().count
    # counts = MasterclassReserveringen.objects.values('sessie_nummer', 'masterclass').annotate(count=Count('id????'))
    # print(counts)

    toont1 = True
    # bottel_piechart()
    # masterclass_barplot()



    toont2 = True
    botteling = BottelingReserveringen.objects.all()
    masterclass = MasterclassReserveringen.objects.all()
    return render(request, 'dashboard.html', {
        'aantallen': Aant_botteling,
        'toont1': toont1,
        'toont2': toont2,
        'botteling': botteling,
        'masterclass': masterclass,
    })


def bottel_piechart():
    output_file("templates/bottel_piechart.html")
    graph = figure(title="Bottel Piechart")


    graph.wedge()
    pass


def masterclass_barplot():
    output_file("templates/masterclass_barplot.html")
    graph = figure(title="Masterclass Barplot")


    graph.vbar()
    pass

