📋 Informe de Errores Corregidos
Proyecto: Gestión de Clientes, Cuentas y Transacciones
Fecha: 27/09/2026
Framework: Django 5.2

1. 🗄️ Errores en Modelos
#	Modelo	Error	Corrección
1.	Cuenta	__str__ devolvía " CTA-001 | Juan Pérez" (espacio extra e invertido)	f"{self.cliente.nombre} | {self.numero}"
2.	Cuenta	Typo self.cleinte	self.cliente
3.	Transaccion	__str__ usaba self.tipo (minúscula)	self.get_tipo_display() + etiquetas capitalizadas
4.	Transaccion	IntegerField(max_length=12) inválido	PositiveIntegerField o DecimalField
2. 🎛️ Errores en Vistas
#	Vista	Error	Corrección
5.	ClienteDetailView	Método listado_clientes mal ubicado dentro de la clase	Eliminado (duplicaba ClienteListView)
6.	Todas	AccesoPersonalMixin exige is_staff=True	Documentado (causa de los 403 en tests)
3. ⚙️ Errores en Admin
#	Admin	Error	Corrección
7.	TransaccionAdmin	filter_horizontal = ("tipo",) sobre CharField	Reemplazado por list_filter = ("tipo",)
4. 🧪 Errores en Tests
#	Test	Error	Corrección
8.	ClienteViewsTest	Usuario sin is_staff=True → 403	Añadido is_staff=True
9.	AuthTest	test_detalle_cliente_muestra_datos mal ubicado	Reubicado en ClienteViewsTest
10.	URLsTest	reverse('lista_clientes') == ''	Cambiado a '/'
11.	ClienteViewsTest	assertTemplateUsed('clientes/...') ≠ 'gestion/...'	Alinear nombres de templates
5. 📄 Errores en Templates
#	Template	Error	Corrección
12.	listado_certificados.html	{{ certificado.estado }} mostraba valor crudo	{{ certificado.get_estado_display }}
13.	Múltiples	render() con objeto en vez de diccionario	render(..., {'form': form})
14.	base.html	{% titulo block %} (orden invertido)	{% block titulo %}
15.	Sidebar	Faltaba </div> de cierre	Cerrado
6. 🔧 Errores de Configuración
#	Ubicación	Error	Corrección
16.	settings.py	DIRS vacío, templates en carpeta .templetes	Renombrada a templates + DIRS: [BASE_DIR / 'templates']
17.	forms.py	Falta coma entre strings en fields → concatenación	Agregar ,
18.	forms.py	widgets fuera de Meta	Movido dentro de Meta
19.	Varias vistas	UnboundLocalError en form/contexto	Inicializar antes del if/else
📊 Resumen Final
19. errores corregidos distribuidos en 6 categorías.

🔑 Causas raíz más comunes
🏷️ Mezcla de nombres entre vista, template y test.

🔀 Confusión singular/plural en variables de contexto.

📦 Variables no inicializadas en todas las rutas del código.

⚠️ Errores críticos
403 Forbidden en tests → faltaba is_staff=True.

UnboundLocalError → variable usada sin definir.

NoReverseMatch → name de URL incorrecto.

