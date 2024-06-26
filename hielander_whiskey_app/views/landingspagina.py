from django.shortcuts import render


def landingspagina(request):
    return render(request, 'landingspagina.html')
