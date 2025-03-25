const user_id = localStorage.getItem("user_id") || "cliente";

// LOGIN
document.getElementById("loginForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const res = await fetch("http://127.0.0.1:5000/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });

  const data = await res.json();

  if (data.success) {
    localStorage.setItem("user_id", data.user_id);
    localStorage.setItem("rol", data.rol);
    window.location.href = "/dashboard";
  } else {
    alert("Login incorrecto");
  }
});

// PRODUCTOS Y COMPRAS
async function cargarProductos() {
  const res = await fetch("http://127.0.0.1:5000/api/productos");
  const productos = await res.json();
  const contenedor = document.getElementById("productos");

  productos.forEach(prod => {
    const div = document.createElement("div");
    div.innerHTML = `
      <strong>${prod.nombre}</strong> - $${prod.precio} <br>
      ${prod.detalles}<br>
      Cantidad disponible: ${prod.cantidad}<br>
      ${prod.imagen ? `<img src="/uploads/${prod.imagen}" style="max-width:100px">` : ""}
      <form onsubmit="return comprarProducto(event, ${prod.id}, ${prod.precio})">
        <input type="number" name="cantidad" placeholder="Cantidad a comprar" min="1" max="${prod.cantidad}" required>
        <button type="submit">Comprar</button>
      </form>
      <hr>
    `;
    contenedor.appendChild(div);
  });
}

async function comprarProducto(e, productoId, precio) {
  e.preventDefault();
  const cantidad = parseInt(e.target.cantidad.value);
  if (!cantidad || cantidad <= 0) return;

  const data = new FormData();
  data.append("tipo", "compra producto " + productoId);
  data.append("monto", cantidad * precio);
  data.append("fecha", new Date().toISOString().split("T")[0]);
  data.append("usuario_id", user_id);
  data.append("cantidad", cantidad);

  const res = await fetch("http://127.0.0.1:5000/api/salidas/", {
    method: "POST",
    body: data
  });

  if (res.ok) {
    alert("Compra realizada");
    cargarProductos();
  } else {
    alert("Error al procesar la compra");
  }
}

cargarProductos();
