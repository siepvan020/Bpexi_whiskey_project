# Third party imports
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

# Local imports
from hielander_whiskey_app.models import BottelingReserveringen
from hielander_whiskey_app.forms import BottelingReserveringenForm


def botteling_reservering_page(request: WSGIRequest) -> HttpResponse:
    if request.method == 'POST':

        # Form valideren
        form = BottelingReserveringenForm(request.POST)

        if form.is_valid():
            form.save(commit=False)
            print(form.cleaned_data)
            print(form.errors)


    return render(request, 'botteling_reservering.html')