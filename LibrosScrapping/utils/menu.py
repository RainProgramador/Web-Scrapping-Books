#EN este script se le dara la bienvenida al usuario y una informacion basica del programa
#Tambien se le dara al usuario un menu de opciones para que pueda elegir que hacer

import os
import sys
import time
import importlib.util
import subprocess
from colorama import init, Fore, Back, Style

# Inicializar colorama para Windows
init()

def print_header(texto):
    print(f"{Fore.CYAN}{Style.BRIGHT}{texto}{Style.RESET_ALL}")

def print_success(texto):
    print(f"{Fore.GREEN}[✓] {texto}{Style.RESET_ALL}")

def print_error(texto):
    print(f"{Fore.RED}[!] {texto}{Style.RESET_ALL}")

def print_warning(texto):
    print(f"{Fore.YELLOW}[!] {texto}{Style.RESET_ALL}")

def print_info(texto):
    print(f"{Fore.BLUE}[i] {texto}{Style.RESET_ALL}")

def BienvenidaUsuario():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════╗
║                    Bienvenido a LibrosScrapping              ║
╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.WHITE}Este programa te permite buscar y descargar libros de la biblioteca LibGen.is  
Las descargas se guardarán en la carpeta "LibrosDescargados" dentro de "Documentos".

{Fore.YELLOW}[!] Asegúrate de tener:{Style.RESET_ALL}
  • Suficiente espacio en disco
  • Una conexión a Internet estable

{Fore.BLUE}[i] Programa creado por:{Style.RESET_ALL} RainProgramador
{Fore.BLUE}[i] Github:{Style.RESET_ALL} RainProgramador/Web-Scrapping-Books
          
{Fore.GREEN}Presiona Enter para continuar...{Style.RESET_ALL}      
    """)
    input()

    #Limpiar consola
    os.system('cls' if os.name == 'nt' else 'clear')

def verificar_dependencia(modulo_nombre, paquete_pip=None):
    if paquete_pip is None:
        paquete_pip = modulo_nombre
    if importlib.util.find_spec(modulo_nombre) is None:
        print_warning(f"El módulo '{modulo_nombre}' no está instalado.")
        respuesta = input(f"¿Deseas instalar '{paquete_pip}' ahora? (s/n): ").strip().lower()
        if respuesta == 's':
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", paquete_pip])
                print_success(f"'{paquete_pip}' se ha instalado correctamente.\n")
            except subprocess.CalledProcessError:
                print_error(f"Hubo un error al instalar '{paquete_pip}'.")
                sys.exit(1)
        else:
            print_error("El programa no puede continuar sin este módulo.")
            sys.exit(1)
    else:
        print_success(f"El módulo '{modulo_nombre}' ya está instalado correctamente.")

def Menu_VerificarDependencias():
    print_header("\nVerificando requisitos del programa...")
    print_info("\n1. Verificando Google Chrome:")
    verificar_chrome_instalado()
    
    print_info("\n2. Verificando dependencias de Python:")
    verificar_dependencia("selenium", "selenium")
    verificar_dependencia("webdriver_manager", "webdriver-manager")
    verificar_dependencia("pandas", "pandas")
    verificar_dependencia("colorama", "colorama")
    
    print_success("\nTodas las verificaciones completadas.")
    time.sleep(2)

#Se definen las funciones necesarias para empezar el programa

#Iniciar el programa

def Menu_iniciar_el_programa():
    try:
        from scraper.libgen_scraper import buscar_y_descargar
        from utils.storage import init_db, guardar_libro

        init_db()
        nombre = input("¿Qué libro deseas buscar?: ")
        titulo, enlace = buscar_y_descargar(nombre)
        guardar_libro(titulo, enlace)
        print("Libro guardado en la base de datos.")
    except Exception as e:
        print(f"Error al iniciar el programa: {e}")

UserOption = ""

#Validar que el usuario ingrese un numero entero

def Menu_ValidarNumeroEntero(mensaje):
    while True:
        try:
            valor = input(mensaje)
            numero = int(valor)
            return numero
        except ValueError:
            print("Error: Por favor ingresa un número entero válido.")

#Funcion para mostrar la lista de libros descargados

def Menu_VerListaLibrosDescargados():
    try:
        from utils.storage import listar_libros
        listar_libros()
    except Exception as e:
        print(f"Error al mostrar la lista de libros: {e}")

#Salir del programa

def Menu_Salir():
    print("Saliendo del programa...")
    sys.exit(0)

def Menu_Options():
    print(f"""
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════╗
║                       Menú Principal                         ║
╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.WHITE}Escribe un número para elegir una de las siguientes opciones:{Style.RESET_ALL}

{Fore.GREEN}[1]{Style.RESET_ALL} Verificar las dependencias e instalarlas
{Fore.BLUE}[2]{Style.RESET_ALL} Iniciar la búsqueda de libros
{Fore.YELLOW}[3]{Style.RESET_ALL} Ver lista de libros descargados
{Fore.RED}[4]{Style.RESET_ALL} Salir del programa

    """)

    UserOption = Menu_ValidarNumeroEntero("Elige una opción: ")

    #Limpiar consola
    os.system('cls' if os.name == 'nt' else 'clear')

    if UserOption == 1:
        from utils.dependencias import Menu_VerificarDependencias
        Menu_VerificarDependencias()
        Menu_Options()
    elif UserOption == 2:
        Menu_iniciar_el_programa()
        Menu_Options()
    elif UserOption == 3:
        Menu_VerListaLibrosDescargados()
        Menu_Options()
    elif UserOption == 4:
        Menu_Salir()
    else:
        print_error("Opción inválida. Por favor, ingrese un número válido.")
        Menu_Options()
    