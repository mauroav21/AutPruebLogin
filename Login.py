import os
import time
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def procesar_encuesta(driver):
    """
    Aquí colocas toda la lógica que ya tenías para navegar por 
    las preguntas, hacer clic en '5' y dar en 'Continuar'.
    """
    # (Mantén aquí tu bucle 'while True' y la lógica de los paneles que ya escribiste)
    print("Ejecutando lógica de encuesta...")
    time.sleep(2) # Simulación

def iniciar_automatizacion():
    # 1. Seleccionar el archivo TXT
    ruta_archivo = filedialog.askopenfilename(
        title="Seleccionar archivo de usuarios",
        filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
    )

    if not ruta_archivo:
        return

    # 2. Configuración del Driver
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
            print(f"[{num}] Procesando: {usuario}")

            # Ir al login local
            driver.get("http://localhost:4200/login")

            # Login con los nuevos IDs
            wait = WebDriverWait(driver, 15)
            
            campo_user = wait.until(EC.presence_of_element_located((By.ID, "email")))
            campo_user.clear()
            campo_user.send_keys(usuario)

            campo_pwd = driver.find_element(By.ID, 'password')
            campo_pwd.clear()
            campo_pwd.send_keys(contrasena)

            # Si el botón no tiene ID, lo buscamos por el tipo submit o clase
            boton_login = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            boton_login.click()

            # --- Lógica de la encuesta ---
            # Llamamos a la función que procesa las preguntas
            procesar_encuesta(driver)
            
            # Limpiar sesión para el siguiente usuario
            driver.delete_all_cookies()
            print(f"Usuario {usuario} finalizado.\n")

        messagebox.showinfo("Proceso Completo", "Se han procesado todos los usuarios del archivo.")

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")
    finally:
        if driver:
            driver.quit()

# --- Interfaz Gráfica Minimalista ---
ventana = tk.Tk()
ventana.title("Selenium Multi-User")
ventana.geometry("350x200")
ventana.configure(bg="#f0f4f7")

frame = ttk.Frame(ventana, padding=30)
frame.pack(expand=True)

ttk.Label(frame, text="Automatización de Encuestas", font=("Segoe UI", 12, "bold")).pack(pady=10)
ttk.Button(frame, text="Cargar TXT e Iniciar", command=iniciar_automatizacion).pack(pady=20)

ventana.mainloop()