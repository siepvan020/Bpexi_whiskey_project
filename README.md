# Developer's guide - Hielander Whisky Festival Ticketsysteem

## Navigatie
- [Inleiding](#inleiding)
    - [Functie](#functie)
    - [Publiek](#publiek)
    - [Installatie en opstart instructies](#installatie-en-opstart-instructies)
- [Bestanden](#bestanden)
    - [Basisstructuur](#basisstructuur)
    - [Bestanden vinden](#bestanden-vinden)
        - [Static bestanden](#static-bestanden)
        - [Views](#views)
        - [Utils](#utils)
    - [Database modellen](#database-modellen)
- [Schermenoverzicht](#schermenoverzicht)
    - [Algemeen](#algemeen)
    - [Inlogscherm](#inlogscherm)
    - [Admin dashboard](#admin-dashboard)
    - [Masterclass reserveringen](#masterclass-reserveringen)
        - [Masterclass veranderen](#masterclasses-veranderen)
        - [Masterclass geselecteerd](#masterclass-geselecteerd)
        - [Totaalprijs updaten](#totaalprijs-updaten)
        - [Reservering geplaatst](#reservering-geplaatst)
    - [Masterclass bevestiging](#masterclass-bevestiging)
    - [Botteling reserveringen](#botteling-reserveringen)
    - [Botteling bevestiging](#botteling-bevestiging)
    - [Landingspagina](#landingspagina)
    - [E-mail templates](#e-mail-templates)
- [Unit testing](#unit-testing)
    - [Testing platform](#testing-platform)
    - [Unit tests runnen](#unit-tests-runnen)
    - [Toegang krijgen tot de unit tests](#toegang-krijgen-tot-de-unit-tests)
- [Development status](#development-status)
    - [Bugs](#bugs)
    - [Features in development](#features-in-development)


## Inleiding

### Functie
Momenteel worden de reserveringen voor de botteling en masterclasses handmatig afgehandeld via e-mail. De Hielander Whisky app is ontwikkeld om dit proces te vervangen. Op de reserveringspagina's kunnen klanten hun reserveringen plaatsen, waarna er automatisch e-mails worden verzonden met de details en de factuur. De applicatie biedt daarnaast de mogelijkheid om via de admin-dashboardpagina bestellingen en producten te beheren en te overzien. 

### Publiek
De botteling en masterclass pagina's zijn bedoeld voor klanten. Hier kunnen de klanten reserveringen maken. Vervolgens krijgen de klanten automatisch de mail waarin informatie over de bestelling en de factuur te vinden is. De admin-dashboardpagina is bedoeld voor de eigenaren. Hierin is informatie over alle gemaakt bestellingen te vinden. Ook kunnen hier gegevens van de huidige verkochte bottels en masterclasses aangepast worden. 

### Installatie en opstart instructies
Voor het gebruiken van de applicatie is python vereist. Als u nog geen python 3.11 geïnstalleerd heeft, volgt u de volgende stappen om python 3.11 te installeren: 

- Ga naar https://www.python.org/downloads/release/python-3119/  
- Scroll vervolgens naar beneden tot aan ‘Files’ 
- Druk vervolgens op ‘Windows installer(64-bit)’ 
- Open de gedownloade installer 
- Vink de optie ‘Add python.exe to PATH’ aan 
- Druk op de optie ‘Install Now’ 
- Wanneer de installatie compleet is kunt u dit venster sluiten 

Wanneer python geïnstalleerd is, kunt u de map waarin de applicatie staat openen. 

Type in de adresbalk van de map (de balk waarin staat waar in uw documenten u zich bevindt) het volgende commando:<br> 
`cmd` 

Vervolgens zullen we een virtuele omgeving aan moeten maken. Indien dit al is gedaan kunt u deze stap overslaan.  
Om een virtuele omgeving aan te maken, typt u het volgende commando:<br> 

`py -3.11 -m venv venv`  

Vervolgens moeten we de virtuele omgeving activeren. Afhankelijk van uw besturingssysteem moet dit met een ander commando gedaan worden. U kunt één van de volgende commando’s kiezen, passend bij uw besturingssysteem:<br> 
- Windows: `venv\scripts\activate` 
- Unix/Mac: `source venv/bin/activate` 

Wanneer de omgeving geactiveerd is, kunt u het laatste commando intypen om de vereiste bestanden te installeren. Dit doet u met het volgende commando:<br> 
`pip install -r requirements.txt` 

Als het installeren van de bestanden voltooid is kunt u de applicatie gebruiken met het volgende commando:<br> 
`python manage.py runserver` 

Dit commando zal ervoor zorgen dat de applicatie start. In uw browser kunt u vervolgens ‘http://127.0.0.1:8000/’ in de adresbalk invoeren om de applicatie te gebruiken. 


## Bestanden
### Basisstructuur
De HTML bestanden voor alle schermen kun je vinden in de map [`hielander_whiskey_app/templates/`](./hielander_whiskey_app/templates/). Tussen deze bestanden staat ook [`base.html`](./hielander_whiskey_app/templates/base.html). Hierin staat de basis HTML structuur, met onder andere een aantal installaties (font, jQuery, Tablesaw), de headerbalk en footerbalk. Ook  De [`base.html` wordt gebruikt om elementen te laden die op alle pagina's worden gebruikt, zoals de header. Deze maakt gebruik van Django template inheritance met blokken zoals `{% block content %}` en `{% block extrascripts %}`.

### Bestanden vinden
#### Static bestanden
De map [`hielander_whiskey_app/static/`](./hielander_whiskey_app/static/) bevat alle CSS, JavaScript en afbeeldingen die nodig zijn voor het gebruik van de applicatie. Deze static bestanden kunnen in templates worden gerefereerd met `{% static 'path/to/file' %}`.

#### Views
De bestanden die nodig zijn om de pagina's te laden (de views), bevinden zich in de map [`hielander_whiskey_app/views/`](./hielander_whiskey_app/views/), waarbij elk bestand de naam van de desbetreffende pagina heeft. Views verwerken HTTP-requests en returnen HTTP-responses, in combinatie met templates.<br>

#### Utils
Het systeem om bevestigings e-mails te sturen is te vinden in het bestand [`hielander_whiskey_app/utils/send_emails.py`](./hielander_whiskey_app/utils/send_emails.py). Dit systeem wordt verder toegelicht in het [schermenoverzicht](#e-mail-templates).

### Database modellen
De database modellen zijn te vinden in de map [`hielander_whiskey_app/models/`](./hielander_whiskey_app/models/), waarbij elk model zijn eigen bestand heeft. Er zijn drie modellen:
- **MasterclassReserveringen**
    - Deze tabel slaat masterclass reserveringen op. 
    - Fields: "voornaam", "tussenvoegsel", "achternaam", "e_mailadres", "opmerking", "aantal_kaarten", "totaalprijs", "reserve", "datum", "tijd", "masterclass", "sessie_nummer".

- **BottelingReserveringen**
    - Deze tabel slaat botteling reserveringen op.
    - Fields: "voornaam", "tussenvoegsel", "achternaam", "e_mailadres", "opmerking", "aantal_flessen", "totaalprijs", "reserve", "datum", "tijd".
    
*Overeenkomende eigenschappen MasterclassReserveringen en BottelingReserveringen*:<br>
-- De instance ID's, datum en tijd worden automatisch aangemaakt wanneer de reservering wordt opgeslagen.<br>
-- Wordt standaard geordend op een combinatie van datum en tijd. De meest recente reserveringen komen dus bovenaan te staan.<br>
-- De string functie in dit model print de volledige naam van de klant + de gekozen masterclass.

- **FestivalData**
    - Deze tabel slaat de algemene festival informatie op, zoals de namen en prijzen.
    - Fields: "type", "naam", "tijd", "sessie", "datum", "aantal_beschikbaar", "prijs".
    - Deze data kan worden aangepast op het admin dashboard. Het is niet mogelijk, en niet de bedoeling, dat hier instanties worden toegevoegd of verwijderd.
    - De data die in deze tabel staat wordt overal op de app gebruikt. De app werkt dan ook niet goed als deze tabel leeg is. 


## Schermenoverzicht

### Algemeen

Na het starten van de applicatie belandt de gebruiker automatisch op de [landingspagina](#landingspagina). Als de applicatie gedeployed zou worden, zou deze pagina niet relevant zijn. De gebruiker krijgt deze niet te zien. De landingspagina maakt het makkelijk voor de developer om de applicatie te testen zonder telkens een "404 - Page not found" te krijgen bij het bezoeken van de base url.

Verder staan de verschillende schermen redelijk los van elkaar. Dit is zo omdat de reserveringspagina's in het eerste geval benaderd konden worden vanaf de originele HWF website op de [botteling](http://www.hielanderwhiskyfestival.nl/festivalbotteling2024) en [masterclass](http://www.hielanderwhiskyfestival.nl/masterclass) pagina's. Om deze reden is er dus ook geen mogelijkheid om door het ticketsysteem te navigeren met een navbar of navigatie knoppen.

De "flow" is als volgt:
- Masterclass reserveringspagina &rarr; Masterclass bevestigingspagina
- Botteling reserveringspagina &rarr; Botteling bevestigingspagina
- Login pagina &rarr; Admin dashboard

### Inlogscherm
Er is een [login template](hielander_whiskey_app/templates/login.html) die voor de login pagina wordt gebruikt. De [login view](hielander_whiskey_app/views/login.py) bevat de code die de pagina gebruikt om de gebruiker succesvol in te loggen. De login_page functie: https://github.com/siepvan020/Bpexi_whiskey_project/blob/0b30ea263a413fb1d324e864f59ea0f13b035b5e/hielander_whiskey_app/views/login.py#L35-L54
wordt aangeroepen als de login pagina aangeroept wordt. Als een gebruiker probeert in te loggen, dan roept de login_page functie de try_log_in functie aan: https://github.com/siepvan020/Bpexi_whiskey_project/blob/92df571f798c48eecff68669228dfbca3c409c60/hielander_whiskey_app/views/login.py#L14-L32 
Deze functie authenticeert de gebuiker en probeert deze in te loggen. Als de gebruiker en het wachtwoord juist zijn, dan wordt de admin dashboard pagina aangeroepen.


### Admin dashboard
Er is een [dashboard template](hielander_whiskey_app/templates/dashboard.html) die voor het admin dashboard wordt gebruikt. De [dashboard view](hielander_whiskey_app/views/dashboard.py) bevat de code die de pagina gebruikt om alle tabellen en grafieken te creëren. 

De login_page functie: https://github.com/siepvan020/Bpexi_whiskey_project/blob/92df571f798c48eecff68669228dfbca3c409c60/hielander_whiskey_app/views/dashboard.py#L27-L114
wordt aangeroepen als een gebruiker succesvol ingelogd is en de dashboard pagina opent. De login_page haalt de bestellingen uit de [Botteling model](hielander_whiskey_app/models/BottelingReserveringen.py) en de [Masterclass model](hielander_whiskey_app/models/MasterclassReserveringen.py) en haalt vervolgens de bijbehorende maximale waardes uit de [FestivalData model](hielander_whiskey_app/models/FestivalData.py). 

Nadat de tabellen met deze data gemaakt zijn, worden twee functies aangeroepen: de bottel_piechart functie en de masteclass_barplot functie: https://github.com/siepvan020/Bpexi_whiskey_project/blob/92df571f798c48eecff68669228dfbca3c409c60/hielander_whiskey_app/views/dashboard.py#L117-L137 
https://github.com/siepvan020/Bpexi_whiskey_project/blob/92df571f798c48eecff68669228dfbca3c409c60/hielander_whiskey_app/views/dashboard.py#L140-L162
Deze functies maken de twee grafieken die op het admin dashboard te zien zijn aan en slaan deze op in de plots folder bij de templates. 

De dashboard pagina bevat ook een [javascript bestand](hielander_whiskey_app/static/js/dashboard.js). Dit bestand regelt de back-end van veel van de knoppen op de dashboard pagina. 

De twee functies van regel 3 t/m 32: https://github.com/siepvan020/Bpexi_whiskey_project/blob/92df571f798c48eecff68669228dfbca3c409c60/hielander_whiskey_app/static/js/dashboard.js#L2-L32
luisteren naar de knoppen op regel 41 en 42  van het dashboard template: https://github.com/siepvan020/Bpexi_whiskey_project/blob/92df571f798c48eecff68669228dfbca3c409c60/hielander_whiskey_app/templates/dashboard.html#L41-L42
en verwisselen de zichtbaarheid van de grafieken zodat de één zichtbaar wordt en dan andere verborgen wordt. 

De twee functies van regel 34 t/m 64: https://github.com/siepvan020/Bpexi_whiskey_project/blob/92df571f798c48eecff68669228dfbca3c409c60/hielander_whiskey_app/static/js/dashboard.js#L34-L64
luisteren naar de knoppen op regel 56 en 57 van het dashboard template: https://github.com/siepvan020/Bpexi_whiskey_project/blob/92df571f798c48eecff68669228dfbca3c409c60/hielander_whiskey_app/templates/dashboard.html#L56-L57
en verwisselen de zichtbaarheid van de bestellingen tabellen zodat de één zichtbaar wordt en dan andere verborgen wordt. 

De functie van regel 66 t/m 82: https://github.com/siepvan020/Bpexi_whiskey_project/blob/92df571f798c48eecff68669228dfbca3c409c60/hielander_whiskey_app/static/js/dashboard.js#L66-L82
achterhaald welke van de twee tabellen momenteel zichtbaar is, dit wordt gebruikt in een aantal van de volgende functies. 
Bijvoorbeeld, de functie van regel 84 t/m 119: https://github.com/siepvan020/Bpexi_whiskey_project/blob/92df571f798c48eecff68669228dfbca3c409c60/hielander_whiskey_app/static/js/dashboard.js#L84-L119
Deze functie achterhaald met behulp van de vorige functie welke tabel zichtbaar is en exporteert deze als CSV-bestand. 

De laatste 3 functies op regel 121 t/m 221: https://github.com/siepvan020/Bpexi_whiskey_project/blob/92df571f798c48eecff68669228dfbca3c409c60/hielander_whiskey_app/static/js/dashboard.js#L121-L221
werken samen met de functie van regel 165 t/m 191 van de dashboard.py: https://github.com/siepvan020/Bpexi_whiskey_project/blob/92df571f798c48eecff68669228dfbca3c409c60/hielander_whiskey_app/views/dashboard.py#L165-L191 
om rijen uit de bestellingen tabel te kunnen selecteren en vervolgens te verwijderen.

### Masterclass reserveringen
In het volgende gedeelte worden de onderdelen besproken die horen bij de masterclass reserveringen.

#### Masterclasses veranderen
De informatie die bij de masterclasses horen veranderen dynamisch wanneer er een sessie wordt geselecteerd of wanneer de gebruiker een masterclass selecteerd. 
Om ervoor te zorgen dat de masterclass naam, tijd, prijs en het aantal beschikbare tickets dynamisch worden overgebracht naar [masterclass_reservering.html](hielander_whiskey_app/templates/masterclass_reservering.html) wordt onderstaande code gebruikt.
https://github.com/siepvan020/Bpexi_whiskey_project/blob/0d04607dab7257b4d2a599ed2217d497cf27dc7a/hielander_whiskey_app/views/masterclass_reservering.py#L52-L68<br>
Vanuit database tabel 'FestivalData' worden de benodigde variabelen gehaald en in de dictionary 'context' geplaatst. Indien het in de toekomst nodig is om meer variabelen uit de tabel 'FestivalData' te halen, kan dit op een zelfde manier gedaan worden als in de code hierboven.

Wanneer de gebruiker van sessie veranderd, zullen de bijbehorende masterclasses als opties verschijnen bij de radio buttons die aanwezig zijn op de pagina. In de onderstaande code is terug te lezen hoe dit is vorm gegeven in [masterclass_reservering.js](hielander_whiskey_app/static/js/masterclass_reservering.js):
https://github.com/siepvan020/Bpexi_whiskey_project/blob/10c9f420fe23b87bd7d4bd4c4146303f004b356b/hielander_whiskey_app/static/js/masterclass_reservering.js#L9-L71

#### Masterclass geselecteerd
Wanneer de gebruiker een masterclass selecteerd worden een aantal functies geactiveerd. De onderstaande code wordt aangeroepen wanneer de gebruiker een masterclass selecteerd:
https://github.com/siepvan020/Bpexi_whiskey_project/blob/10c9f420fe23b87bd7d4bd4c4146303f004b356b/hielander_whiskey_app/static/js/masterclass_reservering.js#L89-L94

Vervolgens wordt eerst de functie 'update_prijs' aangeroepen. Deze functie zorgt ervoor dat onder het kopje 'totaalprijs' de prijs per ticket van de desbetreffende masterclass wordt getoond. Dit is te lezen in de onderstaande code:
https://github.com/siepvan020/Bpexi_whiskey_project/blob/10c9f420fe23b87bd7d4bd4c4146303f004b356b/hielander_whiskey_app/static/js/masterclass_reservering.js#L100-L113

Als laatst wordt de functie 'update_aantal_kaarten' aangeroepen. Deze functie zorgt ervoor dat het maximaal aantal kaarten dat besteld kan worden, wordt aangepast naar het aantal kaarten dat er nog beschikbaar zijn voor de desbetreffende masterclass. Dit is te lezen in de onderstaande code:
https://github.com/siepvan020/Bpexi_whiskey_project/blob/10c9f420fe23b87bd7d4bd4c4146303f004b356b/hielander_whiskey_app/static/js/masterclass_reservering.js#L122-L139

#### Totaalprijs updaten
De totaalprijs van de reservering wordt automatisch geupdate wanneer de gebruiker het aantal tickets aanpast naar het gewenste aantal kaarten. Onderstaande code geeft de code weer die wordt aangeroepen wanneer de gebruiker het aantal kaarten aanpast:
https://github.com/siepvan020/Bpexi_whiskey_project/blob/10c9f420fe23b87bd7d4bd4c4146303f004b356b/hielander_whiskey_app/static/js/masterclass_reservering.js#L78-L80
Vervolgens wordt de functie 'update_prijs' aangeroepen. Deze heeft dezelfde functionaliteit zoals te zien is bij 'Masterclass geselecteerd'.

#### Reservering geplaatst
Wanneer er een reservering geplaatst wordt, dan wordt de volgende code aangeroepen:
https://github.com/siepvan020/Bpexi_whiskey_project/blob/0d04607dab7257b4d2a599ed2217d497cf27dc7a/hielander_whiskey_app/views/masterclass_reservering.py#L70-L71<br>

Deze code zorgt ervoor dat de ingevulde informatie gecontroleerd wordt aan de hand van de volgende form:
https://github.com/siepvan020/Bpexi_whiskey_project/blob/0d04607dab7257b4d2a599ed2217d497cf27dc7a/hielander_whiskey_app/forms/MasterclassForm.py#L4-L16<br>

Wanneer de ingevulde gegevens niet goedgekeurd worden, dan zal de gebruiker een error message ontvangen. Hiervoor wordt de volgende code aangeroepen:
https://github.com/siepvan020/Bpexi_whiskey_project/blob/0d04607dab7257b4d2a599ed2217d497cf27dc7a/hielander_whiskey_app/views/masterclass_reservering.py#L113-L118<br>

Wanneer de ingevulde gegevens wel goedgekeurd worden, dan zal de reservering met behulp van de volgende code opgeslagen worden in de database tabel 'MasterclassReserveringen':
https://github.com/siepvan020/Bpexi_whiskey_project/blob/0d04607dab7257b4d2a599ed2217d497cf27dc7a/hielander_whiskey_app/views/masterclass_reservering.py#L72-L84<br>

Nadat de reservering is opgeslagen zal er een mail worden gestuurd naar het opgegeven mailadres. Deze mail bevat een factuur met daarin de gegevens die ingevuld zijn tijdens de reservering. De code hiervoor ziet er als volgt uit:
https://github.com/siepvan020/Bpexi_whiskey_project/blob/0d04607dab7257b4d2a599ed2217d497cf27dc7a/hielander_whiskey_app/views/masterclass_reservering.py#L87-L103<br>


### Masterclass bevestiging
Op de masterclass bevestings pagina staan de volgende onderdelen:<br>
- Een dank voor de reservering
- Een besteloverzicht

De informatie voor het bestel overzicht is afkomstig uit [masterclass_reservering.py](hielander_whiskey_app/views/masterclas_reservering.py). In de onderstaande code is te zien hoe dit wordt gedaan en welke gegevens mee worden gegeven:
https://github.com/siepvan020/Bpexi_whiskey_project/blob/0d04607dab7257b4d2a599ed2217d497cf27dc7a/hielander_whiskey_app/views/masterclass_reservering.py#L105-L112<br>


### Botteling reserveringen
De [botteling reserveringspagina](./hielander_whiskey_app/templates/botteling_reservering.html) bevat informatie en het reserveringssysteem omtrent de jaarlijkse festival botteling.<br>
- **Functies:**
    - Form voor het reserveren van flessen
    - Validatie van het form, maximaal 2 flessen per e-mailadres
    - Berekening van de totaalprijs van de reservering
    - Dynamische weergave van het aantal beschikbare flessen.
    - Versturen van een bevestigingsmail na een succesvolle reservering.

Er is naar gestreefd om de pagina zo veel mogelijk zelf te laten updaten a.d.h.v. de [Festivaldata](#database-modellen) tabel. Dit kan echter niet overal. In de volgende lijst staan elementen die handmatig aangepast moeten worden als dit nodig is:

- [Titel van de pagina](./hielander_whiskey_app/templates/botteling_reservering.html#L14). Deze kun je aanpassen op regelnummer 14 van de template (`botteling_reservering.html`). Plaats de titel tussen de >< haken.

- [Informatie over de botteling](./hielander_whiskey_app/templates/botteling_reservering.html#L17). Deze kun je aanpassen op regel 17 van de template (`botteling_reservering.html`). Plaats de info tussen de >< haken. De tekst wordt automatisch op de goede manier in het kader geplaatst.

In het onderstaande codeblok wordt een voorbeeld weergegeven van de regels van toepassing:
https://github.com/siepvan020/Bpexi_whiskey_project/blob/c6ff8bc71eeaf4d6d3460a3233ee61cf08153e4c/hielander_whiskey_app/templates/botteling_reservering.html#L12-L17

- Maximaal aantal te bestellen flessen per e-mailadres. Deze moet worden aangepast op twee plekken, in de [template](./hielander_whiskey_app/templates/botteling_reservering.html#L42) (`botteling_reservering.html`) op regel 42 en in de [view](./hielander_whiskey_app/views/botteling_reservering.py#L72) (`botteling_reservering.py`) op regel 72. Dit maximum staat standaard op 2. Let wel op dat je ook de tekst van de [errormessage](./hielander_whiskey_app/views/botteling_reservering.py#L75) op regel 75 in de view aanpast, zodat deze overeenkomt met het maximaal aantal te reserveren flessen per e-mailadres.<br>


- Grenswaarde van het tonen van het aantal flessen over. Dit kan worden aangepast in [`botteling_reservering.js`](https://github.com/siepvan020/Bpexi_whiskey_project/blob/bf106a2fc1caf1bb0a8dfc7d21c2b4678b7f6f62/hielander_whiskey_app/static/js/botteling_reservering.js#L15-L27) op regels 15 en 19. Deze waarde staat standaard op 50. Als er minder dan 50 flessen over zijn volgens de database, wordt het aantal getoond op de [`botteling_reservering.py`](./hielander_whiskey_app/templates/botteling_reservering.html#L20) op regel 20 t/m 22.<br>
Voorbeelden van de twee codeblokken zijn hieronder te zien:<br>
https://github.com/siepvan020/Bpexi_whiskey_project/blob/bf106a2fc1caf1bb0a8dfc7d21c2b4678b7f6f62/hielander_whiskey_app/static/js/botteling_reservering.js#L15-L27
<br>
https://github.com/siepvan020/Bpexi_whiskey_project/blob/bf106a2fc1caf1bb0a8dfc7d21c2b4678b7f6f62/hielander_whiskey_app/templates/botteling_reservering.html#L19-L22


### Botteling bevestiging
De [botteling bevestigingspagina](./hielander_whiskey_app/templates/botteling_bevestiging.html) toont de bevestiging van de botteling reservering.
- **Functies**:
  - Bevestiging van de reservering met details over de bestelling.
  - Instructies over het vinden van de bevestigingsmail en factuur.
  - Terugkeren naar de originele [HWF Botteling website](http://www.hielanderwhiskyfestival.nl/festivalbotteling2024).

In de volgende lijst staan elementen die handmatig aangepast moeten worden als dit nodig is:
- [Titel van de pagina](./hielander_whiskey_app/templates/botteling_bevestiging.html#L14). Deze kun je aanpassen op regel 14 van de template (`botteling_bevestiging.html`). Plaats de titel tussen de >< haken.

- [Bedanktbericht](./hielander_whiskey_app/templates/botteling_bevestiging.html#L15). Deze kun je aanpassen op regel 15 van de template (`botteling_bevestiging.html`). Plaats de gewenste (korte) zin tussen de >< haken.

- [Factuur en e-mail informatie](./hielander_whiskey_app/templates/botteling_bevestiging.html#L16). Deze kun je aanpassen vanaf regel 16 van de template (`botteling_bevestiging.html`). Er hoeven niet per se Enters in de tekst te staan.
- ["Ga terug" knop link](./hielander_whiskey_app/templates/botteling_bevestiging.html#L33). Deze gaat nu terug naar de originele HWF botteling website. Mocht deze link veranderen, kan dit aangepast worden op regel 33 van de template (`botteling_bevestiging.html`). Zorg ervoor dat de volledige link achter de `href=` wordt geplaatst, binnen de aanhalingstekens.

Voorbeelden van de stukken code die aangepast moeten worden zijn hieronder te zien:
https://github.com/siepvan020/Bpexi_whiskey_project/blob/bf106a2fc1caf1bb0a8dfc7d21c2b4678b7f6f62/hielander_whiskey_app/templates/botteling_bevestiging.html#L12-L37


### Landingspagina
De [landingspagina](./hielander_whiskey_app/templates/landingspagina.html) wordt voornamelijk gebruikt voor testdoeleinden en is niet belangrijk voor de gebruiker, zoals al is uitgelegd in het kopje ["Algemeen"](#algemeen) .
- **Functies**:
  - Testen van de applicatie zonder 404 error bij het opstarten van de applicatie.
  - Snelle toegang tot de verschillende pagina's.


### E-mail templates
De [e-mail templates](./hielander_whiskey_app/templates/email_templates/) worden gebruikt om de bevestigingsmail te vullen en stylen. Deze templates worden gemaakt in [`send_mails.py`](./hielander_whiskey_app/utils/send_emails.py).

In de volgende lijst staan elementen die handmatig aangepast moeten worden als dit nodig is:
- [Verzender e-mailadres](./hielander_whiskey_app/utils/send_emails.py#L148). Het e-mailadres waarvan de bevestigingsmails worden verstuurd kan worden aangepast op regel 148 van `send_emails.py` en op regel 130 van `settings.py`. Let op dat ook het wachtwoord aangepast moet worden.
- [E-mail account wachtwoord](./whiskey_project/settings.py#L131). Als het e-mailadres veranderd moet ook het app wachtwoord worden veranderd, op regel 131 in `settings.py`. Let op dat dit niet het echte wachtwoord van het account moet zijn, maar het "app specific password", zie [hier](https://support.google.com/accounts/answer/185833?hl=nl) instructies via Google.
- [Uiterste betaaldatum masterclass](./hielander_whiskey_app/templates/email_templates/masterclass_email.html#L77). De uiterste betaaldatum van de masterclasses kan worden aangepast op regel 77 van `masterclass_email.html`

Voorbeelden van de stukken code in settings.py zijn hieronder weergegeven:
https://github.com/siepvan020/Bpexi_whiskey_project/blob/bf106a2fc1caf1bb0a8dfc7d21c2b4678b7f6f62/whiskey_project/settings.py#L127-L132


## Unit testing

### Testing platform
Het testing platform dat wordt gebruikt voor deze applicatie is Django's standaard `unittest.TestCase` testing framework. Dit is een uitgebreide testmodule die goed integreert met het framework, waardoor het eenvoudig is om zowel model- als view tests te schrijven en uit te voeren.<br>
Django's TestCase is een uitbreiding van de standaard unittest.TestCase van Python. Het geeft extra functionaliteiten die specifiek zijn ontworpen voor het testen van Django-applicaties. Een aantal van deze functies zijn:

- **Database Rollback**: TestCase maakt gebruik van een tijdelijke database voor elke test, deze wordt aangemaakt voor de test en vernietigd gelijk na de test. Dit betekent dat elke test start met een lege database, wat zorgt voor een consistente testomgeving.<br>

- **Client**: Django's test framework bevat een test client die wordt gebruikt om requests naar de views te sturen en de responses op te halen. Dit maakt het mogelijk om volledige tests uit te voeren op de applicatie.<br>

- **Fixtures**: Met Django's TestCase kun je fixtures laden die vooraf gedefinieerde datasets bevatten. Dit maakt het eenvoudig om een bekende staat van de database te creëren voordat de tests worden uitgevoerd.<br>

- **Assertions**: unittest heeft veel verschillende soort assertions die je kunt doen om verschillende aspecten van je code te testen, zoals assertEqual, assertTrue, assertIn, enz.<br>

- **Mocking**: unittest.mock is een krachtig hulpmiddel voor het mocken van objecten en functies. De patch decorator is vooral handig voor het tijdelijk vervangen van objecten door mock-objecten tijdens een test. Dit is nuttig voor het isoleren van de code die je wilt testen en het vermijden van dependencies of validaties van externe systemen of complexe objecten.<br>

Met de combinatie van Django's TestCase en Python's unittest kun je goede en betrouwbare unittests schrijven die ervoor zorgen dat je applicatie op de goede manier werkt.

### Unit tests runnen
Om de tests uit te voeren, moet je de volgende stappen volgen:

1. Navigeer naar de hoofdmap van het project: "whisky_project". Dit is de map waar `manage.py` zich bevindt.
2. Gebruik het Django test commando: Voer het volgende command uit in de command line terminal om alle tests te runnen:
   ```bash
   python manage.py test
   ```
Je kunt er ook voor kiezen om losse testscripts te runnen.
- Voor het testen van de database modellen, voer het volgende command uit:
    ```bash
   python manage.py test hielander_whisky_app.testing.test_models
   ```
- Voor het testen van de views, voer het volgende command uit:
    ```bash
   python manage.py test hielander_whisky_app.testing.test_views
   ```

### Toegang krijgen tot de unit tests

De unit tests zijn te vinden in de map `hielander_whiskey_app/testing`. Deze map bevat twee submappen, `/test_models` en `/test_views`.
- In `/test_models` zijn alle unit tests te vinden die de database modellen testen. Dit zijn de volgende bestanden:
    - `test_bottelingreserveringen.py`
    - `test_festivaldata.py`
    - `test_masterclassreserveringen`
- In `/test_views` zijn alle unit tests te vinden die de pagina views testen. Dit zijn de volgende bestanden:
    - `test_botteling.py`
    - `test_dashboard.py`
    - `test_masterclass.py`

Uitleg over wat elke unit test doet is te vinden in de docstring documentatie van elke testfunctie.


## Development status
### Bugs 

#### Opmerking in csv 
In de dashboardpagina worden opmerkingen, die zijn ingevoerd op de reserveringspagina's, weergegeven met behulp van een tooltip in de bestellingen tabel. Bij het exporteren van deze tabel naar een CSV-bestand verschijnt overigens het teken “ðŸ›ˆ”. Dit komt doordat de unicode van het 🛈 icoon wordt geëxporteerd in plaats van de daadwerkelijke opmerking. 

#### Schermgrootte 
De applicatie is ontworpen voor standaard laptopschermen. Bij gebruik op schermen van afwijkende grootte kan de weergave van de applicatie afwijken van de verwachtingen. 

#### Reservesysteem masterclass 
Voor de masterclasskaarten was, net zoals voor de botteling, een reservelijstsysteem opgezet. Op de masterclassreserveringspagina kunnen echter niet meer dan het maximaal beschikbare aantal kaarten besteld worden. Hierdoor is het momenteel niet mogelijk om op de reservelijst te komen. 

#### Bevestiging pagina’s 
De bevestigingspagina's voor zowel de masterclass als de botteling zijn toegankelijk voordat een bestelling is voltooid. Dit komt doordat de URL van de bevestigingspagina's handmatig kan worden ingevoerd. Deze bevestigingspagina's zullen dan grotendeels leeg zijn, omdat er geen details van bestellingen zijn ingevuld. 

### Features in development 

#### Vreemde tekens 
In sommige invoervelden op de reserveringspagina's, zoals de naamvelden, wordt niet gecontroleerd op vreemde tekens. Het zou een verbetering zijn om validatie toe te voegen die dit controleert en ongewenste tekens voorkomt. 

#### Aantal beschikbare kaarten 
Op de reserveringspagina voor de masterclass wordt momenteel niet duidelijk aangegeven hoeveel kaarten er nog beschikbaar zijn. Een toekomstige verbetering zou zijn om deze informatie duidelijker weer te geven. 

#### Gebruik Try/except 
Momenteel is het gebruik van try/except in de applicatie redelijk gelimiteerd. Op veel plekken zou dit geïmplementeerd kunnen worden om de robuustheid van de applicatie te verbeteren. 

#### Festival data controle 
Als de festivaldata op de admin-dashboardpagina wordt aangepast, wordt deze momenteel niet gevalideerd. Een vorm van controle kan worden ingevoerd om misbruik of fouten te voorkomen. 
