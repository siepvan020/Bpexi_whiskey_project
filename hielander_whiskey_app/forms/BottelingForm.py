from django import forms
from hielander_whiskey_app.models import BottelingReserveringen

class BottelingReserveringenForm(forms.ModelForm):
    class Meta:
        model = BottelingReserveringen
        fields = [
            'voornaam', 
            'tussenvoegsel', 
            'achternaam', 
            'e_mailadres', 
            'opmerking', 
            'aantal_flessen',
            'totaalprijs',
        ]