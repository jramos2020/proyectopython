function eliminarEntrada(idEntrada, modo)
{

    $("#confirm-modal").modal('show')
    let borrar = document.getElementById('modal_borrar');
    borrar.href = "/appdiverxia/eliminar/" + modo + "/" + idEntrada

} 