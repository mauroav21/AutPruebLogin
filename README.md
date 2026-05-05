# autprueb login 🚀

Herramienta de automatización para pruebas de acceso y llenado de formularios masivo utilizando **Python**, **Selenium** y **Tkinter**. Este script permite procesar múltiples credenciales de forma secuencial a partir de un archivo de origen externo.

## 📋 Características

- **Carga por Lote:** Procesa una lista de usuarios y contraseñas desde un archivo `.txt`.
- **Interfaz Intuitiva:** GUI minimalista para facilitar la selección de archivos sin modificar el código.
- **Flujo de Navegación:** Automatiza el login en `localhost:4200` y gestiona la navegación interna de la plataforma.
- **Gestión de Sesiones:** Limpieza automática de cookies entre cada usuario para garantizar entornos de prueba limpios.
- **Logs y Capturas:** Registro de progreso en consola y capturas de pantalla automáticas en caso de fallos.

## 🛠️ Tecnologías Utilizadas

* [Python](https://www.python.org/) - Lógica del sistema.
* [Selenium](https://www.selenium.dev/) - Motor de automatización del navegador.
* [Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/driver/) - Driver de comunicación con MS Edge.
* [Tkinter](https://docs.python.org/3/library/tkinter.html) - Interfaz de usuario.

## 🚀 Configuración Inicial

### 1. Requisitos
Instala las dependencias necesarias con pip:

```bash
pip install selenium