## Voorwoord

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


## Schermenoverzicht

### Inlogscherm
Er is een [login template](hielander_whiskey_app/templates/login.html) die voor de login pagina wordt gebruikt. De [login view](hielander_whiskey_app/views/login.py) bevat de code die de pagina gebruikt om de gebruiker succesvol in te loggen. De login_page functie: https://github.com/siepvan020/Bpexi_whiskey_project/blob/0b30ea263a413fb1d324e864f59ea0f13b035b5e/hielander_whiskey_app/views/login.py#L35-L54
wordt aangeroepen als de login pagina aangeroept wordt. Als een gebruiker probeert in te loggen, dan roept de login_page functie de try_log_in functie aan: https://github.com/siepvan020/Bpexi_whiskey_project/blob/92df571f798c48eecff68669228dfbca3c409c60/hielander_whiskey_app/views/login.py#L14-L32 
Deze functie authenticeert de gebuiker en probeert deze in te loggen. Als de gebruiker en het wachtwoord juist zijn, dan wordt de admin dashboard pagina aangeroepen.


### admin dashboard
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

## Masterclass reserveringen
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

## Unit testing


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
