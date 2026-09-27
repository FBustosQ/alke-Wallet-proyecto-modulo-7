# gestion/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal

from .models import Cliente, Cuenta, Transaccion


# ============================================
# PRUEBAS DE MODELOS
# ============================================

class ClienteModelTest(TestCase):
    """Pruebas para el modelo Cliente"""

    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombre='Juan Pérez',
            email='juan@test.com',
            telefono='+56912345678'
        )

    def test_cliente_creado_correctamente(self):
        """El cliente se crea con los datos correctos"""
        self.assertEqual(self.cliente.nombre, 'Juan Pérez')
        self.assertEqual(self.cliente.email, 'juan@test.com')
        self.assertEqual(self.cliente.telefono, '+56912345678')

    def test_cliente_str(self):
        """El __str__ del cliente devuelve el nombre"""
        self.assertEqual(str(self.cliente), 'Juan Pérez')

    def test_cliente_fecha_registro(self):
        """El cliente tiene fecha de registro automática"""
        self.assertIsNotNone(self.cliente.fecha_registro)

    def test_cliente_email_unico(self):
        """No se pueden crear dos clientes con el mismo email"""
        with self.assertRaises(Exception):
            Cliente.objects.create(
                nombre='Otro',
                email='juan@test.com',
                telefono='+56999999999'
            )

    def test_clientes_ordenados_por_nombre(self):
        """Los clientes se ordenan por nombre por defecto"""
        Cliente.objects.create(nombre='Ana', email='a@test.com', telefono='1')
        Cliente.objects.create(nombre='Zoe', email='z@test.com', telefono='2')

        nombres = list(Cliente.objects.values_list('nombre', flat=True))
        self.assertEqual(nombres, sorted(nombres))


class CuentaModelTest(TestCase):
    """Pruebas para el modelo Cuenta"""

    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombre='Juan Pérez',
            email='juan@test.com',
            telefono='+56912345678'
        )
        self.cuenta = Cuenta.objects.create(
            cliente=self.cliente,
            numero='CTA-001'
        )

    def test_cuenta_creada_correctamente(self):
        self.assertEqual(self.cuenta.cliente, self.cliente)
        self.assertEqual(self.cuenta.numero, 'CTA-001')

    def test_cuenta_str(self):
        """El __str__ muestra cliente | numero"""
        self.assertEqual(str(self.cuenta), 'Juan Pérez | CTA-001')

    def test_cuenta_numero_unico(self):
        """No se pueden crear dos cuentas con el mismo número"""
        otro = Cliente.objects.create(
            nombre='Otro', email='o@test.com', telefono='2'
        )
        with self.assertRaises(Exception):
            Cuenta.objects.create(cliente=otro, numero='CTA-001')

    def test_saldo_sin_transacciones_es_cero(self):
        """Sin transacciones, el saldo es 0"""
        self.assertEqual(self.cuenta.saldo, Decimal('0'))

    def test_saldo_con_ingresos(self):
        """Con ingresos, el saldo es la suma de ellos"""
        Transaccion.objects.create(
            cuenta=self.cuenta, tipo='ingreso', monto=10000
        )
        Transaccion.objects.create(
            cuenta=self.cuenta, tipo='ingreso', monto=5000
        )
        self.assertEqual(self.cuenta.saldo, Decimal('15000'))

    def test_saldo_con_ingresos_y_egresos(self):
        """El saldo es ingresos menos egresos"""
        Transaccion.objects.create(cuenta=self.cuenta, tipo='ingreso', monto=10000)
        Transaccion.objects.create(cuenta=self.cuenta, tipo='egreso', monto=3000)
        self.assertEqual(self.cuenta.saldo, Decimal('7000'))

    def test_contactos_autorizados_m2m(self):
        """Se pueden agregar contactos autorizados"""
        contacto = Cliente.objects.create(
            nombre='María', email='maria@test.com', telefono='3'
        )
        self.cuenta.contactos_autorizados.add(contacto)
        self.assertIn(contacto, self.cuenta.contactos_autorizados.all())


class TransaccionModelTest(TestCase):
    """Pruebas para el modelo Transaccion"""

    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombre='Juan', email='juan@test.com', telefono='1'
        )
        self.cuenta = Cuenta.objects.create(
            cliente=self.cliente, numero='CTA-001'
        )
        self.transaccion = Transaccion.objects.create(
            cuenta=self.cuenta,
            tipo='ingreso',
            monto=5000,
            descripcion='Depósito inicial'
        )

    def test_transaccion_creada_correctamente(self):
        self.assertEqual(self.transaccion.cuenta, self.cuenta)
        self.assertEqual(self.transaccion.tipo, 'ingreso')
        self.assertEqual(self.transaccion.monto, 5000)

    def test_transaccion_str(self):
        """El __str__ muestra tipo | monto"""
        self.assertEqual(str(self.transaccion), 'Ingreso | 5000')

    def test_transaccion_fecha_automatica(self):
        self.assertIsNotNone(self.transaccion.fecha)

    def test_tipos_validos(self):
        tipos_validos = ['ingreso', 'egreso']
        self.assertIn(self.transaccion.tipo, tipos_validos)

    def test_transaccion_cuenta_cascade(self):
        """Al eliminar la cuenta, se eliminan las transacciones"""
        cuenta_id = self.cuenta.pk
        # Nota: Cuenta usa PROTECT al eliminar Cliente, pero las
        # Transacciones SÍ usan PROTECT con Cuenta. Hay que borrarlas primero
        # o usar cascada si cambias el modelo. Aquí verificamos que el
        # borrado directo falla si hay transacciones (por PROTECT):
        with self.assertRaises(Exception):
            self.cuenta.delete()

    def test_transacciones_ordenadas_descendente(self):
        """Las transacciones se ordenan por fecha descendente"""
        Transaccion.objects.create(cuenta=self.cuenta, tipo='egreso', monto=1000)
        transacciones = list(Transaccion.objects.all())
        # La más nueva debe estar primero
        self.assertEqual(transacciones[0].monto, 1000)


# ============================================
# PRUEBAS DE VISTAS (asumiendo login requerido)
# ============================================

class ClienteViewsTest(TestCase):
    """Pruebas para las vistas de Cliente"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='Xk9$mPq2Lw7#', is_staff=True
        )
        self.otro_user = User.objects.create_user(
            username='otro', password='Xk9$mPq2Lw7#', is_staff=True
        )
        self.cliente = Cliente.objects.create(
            nombre='Juan Pérez',
            email='juan@test.com',
            telefono='+56912345678',
        )
        self.client = Client()
        self.client.login(username='testuser', password='Xk9$mPq2Lw7#')

    def test_lista_clientes_requiere_login(self):
        self.client.logout()
        response = self.client.get(reverse('lista_clientes'))
        self.assertEqual(response.status_code, 302)

    def test_lista_clientes_muestra_datos(self):
        response = self.client.get(reverse('lista_clientes'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juan Pérez')

    def test_lista_clientes_usa_template_correcto(self):
        response = self.client.get(reverse('lista_clientes'))
        self.assertTemplateUsed(response, 'gestion/lista_clientes.html')

    def test_detalle_cliente_muestra_datos(self):
        response = self.client.get(
            reverse('detalle_cliente', args=[self.cliente.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juan Pérez')

    def test_detalle_cliente_inexistente_da_404(self):
        response = self.client.get(
            reverse('detalle_cliente', args=[99999])
        )
        self.assertEqual(response.status_code, 404)

    def test_detalle_cliente_muestra_datos(self):
        response = self.client.get(reverse('detalle_cliente', args=[self.cliente.pk]))
        print("STATUS:", response.status_code)
        print("USER AUTH:", self.client.session.get('_auth_user_id'))
        self.assertEqual(response.status_code, 200)

# ============================================
# PRUEBAS DE URLs
# ============================================

class URLsTest(TestCase):
    """Pruebas de que las URLs resuelven correctamente"""

    def test_url_listado_clientes(self):
        self.assertEqual(reverse('lista_clientes'), '/')

    def test_url_detalle_cliente(self):
        self.assertEqual(
            reverse('detalle_cliente', args=[1]),
            '/clientes/1/'
        )

# ============================================
# PRUEBAS DE AUTENTICACIÓN
# ============================================

class AuthTest(TestCase):
    """Pruebas de login y logout"""

    def test_login_funciona(self):
        """El login funciona con credenciales correctas"""
        User.objects.create_user(username='test', password='Xk9$mPq2Lw7#')
        response = self.client.post(reverse('login'), {
            'username': 'test',
            'password': 'Xk9$mPq2Lw7#'
        })
        self.assertEqual(response.status_code, 302)

    def test_logout_funciona(self):
        """El logout funciona"""
        User.objects.create_user(username='test', password='pass1234')
        self.client.login(username='test', password='pass1234')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('lista_clientes'))
        self.assertEqual(response.status_code, 302)

    