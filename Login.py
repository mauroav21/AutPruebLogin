import os
import time
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def iniciar_automatizacion():
    ruta_archivo = filedialog.askopenfilename(
        title="Seleccionar archivo de usuarios",
        filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
    )

    if not ruta_archivo:
        return

    # 1. CREAR CARPETA DE EVIDENCIAS si no existe
    folder_evidencias = "evidencias_login"
    if not os.path.exists(folder_evidencias):
        os.makedirs(folder_evidencias)

    # 2. Configuración del Driver (Asegúrate de que esta ruta sea correcta)
    edge_driver_path = r'C:\dedge\msedgedriver.exe'
    service = Service(executable_path=edge_driver_path)
    driver = None

    try:
        with open(ruta_archivo, 'r') as f:
            lineas = f.readlines()

        driver = webdriver.Edge(service=service)
        
        for num, linea in enumerate(lineas, 1):
            linea = linea.strip()
            if not linea or ',' not in linea:
                continue
            
            usuario, contrasena = linea.split(',')
            print(f"[{num}] Probando login para: {usuario}")

            try:
                driver.get("http://localhost:4200/login")
                wait = WebDriverWait(driver, 10)
                
                # Interacción con los elementos identificados
                campo_user = wait.until(EC.presence_of_element_located((By.ID, "email")))
                campo_user.clear()
                campo_user.send_keys(usuario)

                campo_pwd = driver.find_element(By.ID, 'password')
                campo_pwd.clear()
                campo_pwd.send_keys(contrasena)

                boton_login = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                boton_login.click()

                # Espera para que cargue la respuesta
                time.sleep(2)

                # 3. GENERAR CAPTURA DE PANTALLA (Evidencia)
                nombre_foto = f"evidencia_{usuario}_{int(time.time())}.png"
                ruta_foto = os.path.join(folder_evidencias, nombre_foto)
                driver.save_screenshot(ruta_foto)
                print(f"Captura guardada: {nombre_foto}")

                driver.delete_all_cookies()

            except Exception as error_usuario:
                print(f"Error con usuario {usuario}: {error_usuario}")
                # Captura de pantalla del fallo para el reporte
                driver.save_screenshot(os.path.join(folder_evidencias, f"ERROR_{usuario}.png"))
                continue

        messagebox.showinfo("Proceso Completo", f"Pruebas finalizadas.\nRevisa la carpeta: {folder_evidencias}")

    except Exception as e:
        messagebox.showerror("Error General", f"Ocurrió un error: {e}")
    finally:
        if driver:
            driver.quit()

# --- Interfaz Gráfica Corregida ---
ventana = tk.Tk()
ventana.title("autprueb login")
ventana.geometry("350x200")
ventana.configure(bg="#f0f4f7")

style = ttk.Style()
style.configure("TFrame", background="#f0f4f7")
style.configure("TLabel", background="#f0f4f7", font=("Segoe UI", 11))

frame = ttk.Frame(ventana, padding=30)
frame.pack(expand=True)

ttk.Label(frame, text="autprueb login", font=("Segoe UI", 14, "bold")).pack(pady=10)
ttk.Button(frame, text="Cargar Usuarios e Iniciar", command=iniciar_automatizacion).pack(pady=20)

ventana.mainloop()