from django.urls import path
from . import views

app_name = "appdiverxia"

urlpatterns = [
path('login', views.Login.as_view(), name='login'),
path('panel', views.Panel.as_view(), name='panel'),
path('salir', views.Salir.as_view(), name='salir'),
path('perfil/<str:modo>/<int:p>', views.Perfil.as_view(), name='perfil'),
path('eliminar/<str:modo>/<int:p>', views.Eliminar.as_view(), name='eliminar'),

path('productos', views.ListarProductos.as_view(), name='listarProductos'),
path('productos/agregar', views.AgregarProducto.as_view(), name='agregarProducto'),
path('productos/importar', views.ImportarProductos.as_view(), name='importarProductos'),
path('productos/exportar', views.ExportarProductos.as_view(), name='exportarProductos'),
path('productos/<int:p>/editar', views.EditarProducto.as_view(), name='editarProducto'),

path('listarProveedores', views.ListarProveedores.as_view(), name='listarProveedores'),
path('agregarProveedor', views.AgregarProveedor.as_view(), name='agregarProveedor'),
path('importarProveedores', views.ImportarProveedores.as_view(), name='importarProveedores'),
path('exportarProveedores', views.ExportarProveedores.as_view(), name='exportarProveedores'),
path('editarProveedor/<int:p>', views.EditarProveedor.as_view(), name='editarProveedor'),

path('agregarPedido', views.AgregarPedido.as_view(), name='agregarPedido'),
path('listarPedidos', views.ListarPedidos.as_view(), name='listarPedidos'),
path('detallesPedido', views.DetallesPedido.as_view(), name='detallesPedido'),
path('verPedido/<int:p>',views.VerPedido.as_view(), name='verPedido'),
path('validarPedido/<int:p>',views.ValidarPedido.as_view(), name='validarPedido'),
path('generarPedido/<int:p>',views.GenerarPedido.as_view(), name='generarPedido'),
path('generarPedidoPDF/<int:p>',views.GenerarPedidoPDF.as_view(), name='generarPedidoPDF'),

path('cliente', views.ListarClientes.as_view(), name='listarClientes'),
path('cliente/agregar', views.AgregarCliente.as_view(), name='agregarCliente'),
path('cliente/importar', views.ImportarClientes.as_view(), name='importarClientes'),
path('cliente/exportar', views.ExportarClientes.as_view(), name='exportarClientes'),
path('cliente/<int:p>/editar', views.EditarCliente.as_view(), name='editarCliente'),

path('emitirFactura', views.EmitirFactura.as_view(), name='emitirFactura'),
path('detallesDeFactura', views.DetallesFactura.as_view(), name='detallesDeFactura'),
path('listarFacturas',views.ListarFacturas.as_view(), name='listarFacturas'),
path('verFactura/<int:p>',views.VerFactura.as_view(), name='verFactura'),
path('generarFactura/<int:p>',views.GenerarFactura.as_view(), name='generarFactura'),
path('generarFacturaPDF/<int:p>',views.GenerarFacturaPDF.as_view(), name='generarFacturaPDF'),

path('crearUsuario',views.CrearUsuario.as_view(), name='crearUsuario'),
path('listarUsuarios', views.ListarUsuarios.as_view(), name='listarUsuarios'),

path('importarBDD',views.ImportarBDD.as_view(), name='importarBDD'),
path('descargarBDD', views.DescargarBDD.as_view(), name='descargarBDD'),

path('metodospago', views.ListarMetodosPago.as_view(), name='metodospago'),
path('metodospago/agregar', views.AgregarMetodosPago.as_view(), name='metodospago.agregar'),
path('metodospago/<int:p>/editar/', views.EditarMetodosPago.as_view(), name='metodospago.editar'),

path('configuracionGeneral', views.ConfiguracionGeneral.as_view(), name='configuracionGeneral'),

path('verManualDeUsuario/<str:pagina>/',views.VerManualDeUsuario.as_view(), name='verManualDeUsuario')
]

