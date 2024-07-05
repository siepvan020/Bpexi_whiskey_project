from django import forms
from hielander_whiskey_app.models import MasterclassReserveringen

class MasterclassReserveringenForm(forms.ModelForm):
    class Meta:
        model = MasterclassReserveringen
        fields = [
            'voornaam', 
            'tussenvoegsel',
            'achternaam', 
            'e_mailadres', 
            'opmerking',
            'sessie_nummer',
            'masterclass',
            'aantal_kaarten',
        ]