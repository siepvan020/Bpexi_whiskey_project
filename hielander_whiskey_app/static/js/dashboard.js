document.addEventListener("DOMContentLoaded", function () {

/**
 * Deze functie luister naar de grafiek-botteling knop uit de dashboard.html.
 * Als op de knop gedrukt wordt, dan verandert de display van de masterclass grafiek naar none,
 * en de display van botteling grafiek naar block.
 *
 */
  document
    .getElementById("grafiek-botteling")
    .addEventListener("click", function () {
      var x = document.getElementById("grafiek_botteling");
      var y = document.getElementById("grafiek_masterclass");

      x.style.display = "block";
      y.style.display = "none";
    });

/**
 * Deze functie luister naar de grafiek-masterclass knop uit de dashboard.html.
 * Als op de knop gedrukt wordt, dan verandert de display van de botteling grafiek naar none,
 * en de display van masterclass grafiek naar block.
 *
 */
  document
    .getElementById("grafiek-masterclass")
    .addEventListener("click", function () {
      var y = document.getElementById("grafiek_botteling");
      var x = document.getElementById("grafiek_masterclass");

      x.style.display = "block";
      y.style.display = "none";
    });

/**
 * Deze functie luister naar de tabel-masterclass knop uit de dashboard.html.
 * Als op de knop gedrukt wordt, dan verandert de display van de botteling tabel naar block,
 * en de display van masterclass tabel naar none.
 *
 */
  document
    .getElementById("tabel-botteling")
    .addEventListener("click", function () {
      var x = document.getElementById("tabel_botteling");
      var y = document.getElementById("tabel_masterclass");

      x.style.display = "block";
      y.style.display = "none";
    });

/**
 * Deze functie luister naar de tabel-masterclass knop uit de dashboard.html.
 * Als op de knop gedrukt wordt, dan verandert de display van de masterclass tabel naar block,
 * en de display van botteling tabel naar none.
 *
 */
  document
    .getElementById("tabel-masterclass")
    .addEventListener("click", function () {
      var y = document.getElementById("tabel_botteling");
      var x = document.getElementById("tabel_masterclass");

      x.style.display = "block";
      y.style.display = "none";
    });

/**
 * Deze functie geeft aan welke tabel momenteel zichtbaar is.
 *
 * @returns {Object|null} Een object met de zichtbare tabel en het type, of `null` als geen tabel zichtbaar is.
 */
  function getVisibleTable() {
    var tabelBotteling = document.getElementById("tabel_botteling");
    var tabelMasterclass = document.getElementById("tabel_masterclass");

    if (tabelBotteling.style.display === "block") {
      return { table: tabelBotteling, type: "botteling" };
    } else if (tabelMasterclass.style.display === "block") {
      return { table: tabelMasterclass, type: "masterclass" };
    } else {
      return null;
    }
  }

/**
 * Deze functie luister naar de tabel-export knop uit de dashboard.html.
 * Als op de knop gedrukt wordt, dan checkt de functie welke tabel momenteel zichtbaar is.
 * en exporteert de inhoud als CSV bestand.
 */
  document
    .getElementById("tabel-export")
    .addEventListener("click", function () {
      var visibleTable = getVisibleTable();
      if (!visibleTable) {
        alert("Er is momenteel geen tabel zichtbaar.");
        return;
      }

      var table = visibleTable.table;
      var rows = table.querySelectorAll("tr");
      var csvContent = "";

      rows.forEach(function (row) {
        var cells = row.querySelectorAll("th, td");
        var rowData = [];
        cells.forEach(function (cell) {
          rowData.push(cell.innerText);
        });
        csvContent += rowData.join(";") + "\n";
      });

      var blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
      var link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = table.id + ".csv";
      link.style.display = "none";
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    });

/**
 * Verkrijgt de IDs van de geselecteerde rijen uit de momenteel zichtbare tabel.
 *
 * @returns {Object} Een object met daarin de IDs van de geselecteerde rijen en de zichtbare tabel.
 */
  function getSelectedRowIds() {
    var visibleTable = getVisibleTable();
    if (!visibleTable) {
        alert("Geen tabel gekozen.");
        return { ids: [], type: null };
    }

    var checkboxes = visibleTable.table.querySelectorAll('input[type="checkbox"]:checked');
    var ids = [];
    checkboxes.forEach(function(checkbox) {
        ids.push(checkbox.dataset.id);
    });

    console.log('Geselecteerde IDs:', ids);
    return { ids: ids, type: visibleTable.type };
}

/**
 * Deze functie luister naar de deleteSelectedRowIds knop uit de dashboard.html.
 * Als op de knop gedrukt wordt, verwijdert deze functie de geselecteerde rijen uit de database
 * en uit de tabel.
 */
   document
    .getElementById("deleteSelectedRowIds")
    .addEventListener("click", function () {
    var selectedData = getSelectedRowIds();
    console.log('Geselecteerde Data:', selectedData);
    if (!selectedData.ids || selectedData.ids.length === 0) {
        alert("Geen rijen geselecteerd.");
        return;
    }
    if (!confirm("Weet je zeker dat je de geselecteerde rij(en) wilt verwijderen?")) {
        return;
    }

    fetch('/delete-rij/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ ids: selectedData.ids, type: selectedData.type })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Server Response:', data);
        if (data.success) {
            selectedData.ids.forEach(function(id) {
                var row = document.querySelector(`tr[data-id="${id}"]`);
                if (row) {
                    row.remove();
                }
            });
        } else {
            alert("Error tijdens het verwijderen: " + (data.error || "Unknown error"));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("Er is een fout opgetreden.");
    });
});

/**
 * Verkrijgt de waarde van een specifieke cookie met behulp van de naam.
 *
 * @param {string} name - De naam van de specifieke cookie.
 * @returns {string|null} De waarde van de cookie, of null als de cookie niet bestaat.
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
});
