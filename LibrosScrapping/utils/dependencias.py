#En este script se verificaran las dependencias del programa

import sys
import time
import subprocess
import importlib.util
import os
from colorama import init, Fore, Back, Style

#Inicializar colorama para Windows
init()

#Verificar si las dependencias estan instaladas

def verificar_dependencia(modulo_nombre, paquete_pip=None):
    if paquete_pip is None:
        paquete_pip = modulo_nombre
    if importlib.util.find_spec(modulo_nombre) is None:
        print(f"{Fore.RED}[!]{Style.RESET_ALL} El módulo '{modulo_nombre}' no está instalado.")
        respuesta = input(f"¿Deseas instalar '{paquete_pip}' ahora? (s/n): ").strip().lower()
        if respuesta == 's':
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", paquete_pip])
                print(f"{Fore.GREEN}[+]{Style.RESET_ALL} '{paquete_pip}' se ha instalado correctamente.\n")
            except subprocess.CalledProcessError:
                print(f"{Fore.RED}[!]{Style.RESET_ALL} Hubo un error al instalar '{paquete_pip}'.")
                sys.exit(1)
        else:
            print(f"{Fore.RED}[!]{Style.RESET_ALL} El programa no puede continuar sin este módulo.")
            sys.exit(1)
    else:
        print(f"{Fore.GREEN}[✓]{Style.RESET_ALL} El módulo '{modulo_nombre}' ya está instalado correctamente.")

def verificar_chrome_instalado():
    # Rutas comunes donde se puede encontrar Chrome en Windows
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
    ]
    
    chrome_instalado = any(os.path.exists(path) for path in chrome_paths)
    
    if not chrome_instalado:
        print(f"{Fore.RED}[!]{Style.RESET_ALL} Google Chrome no está instalado o no se puede encontrar.")
        print(f"{Fore.RED}[!]{Style.RESET_ALL} Por favor, instala Google Chrome desde: https://www.google.com/chrome/")
        respuesta = input("¿Deseas continuar después de instalar Chrome? (s/n): ").strip().lower()
        if respuesta != 's':
            print(f"{Fore.RED}[!]{Style.RESET_ALL} El programa no puede continuar sin Google Chrome.")
            sys.exit(1)
    else:
        print(f"{Fore.GREEN}[✓]{Style.RESET_ALL} Google Chrome está instalado correctamente.")

def Menu_VerificarDependencias():
    print(f"{Fore.CYAN}[+]{Style.RESET_ALL} Verificando requisitos del programa...")
    print(f"{Fore.CYAN}[+]{Style.RESET_ALL} 1. Verificando Google Chrome:")
    verificar_chrome_instalado()
    
    print(f"{Fore.CYAN}[+]{Style.RESET_ALL} 2. Verificando dependencias de Python:")
    verificar_dependencia("selenium", "selenium")
    verificar_dependencia("webdriver_manager", "webdriver-manager")
    verificar_dependencia("pandas", "pandas")
    
    print(f"{Fore.CYAN}[+]{Style.RESET_ALL} Todas las verificaciones completadas.")
    time.sleep(2)
