<?php
$nombre=$POST['nombre'];
$correo=$POST['correo'];
$celular=$POST['celular'];
$mensaje=$POST['mensaje'];

$destino="juhanramos3@gmail.com";
$asunto="Nuevo Mensaje de Web";

$mensaje="de: $nombre \n";
$mensaje.="correo: $correo \n";
$mensaje.="celular: $celular \n";
$mensaje.="mensaje: $mensaje \n";

mail($destino, $asunto, $mensaje);

#header('location:contacto.html');
?>