document.addEventListener("DOMContentLoaded", function () {
  console.log("Script geladen!!");

  // Event listener voor de sessie_nummer dropdown
  document
    .getElementById("sessie_nummer")
    .addEventListener("input", function () {
      waarde = document.getElementById("sessie_nummer").value;
      if (waarde == "1") {
        console.log("sessie 1");
        document.getElementById("masterclass1").value = "masterclass 1";
        var label = document.querySelector("label[for=masterclass1]");
        label.innerHTML = "Masterclass 1";
        document.getElementById("masterclass2").value = "masterclass 2";
        label = document.querySelector("label[for=masterclass2]");
        label.innerHTML = "Masterclass 2";
      } else if (waarde == "2") {
        console.log("sessie 2");
        document.getElementById("masterclass1").value = "masterclass 3";
        var label = document.querySelector("label[for=masterclass1]");
        label.innerHTML = "Masterclass 3";
        document.getElementById("masterclass2").value = "masterclass 4";
        label = document.querySelector("label[for=masterclass2]");
        label.innerHTML = "Masterclass 4";
      } else {
        console.log("sessie 3");
        document.getElementById("masterclass1").value = "masterclass 5";
        var label = document.querySelector("label[for=masterclass1]");
        label.innerHTML = "Masterclass 5";
        document.getElementById("masterclass2").value = "masterclass 6";
        label = document.querySelector("label[for=masterclass2]");
        label.innerHTML = "Masterclass 6";
      }
    });

  // Event listener voor het aantal_kaarten inputveld
  document
    .getElementById("aantal_kaarten")
    .addEventListener("input", update_prijs);

  // Event listener voor de masterclass radio buttons
  document
    .querySelectorAll("input[name=masterclass]")
    .forEach(function (input) {
      input.addEventListener("change", update_prijs);
    });

  // Functie om de prijs te updaten voor zowel het aantal kaarten als het masterclass nummer
  function update_prijs() {
    let prijs_dict = JSON.parse(
      document.getElementById("hidden-data-prijzen").textContent
    );
    let masterclass_selected = document.querySelector(
      "input[name=masterclass]:checked"
    ).value;

    var aantal_kaarten = document.getElementById("aantal_kaarten").value;
    var prijs = prijs_dict[masterclass_selected];
    var totaalprijs = aantal_kaarten * prijs;
    var nieuwe_prijs = new String("€" + totaalprijs);
    document.getElementById("totaalprijs").innerHTML = nieuwe_prijs;
  }
});
