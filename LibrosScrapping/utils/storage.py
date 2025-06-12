# utils/storage.py

import pandas as pd
import os
from colorama import init, Fore, Style

# Inicializar colorama
init()

def print_success(texto):
    print(f"{Fore.GREEN}[✓] {texto}{Style.RESET_ALL}")

def print_error(texto):
    print(f"{Fore.RED}[!] {texto}{Style.RESET_ALL}")

def print_info(texto):
    print(f"{Fore.BLUE}[i] {texto}{Style.RESET_ALL}")

# Obtener la ruta base del proyecto (carpeta LibrosScrapping)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Definir la ruta de data relativa al directorio base
CSV_PATH = os.path.join(BASE_DIR, "data", "libros.csv")

def init_db():
    """Inicializa el archivo CSV si no existe."""
    data_dir = os.path.join(BASE_DIR, "data")
    os.makedirs(data_dir, exist_ok=True)
    if not os.path.isfile(CSV_PATH):
        df = pd.DataFrame(columns=['titulo', 'enlace'])
        df.to_csv(CSV_PATH, index=False)
        print_success(f"Archivo {CSV_PATH} creado exitosamente.")
    else:
        print_info(f"Archivo {CSV_PATH} ya existe.")

def guardar_libro(titulo, enlace):
    """Guarda un libro en el archivo CSV."""
    nuevo_libro = pd.DataFrame({'titulo': [titulo], 'enlace': [enlace]})
    
    if os.path.isfile(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        df = pd.concat([df, nuevo_libro], ignore_index=True)
    else:
        df = nuevo_libro
    
    df.to_csv(CSV_PATH, index=False)
    print_success(f"Libro '{titulo}' guardado exitosamente.")

def listar_libros():
    """Muestra todos los libros guardados en el archivo CSV."""
    if os.path.isfile(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        if df.empty:
            print_warning("No hay libros guardados.")
        else:
            print(f"\n{Fore.CYAN}{Style.BRIGHT}╔══════════════════ Lista de Libros Guardados ══════════════════╗{Style.RESET_ALL}")
            for idx, row in df.iterrows():
                print(f"\n{Fore.GREEN}[{idx + 1}]{Style.RESET_ALL} {row['titulo']}")
                print(f"   {Fore.BLUE}Link:{Style.RESET_ALL} {row['enlace']}")
            print(f"{Fore.CYAN}{Style.BRIGHT}╚════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    else:
        print_error("No se encontró la base de datos. Asegúrate de inicializarla primero.")
