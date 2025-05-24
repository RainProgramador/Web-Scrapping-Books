# main.py
import time
import subprocess, sys, importlib.util

def verificar_dependencia(modulo_nombre, paquete_pip=None):
    if paquete_pip is None:
        paquete_pip = modulo_nombre
    if importlib.util.find_spec(modulo_nombre) is None:
        print(f"[!] El módulo '{modulo_nombre}' no está instalado.")
        respuesta = input(f"¿Deseas instalar '{paquete_pip}' ahora? (s/n): ").strip().lower()
        if respuesta == 's':
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", paquete_pip])
                print(f"[+] '{paquete_pip}' se ha instalado correctamente.\n")
            except subprocess.CalledProcessError:
                print(f"[-] Hubo un error al instalar '{paquete_pip}'.")
                sys.exit(1)
        else:
            print("[-] El programa no puede continuar sin este módulo.")
            sys.exit(1)

from utils.bienvenida import BienvenidaUsuario
BienvenidaUsuario()

print("Iniciando el programa...")
verificar_dependencia("selenium", "selenium")
verificar_dependencia("webdriver_manager", "webdriver-manager")
time.sleep(2)

from scraper.libgen_scraper import buscar_y_descargar
from utils.storage import init_db, guardar_libro

init_db()
nombre = input("¿Qué libro deseas buscar?: ")
titulo, enlace = buscar_y_descargar(nombre)
guardar_libro(titulo, enlace)
print("Libro guardado en la base de datos.")
