# Third party imports
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

# Local imports
from hielander_whiskey_app.models import BottelingReserveringen
from hielander_whiskey_app.forms import BottelingReserveringenForm


def botteling_reservering_page(request: WSGIRequest) -> HttpResponse:
    if request.method == 'POST':

        # Form valideren
        form = BottelingReserveringenForm(request.POST)

        if form.is_valid():
            reservering = form.save(commit=False)
            reservering.totaalprijs = reservering.aantal_flessen * 50
            reservering.save()
            print(f'Reservering "{reservering}" opgeslagen')

            return HttpResponseRedirect(reverse('botteling_bevestiging'))
            
        else:
            print('Reservering niet correct/form ongeldig')
            if 'e_mailadres' in form.errors:
                messages.error(request, 'E-mailadres is niet correct')
            else:
                messages.error(request, 'Reservering niet correct')



    return render(request, 'botteling_reservering.html')