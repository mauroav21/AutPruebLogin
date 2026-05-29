import os
import sys
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Debug flag
DEBUG = '--debug' in sys.argv or os.getenv('DEBUG', '').lower() == 'true'

def debug_print(mensaje):
    """Print debug message only if DEBUG flag is enabled"""
    if DEBUG:
        print(f"  [DEBUG] {mensaje}")

# --- FUNCIONES DE APOYO ---

def generar_log(usuario, resultado, detalle=""):
    """Escribe el resultado de la prueba en un archivo .log"""
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("reporte_pruebas.log", "a", encoding="utf-8") as f:
        f.write(f"[{fecha_hora}] USUARIO: {usuario} | RESULTADO: {resultado} | {detalle}\n")

def iniciar_automatizacion(ruta_archivo):
    """Ejecuta las pruebas de login de forma automatizada (headless)"""
    if not os.path.exists(ruta_archivo):
        print(f"Error: El archivo {ruta_archivo} no existe")
        return False

    folder_evidencias = "evidencias_login"
    if not os.path.exists(folder_evidencias):
        os.makedirs(folder_evidencias)

    driver = None

    try:
        with open(ruta_archivo, 'r') as f:
            lineas = f.readlines()

        with open("reporte_pruebas.log", "a", encoding="utf-8") as f:
            f.write(f"\n--- NUEVA SESIÓN DE PRUEBAS: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")

        # Configurar Firefox en modo headless
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Firefox(options=firefox_options)
        wait = WebDriverWait(driver, 10)
        
        for num, linea in enumerate(lineas, 1):
            linea = linea.strip()
            if not linea or ',' not in linea:
                continue
            
            usuario, contrasena = linea.split(',')
            print(f"[{num}] Evaluando: {usuario}")

            try:
                driver.get("http://localhost:4200/login")
                
                # Wait for page to fully load
                wait.until(EC.presence_of_element_located((By.ID, "email")))
                debug_print("Page loaded, entering credentials...")
                
                # Proceso de Login
                campo_user = driver.find_element(By.ID, "email")
                campo_user.clear()
                campo_user.send_keys(usuario)
                debug_print("Username entered")

                campo_pwd = driver.find_element(By.ID, 'password')
                campo_pwd.clear()
                campo_pwd.send_keys(contrasena)
                debug_print("Password entered")

                # Wait for CAPTCHA token to be set (mock token for testing)
                # Look for a hidden input or data attribute that holds the token
                try:
                    # Try to wait for mock token to be set (usually in a hidden field)
                    time.sleep(0.5)  # Give the CAPTCHA component time to emit the token
                    debug_print("Waiting for CAPTCHA token...")
                    
                    # Check if there's a captcha token input or if form is ready
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']:not(:disabled)"))
                    )
                    debug_print("Submit button is ready")
                except:
                    debug_print("Submit button check timed out, proceeding anyway")

                # Click submit button and wait a bit for JS to execute
                submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                submit_btn.click()
                debug_print("Submit clicked")

                # --- VALIDACIÓN DE RESULTADO REAL ---
                # Wait longer and check multiple conditions
                try:
                    # Wait up to 10 seconds for redirect
                    WebDriverWait(driver, 10).until(EC.url_contains("dashboard"))
                    debug_print("Redirected to dashboard")
                    
                    # CASO: LOGIN CORRECTO
                    resultado_status = "ÉXITO"
                    detalle_log = "Acceso concedido. Redirección exitosa."
                    prefijo_foto = "EXITO"
                except:
                    # Check if there's an error message on the page
                    current_url = driver.current_url
                    page_title = driver.title
                    page_source = driver.page_source
                    
                    # Look for common error messages (adjust selectors to your app)
                    error_message = ""
                    try:
                        # Try common error element selectors
                        error_elem = driver.find_element(By.CSS_SELECTOR, ".error, [class*='error'], [class*='alert']")
                        error_message = error_elem.text
                        debug_print(f"Error found on page: {error_message}")
                    except:
                        pass
                    
                    debug_print(f"Redirect failed. URL: {current_url}, Title: {page_title}")
                    if error_message:
                        debug_print(f"Error message: {error_message}")
                    
                    # CASO: LOGIN INCORRECTO (No redirigió)
                    resultado_status = "ACCESO DENEGADO"
                    detalle_log = f"Credenciales inválidas o falta de redirección. Error: {error_message or 'Sin mensaje de error'}"
                    prefijo_foto = "DENEGADO"

                # Guardar Evidencia con el estado real
                nombre_foto = f"{prefijo_foto}_{usuario}.png"
                driver.save_screenshot(os.path.join(folder_evidencias, nombre_foto))
                debug_print(f"Screenshot saved: {nombre_foto}")
                
                # Registrar en Log
                generar_log(usuario, resultado_status, detalle_log)
                
                # Don't delete cookies immediately, add small delay
                import time
                time.sleep(1)
                driver.delete_all_cookies()

            except Exception as e:
                print(f"Error técnico con {usuario}: {str(e)}")
                generar_log(usuario, "ERROR TÉCNICO", str(e))
                try:
                    driver.save_screenshot(os.path.join(folder_evidencias, f"ERROR_TECNICO_{usuario}.png"))
                except:
                    pass
                continue

        print("Pruebas finalizadas. Revisa 'reporte_pruebas.log' y la carpeta de evidencias.")
        return True

    except Exception as e:
        print(f"Error General: {e}")
        return False
    finally:
        if driver:
            driver.quit()

# --- PUNTO DE ENTRADA ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: uv run python Login.py <archivo_usuarios.txt>")
        print("Ejemplo: uv run python Login.py usuarios.txt")
        sys.exit(1)
    
    archivo_usuarios = sys.argv[1]
    exitoso = iniciar_automatizacion(archivo_usuarios)
    sys.exit(0 if exitoso else 1)