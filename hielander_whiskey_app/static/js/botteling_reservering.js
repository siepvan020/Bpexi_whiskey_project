/**
 * JavaScript code voor het displayen van de flessenstatus en berekening van totaalprijs op basis van het aantal flessen.
 * DOM content loaded eventlistener om te zorgen dat de DOM volledig is geladen voordat functies worden uitgevoerd.
 *
 * Om de flessenstatus te tonen bij een andere waarde van 50, pas deze waarde dan aan op regel 15 en 19.
 * Vul in plaats van "50" het gewenste aantal in waarbij een waarschuwing moet worden getoond.
 */

document.addEventListener("DOMContentLoaded", function () {
  // Haalt het aantal flessen op uit een hidden element en toont de goede flessen status.
  let aantalFlessen = document
    .getElementById("hidden-flessen-count")
    .getAttribute("data-flessen-count");

  if (aantalFlessen > 50) {
    console.log("Nog genoeg");
    let flesVoldoende = document.getElementById("fles-voldoende");
    flesVoldoende.style.display = "block";
  } else if (aantalFlessen <= 50) {
    console.log("Nog 50 over");
    let flesVoldoende = document.getElementById("fles-bijna");
    flesVoldoende.style.display = "block";
  } else if (aantalFlessen == "None") {
    console.log("Flessen op");
    let flesVoldoende = document.getElementById("fles-op");
    flesVoldoende.style.display = "block";
  }

  // Haal het aantal geselecteerde flessen en de totaalprijs van de reservering op.
  const flessenInput = document.getElementById("flessen");
  const totaalprijsSpan = document.getElementById("totaalprijs");
  const flesPrijs = parseFloat(totaalprijsSpan.getAttribute("data-fles-prijs"));
  totaalprijsSpan.innerText = `€${flesPrijs.toFixed(2).replace(".", ",")}`;

  /**
   * Eventlistener toevoegen aan de flessen invoer om de totaalprijs dynamisch bij te werken wanneer het aantal flessen verandert.
   */
  flessenInput.addEventListener("input", function () {
    if (flessenInput.value) {
      const aantalFlessen = parseInt(flessenInput.value);
      const totaalprijs = aantalFlessen * flesPrijs;
      totaalprijsSpan.innerText = `€${totaalprijs
        .toFixed(2)
        .replace(".", ",")}`;
    }
  });
});
