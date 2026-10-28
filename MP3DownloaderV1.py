# Made by Daniel Culpian
# MP3Downloader - Powered by spotDL

import subprocess
import sys
from pathlib import Path
from colorama import Fore, Style, init

init(autoreset=True)

# Configuracion de la carpeta que almacena la musica.
CARPETA_MUSICA = Path.cwd() / "musica"


# Simple funcion estetica
def mostrar_banner():
    print(
        f"\n{Fore.RED}"
        "-----------------------------------\n"
        "       MP3Downloader\n"
        "       by DANIEL CULPIAN\n"
        "-----------------------------------"
        f"{Style.RESET_ALL}\n"
    )

# Comprueba que la carpeta musica existe o no, en caso negativo, se crea.
def preparar_carpeta():
    if not CARPETA_MUSICA.exists():
        CARPETA_MUSICA.mkdir(parents=True)
        print(f'{Fore.GREEN}Carpeta "musica" creada.')
    else:
        print(f'{Fore.CYAN}Carpeta "musica" ya existente.')

    print(f"Ruta de descarga: {CARPETA_MUSICA.resolve()}")

# Funcion encargada de gestion la descarga de musica.
def descargar_musica(consulta):
    # Almacena y prepara una llamada a spotdl con la consulta de musica deseada.
    comando = [
        sys.executable,
        "-m",
        "spotdl",
        "download",
        consulta,
        "--format",
        "mp3",
        "--output",
        str(CARPETA_MUSICA / "{artists} - {title}.{output-ext}"),
    ]

    # Estetico
    print(f"\n{Fore.YELLOW}Iniciando descarga...")

    # Se realiza la descarga usando subprocess para poder descargar varias canciones en multiplano.
    try:
        resultado = subprocess.run(
            comando,
            check=False,
        )

        if resultado.returncode == 0:
            print(f"\n{Fore.GREEN}Descarga finalizada.")
        else:
            print(
                f"\n{Fore.RED}"
                f"spotDL termino con codigo {resultado.returncode}."
            )
            print("Comprueba el enlace, la conexion y FFmpeg.")

    # Excepciones
    except FileNotFoundError:
        print(
            f"{Fore.RED}No se pudo iniciar spotDL. "
            "Comprueba que esta instalado en este Python."
        )
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Descarga interrumpida.")

# Funcion main
def main():
    mostrar_banner() # Muestra el banner.
    preparar_carpeta() # Setea la carpeta para almacenar musica.

    # Gestion del programa en bucle hasta finalizacion por entrada del usuario.
    while True:
        try: # Gestiona la consulta
            consulta = input(
                "\nIntroduce una URL de Spotify "
                "o una cancion (artista - titulo).\n"
                "Escribe 'salir' para terminar:\n> "
            ).strip()

            if consulta.lower() == "salir": # Rompe el bucle.
                print(f"{Fore.CYAN}¡Hasta pronto!")
                break

            if not consulta:
                print(f"{Fore.YELLOW}Introduce una URL o una canción.")
                continue

            descargar_musica(consulta) # Inicia gestion de descarga.

            input("\nPresiona Enter para continuar...") # Uso de input para pausar el programa hasta interaccion del usuario.

        except (EOFError, KeyboardInterrupt):
            print(f"\n{Fore.CYAN}Programa finalizado.")
            break


if __name__ == "__main__":
    main()