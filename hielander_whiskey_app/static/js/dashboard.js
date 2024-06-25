document.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("grafiek-botteling")
    .addEventListener("click", function () {
      var x = document.getElementById("grafiek_botteling");
      var y = document.getElementById("grafiek_masterclass");

      x.style.display = "block";
      y.style.display = "none";
    });

  document
    .getElementById("grafiek-masterclass")
    .addEventListener("click", function () {
      var y = document.getElementById("grafiek_botteling");
      var x = document.getElementById("grafiek_masterclass");

      x.style.display = "block";
      y.style.display = "none";
    });

  document
    .getElementById("tabel-botteling")
    .addEventListener("click", function () {
      var x = document.getElementById("tabel_botteling");
      var y = document.getElementById("tabel_masterclass");

      x.style.display = "block";
      y.style.display = "none";
    });

  document
    .getElementById("tabel-masterclass")
    .addEventListener("click", function () {
      var y = document.getElementById("tabel_botteling");
      var x = document.getElementById("tabel_masterclass");

      x.style.display = "block";
      y.style.display = "none";
    });

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

  document
    .getElementById("tabel-export")
    .addEventListener("click", function () {
      var table = getVisibleTable();
      if (!table) {
        alert("Er is momenteel geen tabel zichtbaar.");
        return;
      }

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

   document
    .getElementById("deleteSelectedRowIds")
    .addEventListener("click", function () {
    var selectedData = getSelectedRowIds();
    console.log('Geselecteerde Data:', selectedData);
    if (!selectedData.ids || selectedData.ids.length === 0) {
        alert("Geen rijden geselecteerd.");
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
