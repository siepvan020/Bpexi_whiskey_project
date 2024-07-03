# Third party imports
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

# Local imports


def botteling_bevestiging_page(request: WSGIRequest) -> HttpResponse:
    """Botteling bevestiging view
    Rendert de botteling bevestigingspagina.

    :param request: De HTTP request dat wordt gebruikt voor de view.
    :type request: WSGIRequest
    :return: Het HTTP response object dat wordt gebruikt om de pagina te renderen.
    :rtype: HttpResponse
    """
    return render(request, 'botteling_bevestiging.html')