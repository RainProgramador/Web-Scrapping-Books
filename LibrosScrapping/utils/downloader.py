# utils/downloader.py
import os
import time

def obtener_archivos(carpeta):
    """
    Devuelve un conjunto con los nombres de archivos actualmente en la carpeta.
    """
    try:
        return set(os.listdir(carpeta))
    except FileNotFoundError:
        return set()


def esperar_descarga_completa(carpeta_descargas, tiempo_espera=240):
    """
    Espera a que un nuevo archivo aparezca en la carpeta de descargas y se complete.
    Retorna la ruta del archivo descargado o None si falla.
    """
    archivos_antes = obtener_archivos(carpeta_descargas)
    tiempo_transcurrido = 0

    while tiempo_transcurrido < tiempo_espera:
        archivos_ahora = obtener_archivos(carpeta_descargas)
        nuevos = archivos_ahora - archivos_antes

        if nuevos:
            # Verificar cada nuevo archivo
            for nombre in nuevos:
                # Ignorar descargas en curso
                if nombre.endswith('.crdownload'):
                    continue
                ruta_archivo = os.path.join(carpeta_descargas, nombre)
                # Esperar brevemente para asegurar escritura completa
                time.sleep(1)
                if os.path.getsize(ruta_archivo) > 0:
                    return ruta_archivo

        time.sleep(1)
        tiempo_transcurrido += 1

    return None