document.getElementById("formSalida").addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = e.target;
  const data = new FormData(form);
  data.append("usuario_id", user_id);

  await fetch("http://127.0.0.1:5000/api/salidas/", {
    method: "POST",
    body: data
  });

  form.reset();
  cargarSalidas();
});

async function cargarSalidas() {
  const res = await fetch(`http://127.0.0.1:5000/api/salidas/${user_id}`);
  const salidas = await res.json();
  const contenedor = document.getElementById("salidas");
  contenedor.innerHTML = "";

  salidas.forEach(salida => {
    //console.log("Salida:", salida); // Verificar usuario_id
    const div = document.createElement("div");
    div.className = "item";
    div.innerHTML = `
      <strong>${salida.tipo}</strong> - $${salida.monto} <br>
      Fecha: ${salida.fecha}<br>
      Cantidad: ${salida.cantidad || 'N/A'}<br>
      ${salida.factura_ruta ? `<a href="/uploads/${salida.factura_ruta}" target="_blank">Ver factura</a><br>` : ""}
    `;

    if (rol === "admin" || salida.usuario_id == user_id) {
      const acciones = document.createElement("div");
      acciones.className = "admin-controls";
      acciones.innerHTML = `
        <button onclick="eliminarSalida(${salida.id})" class="btn btn-danger btn-sm me-1">Eliminar</button>
        <button onclick='editarSalida(${JSON.stringify(salida)})' class="btn btn-warning btn-sm">Editar</button>
      `;
      div.appendChild(acciones);
    }

    contenedor.appendChild(div);
  });
}

async function eliminarSalida(id) {
  const result = await Swal.fire({
    title: "¿Estás seguro?",
    text: "Esta salida será eliminada",
    icon: "warning",
    showCancelButton: true,
    confirmButtonText: "Sí, eliminar",
    cancelButtonText: "Cancelar"
  });

  if (!result.isConfirmed) return;

  await fetch(`http://127.0.0.1:5000/api/salidas/delete/${id}?usuario_id=${user_id}&rol=${rol}`, {
    method: "DELETE"
  });

  cargarSalidas();
}

function editarSalida(salida) {
  Swal.fire({
    title: "Editar Salida",
    html: `
      <input id="tipo" class="swal2-input" placeholder="Tipo" value="${salida.tipo}">
      <input id="monto" type="number" class="swal2-input" placeholder="Monto" value="${salida.monto}">
      <input id="fecha" type="date" class="swal2-input" value="${salida.fecha}">
      <input id="cantidad" type="number" class="swal2-input" placeholder="Cantidad" value="${salida.cantidad || 1}">
    `,
    focusConfirm: false,
    preConfirm: () => {
      return {
        tipo: document.getElementById("tipo").value,
        monto: document.getElementById("monto").value,
        fecha: document.getElementById("fecha").value,
        cantidad: document.getElementById("cantidad").value
      };
    }
  }).then(result => {
    if (!result.isConfirmed) return;
    const { tipo, monto, fecha, cantidad } = result.value;

    const data = new FormData();
    data.append("tipo", tipo);
    data.append("monto", monto);
    data.append("fecha", fecha);
    data.append("cantidad", cantidad);
    data.append("usuario_id", user_id);
    data.append("rol", rol);

    fetch(`http://127.0.0.1:5000/api/salidas/update/${salida.id}`, {
      method: "PUT",
      body: data
    }).then(() => cargarSalidas());
  });
}
