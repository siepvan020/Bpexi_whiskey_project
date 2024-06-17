# Third party imports
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.db.models import Sum

# Local imports
from hielander_whiskey_app.models import BottelingReserveringen
from hielander_whiskey_app.models import FestivalData
from hielander_whiskey_app.forms import BottelingReserveringenForm

def botteling_reservering_page(request: WSGIRequest) -> HttpResponse:

    totaal_flessen = BottelingReserveringen.objects.aggregate(
                totaal_flessen=Sum('aantal_flessen'))['totaal_flessen']

    context = {}

    # Het maximaal aantal te reserveren flessen wordt hier bepaald.
    # Als er geen flessen meer over zijn, kan de gebruiker op de
    # reservelijst maximaal 10 flessen selecteren.
    if totaal_flessen and 150 - totaal_flessen > 0: # Flessen over
        context['flessen_over'] = 150 - totaal_flessen
    elif totaal_flessen is None:    # Nog geen reserveringen
        context['flessen_over'] = 150
    elif 150 - totaal_flessen <= 0: # Geen flessen meer beschikbaar
        context['flessen_over'] = None

    context['fles'] = FestivalData.objects.get(pk=1) # nog updaten! pk -> type

    if request.method == 'POST':
        # Form valideren
        form = BottelingReserveringenForm(request.POST)

        if form.is_valid():
            reservering = form.save(commit=False)
            # Berekening totaalprijs: aantal flessen * prijs per fles 
            reservering.totaalprijs = reservering.aantal_flessen * \
                FestivalData.objects.get(pk=1).prijs # nog updaten! pk -> type
            
            if totaal_flessen:
                # Aantal flessen over na de reservering
                na_reserv = 150 - totaal_flessen - reservering.aantal_flessen

                if na_reserv < 0:
                    reservering.reserve = True

            reservering.save()
            print(f'Reservering "{reservering}" opgeslagen')

            return HttpResponseRedirect(reverse('botteling_bevestiging'))
            
        else:
            print('Reservering niet correct/form ongeldig')
            if 'e_mailadres' in form.errors:
                messages.error(request, 'E-mailadres is niet correct')
            else:
                messages.error(request, 'Reservering niet correct')

    return render(request, 'botteling_reservering.html', context)