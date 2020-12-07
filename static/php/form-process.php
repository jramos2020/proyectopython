<?php

$errorMSG = "";

// NAME
if (empty($_POST["nombre"])) {
    $errorMSG = "Name is required ";
} else {
    $name = $_POST["nombre"];
}

// EMAIL
if (empty($_POST["correo"])) {
    $errorMSG .= "Email is required ";
} else {
    $email = $_POST["correo"];
}

// celular
if (empty($_POST["celular"])) {
    $errorMSG .= "celular is required ";
} else {
    $subject = $_POST["celular"];
}

// MESSAGE
if (empty($_POST["mensaje"])) {
    $errorMSG .= "mensaje is required ";
} else {
    $message = $_POST["mensaje"];
}


$EmailTo = "juhanramos3@gmail.com";
$Subject = "Nuevo mensaje recibido PaginaWeb";

// prepare email body text
$Body = "";
$Body .= "nombre: ";
$Body .= $name;
$Body .= "\n";
$Body .= "correo: ";
$Body .= $email;
$Body .= "\n";
$Body .= "celular: ";
$Body .= $guest;
$Body .= "\n";
$Body .= "event: ";
$Body .= $event;
$Body .= "\n";
$Body .= "mensaje: ";
$Body .= $message;
$Body .= "\n";

// enviar correo electrónico
$success = mail($EmailTo, $Subject, $Body, "From:".$email);

// redirigir a la página de éxito
if ($success && $errorMSG == ""){
   echo "success";
}else{
    if($errorMSG == ""){
        echo "Something went wrong :(";
    } else {
        echo $errorMSG;
    }
}

?>