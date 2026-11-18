# 👗 FashionDB – Sistema de Gestión para la Industria de la Moda

## 📌 Descripción del proyecto

FashionDB es una aplicación de escritorio desarrollada en Python con Tkinter y MongoDB, diseñada para gestionar la información de una empresa de moda.

El sistema permite administrar prendas, colecciones, diseñadores, vendedores, tiendas, talleres y ventas, facilitando el control del inventario y la consulta de información comercial.

## 🎯 Objetivo

Desarrollar un sistema de gestión que permita organizar y administrar la información de una empresa de moda mediante una interfaz gráfica y una base de datos NoSQL.

## 🛠️ Tecnologías utilizadas

- **Python:** lenguaje de programación.
- **Tkinter:** desarrollo de la interfaz gráfica.
- **MongoDB:** sistema de gestión de base de datos NoSQL.
- **MongoDB Compass:** administración visual de la base de datos.
- **PyMongo:** conexión entre Python y MongoDB.
- **tkcalendar:** selección de fechas mediante calendario.

## 🚀 Funcionalidades principales

### 👚 Gestión de prendas
- Registrar nuevas prendas.
- Editar información de prendas.
- Eliminar prendas.
- Buscar prendas por referencia.
- Consultar inventario disponible.

### 📦 Gestión de información
- Consultar colecciones.
- Consultar diseñadores.
- Consultar vendedores.
- Consultar tiendas.
- Consultar talleres.

### 📊 Reportes y consultas
- Reportes de ingresos por colección.
- Consulta de existencias por talla.
- Consulta de prendas por diseñador.
- Consulta de prendas con precios altos.
- Consulta de diseñadores por ciudad.
- Consulta de ventas por tienda y vendedor.

### 📅 Gestión de fechas
- Selección de fechas mediante calendario.
- Consulta de información relacionada con fechas.

## 🗄️ Base de datos

**Nombre de la base de datos:** `fashiondb`

La base de datos está desarrollada en MongoDB y almacena la información del sistema mediante colecciones.

Entre las colecciones del proyecto se encuentran:

- `prendas`
- `colecciones`
- `disenadores`
- `vendedores`
- `tiendas`
- `talleres`
- `ventas`

## ⚙️ Requisitos para ejecutar el proyecto

Antes de ejecutar FashionDB, es necesario tener instalado:

1. Python.
2. MongoDB.
3. MongoDB Compass (opcional, para administrar visualmente la base de datos).
4. PyCharm u otro editor compatible con Python.

## 📥 Instalación

### 1. Clonar el repositorio

```bash
git clone URL_DE_TU_REPOSITORIO
```

### 2. Ingresar a la carpeta del proyecto

```bash
cd FashionDB
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Verificar MongoDB

Comprobar que el servicio de MongoDB esté funcionando correctamente.

La conexión local utilizada por el proyecto es:

```python
mongodb://localhost:27017/
```

### 5. Ejecutar la aplicación

Abrir el proyecto en PyCharm y ejecutar el archivo principal de Python.

## 🖼️ Icono de la aplicación

El proyecto incluye un icono personalizado llamado `fashion_icon.ico`, utilizado en la ventana principal de FashionDB.

## 📁 Estructura del proyecto

```text
FashionDB/
│
├── README.md
├── requirements.txt
├── .gitignore
├── main.py
├── fashion_icon.ico
│
└── database/
    ├── prendas.json
    ├── colecciones.json
    ├── disenadores.json
    ├── vendedores.json
    ├── tiendas.json
    ├── talleres.json
    └── ventas.json
```

*Nota: Los archivos JSON de la carpeta `database` corresponden a exportaciones de las colecciones de MongoDB, si se incluyen en el repositorio.*

## 👨‍🎓 Información del estudiante

- **Estudiante:** Andres Vargas
- **Institución:** CEFIT
- **Programa:** Auxiliar de Programación y Desarrollo de Software

## 📚 Tipo de proyecto

Proyecto académico desarrollado como parte del proceso de formación en programación y desarrollo de software.

---

**FashionDB – Sistema de Gestión para la Industria de la Moda** 👗