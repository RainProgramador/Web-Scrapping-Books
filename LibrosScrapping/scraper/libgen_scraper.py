# scraper/libgen_scraper.py
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from config import RUTA_DESCARGAS
from utils.downloader import esperar_descarga_completa
from colorama import init, Fore, Style

# Inicializar colorama
init()

def print_success(texto):
    print(f"{Fore.GREEN}[✓] {texto}{Style.RESET_ALL}")

def print_error(texto):
    print(f"{Fore.RED}[!] {texto}{Style.RESET_ALL}")

def print_warning(texto):
    print(f"{Fore.YELLOW}[!] {texto}{Style.RESET_ALL}")

def print_info(texto):
    print(f"{Fore.BLUE}[i] {texto}{Style.RESET_ALL}")

def validar_seleccion(mensaje, max_numero):
    while True:
        try:
            seleccion = int(input(f"{Fore.CYAN}{mensaje}{Style.RESET_ALL}"))
            if 1 <= seleccion <= max_numero:
                return seleccion
            else:
                print_error(f"Por favor ingresa un número entre 1 y {max_numero}")
        except ValueError:
            print_error("Por favor ingresa un número válido")

def iniciar_driver():
    # Suppress logging warnings
    os.environ["GRPC_VERBOSITY"] = "ERROR"
    os.environ["GLOG_minloglevel"] = "2"
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,720")
    # Configuración de descargas
    prefs = {
        "download.default_directory": RUTA_DESCARGAS,
        # Deshabilitar logs
        "excludeSwitches": ["enable-logging"],
        "logging": {
            "browser": "OFF",
            "performance": "OFF",
            "driver": "OFF"
        }
    }
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # Suprimir logs de Selenium
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    
    service = Service(ChromeDriverManager().install())
    service.log_path = 'NUL'  # En Windows
    return webdriver.Chrome(service=service, options=options)

def buscar_y_descargar(nombre_libro):
    driver = iniciar_driver()
    print_info("Conectando con LibGen...")
    driver.get("https://libgen.is/")

    # Ingresar término de búsqueda
    search_input = driver.find_element(By.NAME, "req")
    search_input.send_keys(nombre_libro)
    search_input.submit()
    print_info("Buscando libros...")

    try:
        # Esperar y obtener resultados
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, "//td[@width='500']/a"))
        )
        titles = driver.find_elements(By.XPATH, "//td[@width='500']/a")
        libros = []
        
        if not titles:
            print_error("No se encontraron libros para ese término.")
            return None, None
            
        print(f"\n{Fore.CYAN}{Style.BRIGHT}═══════════════ Resultados de la búsqueda ═══════════════{Style.RESET_ALL}\n")
        for i, title in enumerate(titles, 1):
            raw = title.get_attribute("innerHTML")
            titulo = raw.split("<br>")[0].split("<font")[0].strip()
            enlace = title.get_attribute("href")
            libros.append((i, titulo, enlace))
            print(f"{Fore.GREEN}[{i}]{Style.RESET_ALL} {titulo}")
        print(f"\n{Fore.CYAN}{Style.BRIGHT}═══════════════════════════════════════════════════════{Style.RESET_ALL}\n")

        seleccion = validar_seleccion("Selecciona un libro por número: ", len(libros))
        elegido = libros[seleccion - 1]
        print_info(f"Descargando: {elegido[1]}")
        driver.get(elegido[2])

        # Intentar hacer clic en el enlace de descarga principal
        try:
            descarga = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/table/tbody/tr[18]/td[2]/table/tbody/tr/td[1]/a"))
            )
            descarga.click()
        except Exception:
            print_warning("Selector de descarga principal falló, usando fallback...")
            enlaces = driver.find_elements(By.CSS_SELECTOR, "#download a")
            if enlaces:
                enlaces[0].click()
            else:
                print_error("No se encontró enlace de descarga final.")
                return elegido[1], elegido[2]

        # Segundo paso: enlace final
        try:
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#download a"))
            )
            final = driver.find_element(By.CSS_SELECTOR, "#download a")
            final.click()
        except Exception:
            print_error("No se pudo hacer clic en el enlace final de descarga.")
            return elegido[1], elegido[2]

        ruta_archivo = esperar_descarga_completa(RUTA_DESCARGAS)
        if ruta_archivo:
            print_success(f"Descarga completada: {ruta_archivo}")
        else:
            print_error("La descarga falló o tardó demasiado.")

        return elegido[1], elegido[2]

    finally:
        driver.quit()
