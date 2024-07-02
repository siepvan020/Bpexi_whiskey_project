# Third party imports
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.db.models import Sum
from datetime import date
from typing import Union

# Local imports
from hielander_whiskey_app.models import BottelingReserveringen
from hielander_whiskey_app.models import FestivalData
from hielander_whiskey_app.forms import BottelingReserveringenForm
from hielander_whiskey_app.models import FestivalData
from hielander_whiskey_app.utils.send_emails import setup_botteling_email


def botteling_reservering_page(request: WSGIRequest)\
                            -> Union[HttpResponse, HttpResponseRedirect]:


    totaal_flessen = BottelingReserveringen.objects.aggregate(
                totaal_flessen=Sum('aantal_flessen'))['totaal_flessen']
    beschikbaar = FestivalData.objects.get(type='botteling').aantal_beschikbaar

    context = {}

    # Het maximaal aantal te reserveren flessen wordt hier bepaald.
    # Als er geen flessen meer over zijn, kan de gebruiker op de
    # reservelijst maximaal 10 flessen selecteren.
    if totaal_flessen and beschikbaar - totaal_flessen > 0: # Flessen over
        context['flessen_over'] = beschikbaar - totaal_flessen
    elif totaal_flessen is None:    # Nog geen reserveringen
        context['flessen_over'] = beschikbaar
    elif beschikbaar - totaal_flessen <= 0: # Geen flessen meer beschikbaar
        context['flessen_over'] = None

    context['fles'] = FestivalData.objects.get(type='botteling')

    if request.method == 'POST':
        # Form valideren
        form = BottelingReserveringenForm(request.POST)

        if form.is_valid():
            reservering = form.save(commit=False)
            print(reservering.opmerking)

            # Check of het e-mailadres al 2 flessen heeft gereserveerd
            bestaande_reserveringen = BottelingReserveringen.objects.filter(
                e_mailadres=reservering.e_mailadres)
            
            totaal_flessen_op_email = sum(
                res.aantal_flessen for res in bestaande_reserveringen)

            if totaal_flessen_op_email + reservering.aantal_flessen > 2:
                messages.error(request, 'Kan niet meer dan\
                                2 flessen per persoon reserveren')
                
                return HttpResponseRedirect(reverse('botteling_reservering'))
            
            else:

                fles_prijs = FestivalData.objects.get(type='botteling').prijs

                # Berekening totaalprijs: aantal flessen * prijs per fles 
                reservering.totaalprijs = reservering.aantal_flessen * fles_prijs
                email_totaalprijs = f'{reservering.totaalprijs:.2f}'.replace('.', ',')
                
                if totaal_flessen:
                    # Aantal flessen over na de reservering
                    na_reserv = beschikbaar - \
                                totaal_flessen - \
                                reservering.aantal_flessen

                    if na_reserv < 0:
                        reservering.reserve = True

                tussenvoegsel = reservering.tussenvoegsel if\
                    reservering.tussenvoegsel else ''
                
                reservering.save()

                setup_botteling_email(f'{reservering.voornaam} \
                                    {tussenvoegsel} \
                                    {reservering.achternaam}', 
                                    reservering.e_mailadres, 
                                    date.today(), 
                                    reservering.aantal_flessen, 
                                    email_totaalprijs,)

                print(f'Reservering "{reservering}" opgeslagen')
                context['reservering'] = reservering
                context['email_totaalprijs'] = email_totaalprijs

                return render(request, 'botteling_bevestiging.html', context)
            
        else:
            print('Reservering niet correct/form ongeldig')
            if 'e_mailadres' in form.errors:
                messages.error(request, 'E-mailadres is niet correct')
            else:
                messages.error(request, 'Reservering niet correct')
    
    
    
    return render(request, 'botteling_reservering.html', context)