# Third party imports
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

# Local imports


def masterclass_bevestiging_page(request: WSGIRequest) -> HttpResponse:
    """
    Deze functie zorgt ervoor dat de pagina
    'masterclass_bevestiging.html' wordt geladen.

    :param request: Het HTTP request object.
    :type request: WSGIRequest
    :return: Het HTTPResponse object dat de pagina rendert.
    :rtype: HttpResponse
    """
    return render(request, 'masterclass_bevestiging.html')