# Third party imports
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib import messages
from datetime import date

# Local imports
from hielander_whiskey_app.models import MasterclassReserveringen
from hielander_whiskey_app.forms import MasterclassReserveringenForm
from hielander_whiskey_app.models import FestivalData
from hielander_whiskey_app.utils.send_emails import setup_masterclass_email

def masterclass_reservering_page(request: WSGIRequest) -> HttpResponse:
    context = {}
    templijst = dict(FestivalData.objects.values_list('type', 'prijs')[1:])
    context['masterclass_prijzen'] = templijst
    templijst = dict(FestivalData.objects.values_list('type', 'aantal_beschikbaar')[1:])
    for masterclass in templijst.keys():
        for reservering in MasterclassReserveringen.objects.all():
            if reservering.masterclass == masterclass:
                templijst[masterclass] -= reservering.aantal_kaarten
                if templijst[masterclass] == 0:
                    templijst[masterclass] = 0
    context['kaarten_beschikbaar'] = templijst
    templijst = dict(FestivalData.objects.values_list('type', 'naam')[1:])
    context['masterclass_naam'] = templijst
    templijst = dict(FestivalData.objects.values_list('type', 'tijd')[1:])
    for masterclass in templijst.keys():
        templijst[masterclass] = str(templijst[masterclass])[:5]
    context['masterclass_tijd'] = templijst

    if request.method == 'POST':
        form = MasterclassReserveringenForm(request.POST)
        if form.is_valid():
            reservering = form.save(commit=False)
            reservering.totaalprijs = reservering.aantal_kaarten * 15
            masterclass_reserveringen = MasterclassReserveringen.objects.all()
            totaal_aantal_kaarten = 0
            for res in masterclass_reserveringen:
                if res.masterclass == reservering.masterclass:
                    totaal_aantal_kaarten += res.aantal_kaarten
            if totaal_aantal_kaarten >= 30:
                reservering.reserve = True
            tussenvoegsel = reservering.tussenvoegsel if \
                reservering.tussenvoegsel else ''
            reservering.save()
            print(f'Reservering "{reservering}" opgeslagen')

            templijst = FestivalData.objects.all()[1:]
            masterclass_prijs = 0
            for masterclass in templijst:
                if masterclass.type == reservering.masterclass:
                    masterclass_prijs = masterclass.prijs
                    setup_masterclass_email(f'{reservering.voornaam} \
                                                                                      {tussenvoegsel} \
                                                                                      {reservering.achternaam}',
                                            reservering.e_mailadres,
                                            date.today(),
                                            masterclass.naam,
                                            masterclass.sessie,
                                            masterclass.tijd,
                                            masterclass.prijs,
                                            reservering.aantal_kaarten,
                                            reservering.totaalprijs, )
                    print('email verstuurd!')

            return render(request,'masterclass_bevestiging.html', {
                'naam': f'{reservering.voornaam} {tussenvoegsel} {reservering.achternaam}',
                'mail': reservering.e_mailadres,
                'masterclass': masterclass.naam,
                'prijs': masterclass_prijs,
                'aantal_kaarten': reservering.aantal_kaarten,
                'totaalprijs': reservering.totaalprijs
            })
        else:
            print('Reservering niet correct/form ongeldig')
            if 'e_mailadres' in form.errors:
                messages.error(request, 'E-mailadres is niet correct')
            else:
                messages.error(request, 'Reservering niet correct')

    return render(request, 'masterclass_reservering.html', context)