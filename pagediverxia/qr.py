import pyqrcode as QRCODE

qrcode_enlace = QRCODE.create("https://www.facebook.com/juhanramos1")
qrcode_enlace.png("qr-code.png")