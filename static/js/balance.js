const user_id = localStorage.getItem("user_id");

async function generarReporte() {
  const mes = document.getElementById("mesSeleccionado").value;
  if (!mes) {
    Swal.fire("Por favor selecciona un mes");
    return;
  }

  const [anio, mesNum] = mes.split("-");
  const inicio = `${anio}-${mesNum}-01`;
  const fin = new Date(anio, mesNum, 0).toISOString().split("T")[0];

  // Formatear mes en texto 
  const mesTexto = new Intl.DateTimeFormat('es-ES', { month: 'long', year: 'numeric' })
    .format(new Date(`${anio}-${mesNum}-01`));

  document.getElementById("rangoFechasTexto").textContent = `${inicio} / ${fin}`;
  document.getElementById("tituloReporte").textContent = `Reporte Mensual de Balance - ${mesTexto.charAt(0).toUpperCase() + mesTexto.slice(1)}`;

  const user_id = localStorage.getItem("user_id");
  const url = `http://127.0.0.1:5000/api/reportes/balance?usuario_id=${user_id}&inicio=${inicio}&fin=${fin}`;

  const res = await fetch(url);
  const data = await res.json();

  document.getElementById("contenidoReporte").style.display = "block";

  const tbodyEntradas = document.querySelector("#tablaEntradas tbody");
  const tbodySalidas = document.querySelector("#tablaSalidas tbody");
  tbodyEntradas.innerHTML = "";
  tbodySalidas.innerHTML = "";

  let totalEntradas = 0, totalSalidas = 0;

  data.entradas.forEach(e => {
    tbodyEntradas.innerHTML += `<tr><td>${e.tipo}</td><td>$${e.monto}</td><td>${e.fecha}</td></tr>`;
    totalEntradas += parseFloat(e.monto);
  });

  data.salidas.forEach(s => {
    tbodySalidas.innerHTML += `<tr><td>${s.tipo}</td><td>$${s.monto}</td><td>${s.fecha}</td></tr>`;
    totalSalidas += parseFloat(s.monto);
  });

  // Totales
  tbodyEntradas.innerHTML += `
    <tr class="table-success fw-bold">
      <td>TOTAL</td>
      <td>$${totalEntradas.toFixed(2)}</td>
      <td></td>
    </tr>`;
  tbodySalidas.innerHTML += `
    <tr class="table-danger fw-bold">
      <td>TOTAL</td>
      <td>$${totalSalidas.toFixed(2)}</td>
      <td></td>
    </tr>`;

  const balance = totalEntradas - totalSalidas;
  document.getElementById("balance").innerText = `Balance mensual: $${balance.toFixed(2)}`;

  renderGrafico(totalEntradas, totalSalidas);
  document.getElementById("btnExportarPDF").style.display = "inline-block";

}

function exportarPDF() {
  const canvas = document.getElementById("graficoBalance");
  const imgData = canvas.toDataURL("image/png");

  const imgElement = document.createElement("img");
  imgElement.src = imgData;
  imgElement.id = "imgGraficoBalance";
  imgElement.style.maxWidth = "300px";
  imgElement.style.display = "block";
  imgElement.style.margin = "20px auto";
  canvas.style.display = "none";

  canvas.parentNode.insertBefore(imgElement, canvas);

  const contenido = document.getElementById("contenidoReporte");

  const opciones = {
    margin: 0.5,
    filename: `reporte_balance_${new Date().toISOString().slice(0, 10)}.pdf`,
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { scale: 2 },
    jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
  };

  html2pdf().set(opciones).from(contenido).save().then(() => {
    document.getElementById("imgGraficoBalance").remove();
    canvas.style.display = "block";
  });
}

function renderGrafico(entradas, salidas) {
  const ctx = document.getElementById('graficoBalance').getContext('2d');
  if (window.miGrafico) window.miGrafico.destroy();

  window.miGrafico = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: ['Entradas', 'Salidas'],
      datasets: [{
        data: [entradas, salidas],
        backgroundColor: ['#28a745', '#dc3545']
      }]
    }
  });
}

window.onload = function () {
  document.getElementById("btnExportarPDF").style.display = "none";
};

function volverAlDashboard() {
  window.location.href = "/dashboard";
}

