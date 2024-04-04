# Made by Daniel Culpian
import subprocess
from pytube import YouTube
import os
from colorama import Fore, Style

txt = f"{Fore.RED}---MP3Downloader by DANIEL CULPIAN---{Style.RESET_ALL}"
printResult = f"echo {txt}"
subprocess.call(printResult, shell=True)

ruta = os.getcwd()

carpeta_musica = os.path.join(ruta, 'musica')

# Intenta crear la carpeta solo si no existe
if not os.path.exists(carpeta_musica):
    os.makedirs(carpeta_musica)
    print(f'Se ha creado la carpeta "musica" en {ruta}')
else:
    print(f'La carpeta "musica" ya existe en {ruta}')


while True:
    url = input("\nIntroduzca su URL de su video de Youtube: \n")

    yt = YouTube(url)
    yt.streams.filter(only_audio=True)[-1].download(output_path=carpeta_musica, filename=yt.title + ".mp3")

    txt2 = f"{Fore.GREEN}Descarga realizada con éxito!{Style.RESET_ALL}"
    printResult = f"echo {txt2}"
    subprocess.call(printResult, shell=True)

    input("Presione Enter para continuar")


