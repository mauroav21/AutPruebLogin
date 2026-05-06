import os
import time
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# --- FUNCIONES DE APOYO ---

def generar_log(usuario, resultado, detalle=""):
    """Escribe el resultado de la prueba en un archivo .log"""
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("reporte_pruebas.log", "a", encoding="utf-8") as f:
        f.write(f"[{fecha_hora}] USUARIO: {usuario} | RESULTADO: {resultado} | {detalle}\n")

def iniciar_automatizacion():
    ruta_archivo = filedialog.askopenfilename(
        title="Seleccionar archivo de usuarios",
        filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
    )

    if not ruta_archivo:
        return

    folder_evidencias = "evidencias_login"
    if not os.path.exists(folder_evidencias):
        os.makedirs(folder_evidencias)

    edge_driver_path = r'C:\dedge\msedgedriver.exe'
    service = Service(executable_path=edge_driver_path)
    driver = None

    try:
        with open(ruta_archivo, 'r') as f:
            lineas = f.readlines()

        with open("reporte_pruebas.log", "a", encoding="utf-8") as f:
            f.write(f"\n--- NUEVA SESIÓN DE PRUEBAS: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")

        driver = webdriver.Edge(service=service)
        wait = WebDriverWait(driver, 10)
        
        for num, linea in enumerate(lineas, 1):
            linea = linea.strip()
            if not linea or ',' not in linea:
                continue
            
            usuario, contrasena = linea.split(',')
            print(f"[{num}] Evaluando: {usuario}")

            try:
                driver.get("http://localhost:4200/login")
                
                # Proceso de Login
                campo_user = wait.until(EC.presence_of_element_located((By.ID, "email")))
                campo_user.clear()
                campo_user.send_keys(usuario)

                campo_pwd = driver.find_element(By.ID, 'password')
                campo_pwd.clear()
                campo_pwd.send_keys(contrasena)

                driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

                # --- VALIDACIÓN DE RESULTADO REAL ---
                # Esperamos a ver si la URL cambia (indicativo de éxito)
                # Si en 5 segundos no cambia, asumimos que el login falló
                try:
                    # Ajusta 'dashboard' por una palabra que aparezca en tu URL al entrar
                    WebDriverWait(driver, 5).until(EC.url_contains("dashboard"))
                    
                    # CASO: LOGIN CORRECTO
                    resultado_status = "ÉXITO"
                    detalle_log = "Acceso concedido. Redirección exitosa."
                    prefijo_foto = "EXITO"
                except:
                    # CASO: LOGIN INCORRECTO (No redirigió)
                    resultado_status = "ACCESO DENEGADO"
                    detalle_log = "Credenciales inválidas o falta de redirección."
                    prefijo_foto = "DENEGADO"

                # Guardar Evidencia con el estado real
                nombre_foto = f"{prefijo_foto}_{usuario}.png"
                driver.save_screenshot(os.path.join(folder_evidencias, nombre_foto))
                
                # Registrar en Log
                generar_log(usuario, resultado_status, detalle_log)
                
                driver.delete_all_cookies()

            except Exception as e:
                print(f"Error técnico con {usuario}")
                generar_log(usuario, "ERROR TÉCNICO", str(e))
                driver.save_screenshot(os.path.join(folder_evidencias, f"ERROR_TECNICO_{usuario}.png"))
                continue

        messagebox.showinfo("Proceso Completo", "Pruebas finalizadas.\nRevisa 'reporte_pruebas.log' y la carpeta de evidencias.")

    except Exception as e:
        messagebox.showerror("Error General", f"Fallo al iniciar el sistema: {e}")
    finally:
        if driver:
            driver.quit()

# --- Interfaz Gráfica ---
ventana = tk.Tk()
ventana.title("autprueb login")
ventana.geometry("400x250")
ventana.configure(bg="#f0f4f7")

style = ttk.Style()
style.configure("TFrame", background="#f0f4f7")
style.configure("TLabel", background="#f0f4f7")

frame = ttk.Frame(ventana, padding=30)
frame.pack(expand=True)

ttk.Label(frame, text="AUTPRUEB LOGIN", font=("Segoe UI", 14, "bold")).pack(pady=5)
ttk.Label(frame, text="QA Automation Tool", font=("Segoe UI", 9)).pack(pady=5)

ttk.Button(frame, text="Ejecutar Pruebas Masivas", command=iniciar_automatizacion).pack(pady=20)

# Información de ayuda en la interfaz
ttk.Label(frame, text="Logs: reporte_pruebas.log", font=("Segoe UI", 8, "italic")).pack()

ventana.mainloop()