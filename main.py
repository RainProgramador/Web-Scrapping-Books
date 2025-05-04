# -*- coding: utf-8 -*-

import os
import selenium
import time
from selenium import webdriver
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

# Ocultar logs de TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Configurar la carpeta de descargas
ruta_descargas = os.path.join(os.path.expanduser("~"), "Documents", "LibrosDescargados")
if not os.path.exists(ruta_descargas):
    os.makedirs(ruta_descargas)

def esperar_descarga_completa(carpeta_descargas, tiempo_espera=60):
    """
    Espera a que se complete la descarga en la carpeta especificada.
    """
    tiempo_transcurrido = 0
    while tiempo_transcurrido < tiempo_espera:
        archivos = os.listdir(carpeta_descargas)
        # Verificar si hay algún archivo con extensión .crdownload (descarga en curso)
        if not any(archivo.endswith(".crdownload") for archivo in archivos):
            return True  # Descarga completada
        time.sleep(1)
        tiempo_transcurrido += 1
    return False  # Tiempo de espera agotado

#Mensaje de bienvenida
#En el mensaje de bienvenida se le da la bienvenida al usuario y se le explica brevemente la aplicacion
#Tambien se imprime en codigo ascci RAEN

MensajeDeBienvenida = """\n

Bienvenido Usuario
Esta es la version 1.0 de la aplicacion Buscador de libros

Esta aplicacion te permitira buscar libros en la pagina web Libgen
- https://libgen.is/

Se creara una carpeta en Documentos\LibrosDescargados
En esta carpeta se guardaran los libros que descargues
Si no tienes la carpeta, se creara automaticamente

Esta aplicacion fue creada por Rain
Si tienes alguna duda o sugerencia, no dudes en contactarme
Espero te guste
Jijiji
"""
print(MensajeDeBienvenida)
time.sleep(10)

#Limpia la consola
os.system('cls' if os.name == 'nt' else 'clear')

# Solicitar el nombre del libro al usuario
NombreDelLibro = input("\n[+] ¿Qué libro deseas buscar?: ")

def BuscadorDeLibros():
    # Configurar opciones de Chrome para descargas automáticas
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1280,720")
    #options.add_argument("--incognito")
    options.add_argument("--headless=new")  # Ejecutar Chrome en segundo plano
    options.add_argument("--disable-gpu")  # Deshabilitar GPU (recomendado para headless)
    options.add_argument("--no-sandbox")   # Requerido en algunos entornos
    options.add_argument("--disable-dev-shm-usage")  # Evitar problemas de memoria compartida

    prefs = {
        "download.default_directory": ruta_descargas,  # Carpeta de descargas
        "download.prompt_for_download": False,         # No preguntar por la ubicación
        "download.directory_upgrade": True,           # Actualizar automáticamente la carpeta de descargas
        "safebrowsing.enabled": True                  # Habilitar descargas seguras
    }
    options.add_experimental_option("prefs", prefs)

    # Inicializar el WebDriver
    service = Service(ChromeDriverManager().install(), log_path=os.devnull)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://libgen.is/")

    # Buscar el libro
    search_input = driver.find_element(By.NAME, "req")
    search_input.send_keys(NombreDelLibro)
    search_input.submit()

    try:
        # Esperar a que los títulos de los libros estén presentes
        titles = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//td[@width='500']/a"))
        )
        print("\n[+] Libros encontrados: ")

        # Mostrar los títulos con índices
        libros = []
        for index, title in enumerate(titles, start=1):
            raw_text = title.get_attribute("innerHTML")
            libro_titulo = raw_text.split("<br>")[0].strip()
            libro_titulo = libro_titulo.split("<font")[0].strip()
            libros.append((index, libro_titulo, title.get_attribute("href")))
            print(f"{index}. {libro_titulo}")

        # Permitir al usuario elegir un libro
        if libros:
            try:
                seleccion = int(input("\n[+] Ingresa el número del libro que deseas seleccionar: "))
                if 1 <= seleccion <= len(libros):
                    libro_seleccionado = libros[seleccion - 1]
                    print(f"\n[+] Has seleccionado: {libro_seleccionado[1]}")
                    print(f"[+] Enlace del libro: {libro_seleccionado[2]}")

                    # Navegar al enlace del libro seleccionado
                    driver.get(libro_seleccionado[2])

                    # Buscar y hacer clic en el primer enlace de descarga
                    enlace_descarga = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "/html/body/table/tbody/tr[18]/td[2]/table/tbody/tr/td[1]"))
                    )
                    enlace_descarga.click()

                    # Buscar y hacer clic en el enlace final de descarga
                    enlace_final = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//*[@id='download']/h2[1]/a"))
                    )
                    enlace_final.click()

                    print(f"\n[+] El libro se está descargando en: {ruta_descargas}")

                    # Esperar a que la descarga se complete
                    print("\n[+] Esperando a que se complete la descarga...")
                    if esperar_descarga_completa(ruta_descargas):
                        time.sleep(30)
                        print("\n[+] Descarga completada con éxito.")
                    else:
                        print("\n[-] La descarga no se completó dentro del tiempo esperado.")
                else:
                    print("\n[-] Selección inválida. Por favor, intenta de nuevo.")
            except ValueError:
                print("\n[-] Entrada inválida. Por favor, ingresa un número.")
        else:
            print("\n[-] No se encontraron libros.")
    except Exception as e:
        print("\n[-] Error al buscar los libros:", str(e))
    finally:
        print("\n[+] Cerrando el navegador...")
        time.sleep(5)
        driver.quit()

BuscadorDeLibros()
