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