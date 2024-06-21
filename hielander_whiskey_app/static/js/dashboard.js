function grafiek_botteling() {
    var x = document.getElementById("grafiek_botteling");
    var y = document.getElementById("grafiek_masterclass");

    x.style.display = "block";
    y.style.display = "none";
}

function grafiek_masterclass() {
    var y = document.getElementById("grafiek_botteling");
    var x = document.getElementById("grafiek_masterclass");

    x.style.display = "block";
    y.style.display = "none";
}


function tabel_botteling() {
    var x = document.getElementById("tabel_botteling");
    var y = document.getElementById("tabel_masterclass");

    x.style.display = "block";
    y.style.display = "none";
}

function tabel_masterclass() {
    var y = document.getElementById("tabel_botteling");
    var x = document.getElementById("tabel_masterclass");

    x.style.display = "block";
    y.style.display = "none";
}

function getVisibleTable() {
    var tabelBotteling = document.getElementById("tabel_botteling");
    var tabelMasterclass = document.getElementById("tabel_masterclass");

    if (tabelBotteling.style.display === "block") {
        return tabelBotteling;
    } else if (tabelMasterclass.style.display === "block") {
        return tabelMasterclass;
    } else {
        return null;
    }
}

function exportTableToCSV() {
    var table = getVisibleTable();
    if (!table) {
        alert("No table is currently visible.");
        return;
    }

    var rows = table.querySelectorAll('tr');
    var csvContent = '';

    rows.forEach(function(row) {
        var cells = row.querySelectorAll('th, td');
        var rowData = [];
        cells.forEach(function(cell) {
            rowData.push(cell.innerText);
        });
        csvContent += rowData.join(',') + '\n';
    });

    var blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    var link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'table_data.csv';
    link.style.display = 'none';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}