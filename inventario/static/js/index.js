document.addEventListener("DOMContentLoaded", function () {
    const botonesVer = document.querySelectorAll(".btn-ver");
    botonesVer.forEach(btn => {
        btn.addEventListener("click", function () {
            document.getElementById("modal-nombre").textContent = this.dataset.nombre;
            document.getElementById('modal-fabricante').innerText = btn.dataset.fabricante;
            document.getElementById('modal-modelo').innerText = btn.dataset.modelo;
            document.getElementById('modal-n_serie').innerText = btn.dataset.n_serie;
            document.getElementById("modal-descripcion").textContent = this.dataset.descripcion;
            document.getElementById("modal-categoria").textContent = this.dataset.categoria;
            document.getElementById("modal-stock").textContent = this.dataset.stock;
            document.getElementById('modal-nivel_minimo').innerText = btn.dataset.nivel_minimo;
            document.getElementById("modal-ubicacion").textContent = this.dataset.ubicacion;
            document.getElementById("modal-creacion").textContent = this.dataset.creacion;
            document.getElementById("modal-actualizacion").textContent = this.dataset.actualizacion;
            document.getElementById("modal-imagen").src = this.dataset.imagen;

            const historialBtn = document.getElementById("modal-historial-btn");
            const productoId = this.dataset.id;
            historialBtn.href = `/historial/${productoId}/`;

            // Mostrar el modal (usando Bootstrap 5)
            const modal = new bootstrap.Modal(document.getElementById('detalleModal'));
            modal.show();
        });
    });
});