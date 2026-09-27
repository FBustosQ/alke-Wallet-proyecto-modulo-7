# Proyecto Módulo 6 - Alke Wallet

## 📝 Descripción

**Aplicación web de billetera virtual.** Permite a los usuarios organizar sus cuentas, transacciones y los clientes para el administrador.

## 🚀 Características Principales

* **Gestión de Usuarios:** Registro, inicio de sesión y control de acceso seguro.
* **Control Multiusuario (Multi-tenant):** Los usuarios solo pueden visualizar, editar y gestionar sus propios proyectos y tareas.
* **Operaciones CRUD Completas:** Control total (Crear, Leer, Actualizar y Eliminar) tanto para proyectos como para tareas dependientes.
* **Interfaz Responsiva:** Diseño adaptable a dispositivos móviles y de escritorio.

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python, Django
* **Base de datos:** SQLlite
* **Frontend:** HTML5, CSS3, Bootstrap 4
* **Entorno de Desarrollo:** Linux

## ⚙️ Instalación y Configuración

Sigue estos pasos para configurar el entorno de desarrollo local:

### 1. Clonar el repositorio
```bash
git clone https://github.com
cd proyecto-modulo-7
```

### 2. Configurar el Entorno Virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install --upgrade pip
pip install -r enviroment.txt
```

### 4. Aplicar migraciones de la Base de Datos
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

## 🖥️ Ejecución del Proyecto

Para iniciar el servidor de desarrollo local, ejecuta el siguiente comando en la terminal:

```bash
python3 manage.py runserver
```

Luego, abre tu navegador web e ingresa a la dirección: [http://127.0.0](http://127.0.0)

## Explicación de la aplicacion

Base de Datos
Se utilizó SQLite (motor por defecto de Django), configurado en settings.py mediante el diccionario DATABASES. Al ser un archivo local (db.sqlite3), no requiere servidor externo, ideal para desarrollo. Las tablas se generan automáticamente con makemigrations y migrate, que traducen los modelos Python a SQL.

Estas son las migraciones que se han realizado:

![migraciones 1 ](/static/img/migraciones1.png)
![migraciones 2](/static/img/migraciones2.png)
![migraciones 3](/static/img/migraciones3.png)
![migraciones 4](/static/img/migraciones4.png)


Modelos
Se definieron tres modelos en gestion/models.py usando el ORM de Django:

Cliente: almacena datos personales (nombre, email único, teléfono) y fecha de registro automática.

Cuenta: se relaciona con Cliente mediante OneToOneField (una cuenta por cliente) y con otros clientes mediante ManyToManyField como contactos autorizados. Incluye una propiedad saldo que calcula ingresos menos egresos usando Sum.

Transaccion: se vincula a Cuenta con ForeignKey y registra tipo (ingreso/egreso) y monto. Usa choices para restringir valores y on_delete=PROTECT para evitar borrados accidentales.

Las relaciones usan related_name para acceder desde el modelo inverso (ej: cliente.cuenta, cuenta.transacciones), y Meta define ordenamientos y nombres legibles en el admin.

Los modelos:

![modelos](/static/img/modelo1.png)

![modelos](/static/img/modelo2.png)

## Demostración de la aplicacion

Las siguientes capturas muestran el panel de administración de Django, donde se gestionan los modelos Cliente, Cuenta y Transaccion. En ellas se aprecia la interfaz autogenerada por el framework, incluyendo listados, formularios de edición y validaciones configuradas. Admeas se muestran las acciones CRUD, para cada uno de los modelos.

### Interfaz Administración 

![interzas admin](/static/img/admin1.png)
![interzas admin](/static/img/admin2.png)
![interzas admin](/static/img/admin3.png)
![interzas admin](/static/img/admin4.png)

### Interfaz Administración CRUD

#### Crear
![interzas admin crear](/static/img/admin-create1.png)
![interzas admin crear](/static/img/admin-create2.png)
![interzas admin crear](/static/img/admin-create3.png)
![interzas admin crear](/static/img/admin-create4.png)
![interzas admin crear](/static/img/admin-create5.png)

#### Editar

![interzas admin editar](/static/img/admin-editar.png)
![interzas admin editar](/static/img/admin-editar2.png)

#### Eliminar

![interzas admin eliminar](/static/img/admin-delete1.png)
![interzas admin eliminar](/static/img/admin-delete2.png)
![interzas admin eliminar](/static/img/admin-delete3.png)
![interzas admin eliminar](/static/img/admin-delete4.png)
![interzas admin eliminar](/static/img/admin-delete5.png)
![interzas admin eliminar](/static/img/admin-delete6.png)

#### Ver

Si bien el apartado administrativo de django permite la visualización de los objetos, la vista generada del tempalte es :

![template ver detalle cliente](/static/img/template.png)


## 🧪 Pruebas Unitarias (Testing)

El proyecto cuenta con una suite automatizada de **28 pruebas unitarias** para asegurar la estabilidad del código.

* El desglose detallado de los casos de prueba se encuentra en el archivo `/tests/test-resumen.md`.
* Las capturas de pantalla con los resultados de las ejecuciones exitosas están disponibles en la carpeta `tests/screenshots/`.

Para volver a ejecutar la suite de pruebas localmente:
```bash
python3 manage.py test tareas
```

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT**. Puedes usarlo, modificarlo y distribuirlo libremente, incluso para fines comerciales.

---

### MIT License

Copyright (c) 2026 Francisca Bustos

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 📬 Contacto y Soporte

* **Desarrolladora:** Francisca Bustos
* **Correo electrónico:** fran.bustos.quezada@gmail.com
