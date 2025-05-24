# scraper/libgen_scraper.py
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from config import RUTA_DESCARGAS
from utils.downloader import esperar_descarga_completa

def iniciar_driver():
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,720")
    # Configuración de descargas
    prefs = {"download.default_directory": RUTA_DESCARGAS}
    options.add_experimental_option("prefs", prefs)
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def buscar_y_descargar(nombre_libro):
    driver = iniciar_driver()
    driver.get("https://libgen.is/")

    # Ingresar término de búsqueda
    search_input = driver.find_element(By.NAME, "req")
    search_input.send_keys(nombre_libro)
    search_input.submit()

    try:
        # Esperar y obtener resultados
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, "//td[@width='500']/a"))
        )
        titles = driver.find_elements(By.XPATH, "//td[@width='500']/a")
        libros = []
        for i, title in enumerate(titles, 1):
            raw = title.get_attribute("innerHTML")
            titulo = raw.split("<br>")[0].split("<font")[0].strip()
            enlace = title.get_attribute("href")
            libros.append((i, titulo, enlace))
            print(f"{i}. {titulo}")

        if not libros:
            print("[-] No se encontraron libros para ese término.")
            return None, None

        seleccion = int(input("Selecciona un libro por número: "))
        elegido = libros[seleccion - 1]
        print(f"Descargando: {elegido[1]}")
        driver.get(elegido[2])

        # Intentar hacer clic en el enlace de descarga principal
        try:
            descarga = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/table/tbody/tr[18]/td[2]/table/tbody/tr/td[1]/a"))
            )
            descarga.click()
        except Exception:
            # Fallback: intentar con otro selector
            print("[!] Selector de descarga principal falló, usando fallback...")
            enlaces = driver.find_elements(By.CSS_SELECTOR, "#download a")
            if enlaces:
                enlaces[0].click()
            else:
                print("[-] No se encontró enlace de descarga final.")
                return elegido[1], elegido[2]

        # Segundo paso: enlace final
        try:
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#download a"))
            )
            final = driver.find_element(By.CSS_SELECTOR, "#download a")
            final.click()
        except Exception:
            print("[-] No se pudo hacer clic en el enlace final de descarga.")
            return elegido[1], elegido[2]

        ruta_archivo = esperar_descarga_completa(RUTA_DESCARGAS)
        if ruta_archivo:
            print(f"Descarga completada: {ruta_archivo}")
        else:
            print("La descarga falló o tardó demasiado.")

        return elegido[1], elegido[2]

    finally:
        driver.quit()
