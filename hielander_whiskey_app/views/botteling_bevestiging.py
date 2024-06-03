# Third party imports
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

# Local imports


def botteling_bevestiging_page(request: WSGIRequest) -> HttpResponse:
    return render(request, 'botteling_bevestiging.html')