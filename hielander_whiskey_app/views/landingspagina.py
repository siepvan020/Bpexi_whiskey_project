from django.shortcuts import render


def landingspagina(request):
    """ Landingspagina view
    Dit is de landingspagina van het ticketsysteem. Het wordt niet verwacht dat de gebruiker hier zal komen,
    maar deze pagina bestaat zodat de gebruiker niet gelijk een 404 krijgt op het moment dat de applicatie gestart wordt.

    :param request: Het HTTP-verzoek dat is gegeven.
    :type request: HttpRequest
    :return: De HTTP response dat wordt gereturned.
    :rtype: HttpResponse
    """
    return render(request, 'landingspagina.html')
