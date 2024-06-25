document.addEventListener("DOMContentLoaded", function () {
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

  const flessenInput = document.getElementById("flessen");
  const totaalprijsSpan = document.getElementById("totaalprijs");
  const flesPrijs = parseFloat(totaalprijsSpan.getAttribute("data-fles-prijs"));
  totaalprijsSpan.innerText = `€${flesPrijs.toFixed(2).replace(".", ",")}`;

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
