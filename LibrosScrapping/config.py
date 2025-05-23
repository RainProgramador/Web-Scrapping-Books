import os

# Carpeta de descargas
RUTA_DESCARGAS = os.path.join(os.path.expanduser("~"), "Documents", "LibrosDescargados")

if not os.path.exists(RUTA_DESCARGAS):
    os.makedirs(RUTA_DESCARGAS)
