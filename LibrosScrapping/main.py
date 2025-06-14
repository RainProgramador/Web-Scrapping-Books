# main.py
import importlib.util
import subprocess
import sys

#Se inicia el programa
#Funcion para verificar si colorama esta instalado
def verificar_dependencia(modulo_nombre, paquete_pip=None):
    if paquete_pip is None:
        paquete_pip = modulo_nombre
    if importlib.util.find_spec(modulo_nombre) is None:
        print("Este programa necesita el modulo colorama para funcionar correctamente.")
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
    else:
        print(f"[✓] El módulo '{modulo_nombre}' ya está instalado correctamente.")

from utils.menu import BienvenidaUsuario
BienvenidaUsuario()

from utils.menu import Menu_Options
Menu_Options()
