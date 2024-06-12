# Third party imports
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib import messages

# Local imports
from hielander_whiskey_app.models import MasterclassReserveringen
from hielander_whiskey_app.forms import MasterclassReserveringenForm


def masterclass_reservering_page(request: WSGIRequest) -> HttpResponse:
    if request.method == 'POST':
        form = MasterclassReserveringenForm(request.POST)
        if form.is_valid():
            reservering = form.save(commit=False)
            reservering.save()
            print(f'Reservering "{reservering}" opgeslagen')

            return HttpResponseRedirect(reverse('masterclass_bevestiging'))
        else:
            print('Reservering niet correct/form ongeldig')
            if 'e_mailadres' in form.errors:
                messages.error(request, 'E-mailadres is niet correct')
            else:
                messages.error(request, 'Reservering niet correct')

    return render(request, 'masterclass_reservering.html')