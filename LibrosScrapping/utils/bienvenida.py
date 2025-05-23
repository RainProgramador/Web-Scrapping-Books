#EN este script se le dara la bienvenida al usuario y una informacion basica
import os

def BienvenidaUsuario():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("""
    Bienvenido a LibrosScrapping

    Este programa te permite buscar y descargar libros de la biblioteca LibGen.is  
    Las descargas se guardarán en la carpeta "LibrosDescargados" dentro de "Documentos".
    Asegúrate de tener suficiente espacio en disco y una conexión a Internet estable.
    Si tienes alguna pregunta o necesitas ayuda, no dudes en preguntar.
    Este programa fue creado por RainProgramador
          
    Github: RainProgramador/Web-Scrapping-Books
          
    Presiona Enter para continuar...      
    """)
    input()

    #Limpiar consola
    os.system('cls' if os.name == 'nt' else 'clear')
    