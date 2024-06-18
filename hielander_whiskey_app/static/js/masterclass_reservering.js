console.log('Script geladen!!');

function sessie_selectie() {
    waarde = document.getElementById('sessie_nummer').value;
    if (waarde == '1') {
        console.log('sessie 1');
        document.getElementById('masterclass1').value = 'masterclass; 1';
        var label = document.querySelector('label[for=masterclass1]')
        label.innerHTML = 'Masterclass 1';
        document.getElementById('masterclass2').value = 'masterclass 2';
        label = document.querySelector('label[for=masterclass2]');
        label.innerHTML = 'Masterclass 2';
    } else if (waarde == '2') {
        console.log('sessie 2');
        document.getElementById('masterclass1').value = 'masterclass; 3';
        var label = document.querySelector('label[for=masterclass1]')
        label.innerHTML = 'Masterclass 3';
        document.getElementById('masterclass2').value = 'masterclass 4';
        label = document.querySelector('label[for=masterclass2]');
        label.innerHTML = 'Masterclass 4';
    } else {
        console.log('sessie 3');
        document.getElementById('masterclass1').value = 'masterclass; 5';
        var label = document.querySelector('label[for=masterclass1]')
        label.innerHTML = 'Masterclass 5';
        document.getElementById('masterclass2').value = 'masterclass 6';
        label = document.querySelector('label[for=masterclass2]');
        label.innerHTML = 'Masterclass 6';
    };
};

function prijs_aanpassen() {
    var aantal_kaarten = document.getElementById('aantal_kaarten').value;
    var prijs = 15;
    var totaalprijs = aantal_kaarten * prijs;
    var nieuwe_prijs = new String("€" + totaalprijs);
    document.getElementById('totaalprijs').innerHTML = nieuwe_prijs;
}