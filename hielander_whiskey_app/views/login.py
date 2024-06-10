# Third party imports
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse


# Local imports


def try_log_in(request, gebruikersnaam, wachtwoord):
    """
    Probeert een gebruiker aan te melden. Deze functie probeert een gebruiker aan te melden met de opgegeven
    gebruikersnaam en wachtwoord. Als de aanmelding succesvol is, meldt het de gebruiker aan en wordt
    doorgestuurd naar de admin dashboard. Anders retourneert het None.

    Args:
        request: Een HttpRequest-object.
        gebruikersnaam: De gebruikersnaam van de gebruiker.
        wachtwoord: Het wachtwoord van de gebruiker.

    Returns:
        Een HttpResponseRedirect-object dat doorverwijst naar de admin dashboard als de aanmelding succesvol is, anders None.
    """
    user = authenticate(request, username=gebruikersnaam, password=wachtwoord)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('dashboard'))
    return None


def login_page(request: WSGIRequest) -> HttpResponse:
    if request.method == "POST":
        form = request.POST
        if form:
            gebruikersnaam = request.POST.get('gebruikersnaam')
            wachtwoord = request.POST.get('wachtwoord')
            return (try_log_in(request, gebruikersnaam, wachtwoord) or
                    render(request, "login.html",
                           {
                               "errors": "De gegeven gebruikersnaam en/of wachtwoord is onjuist!"}))
    else:
        pass
    return render(request, 'login.html')