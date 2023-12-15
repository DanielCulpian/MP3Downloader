# Made by Daniel Culpian
import os
from tkinter import Tk, Label, Entry, messagebox, Menu
from tkinter.ttk import Button
from pytube import YouTube
from ttkthemes import ThemedStyle

class MP3DownloaderApp:
    def __init__(self, master):
        self.master = master
        master.title("MP3 Downloader")
        master.geometry("400x200")

        style = ThemedStyle(master)
        style.set_theme("clam")

        self.label = Label(master, text="Introduzca la URL del video de YouTube:")
        self.label.pack(pady=10)

        self.url_entry = Entry(master, width=40)
        self.url_entry.pack(pady=10)

        # Agregar menú contextual (clic derecho)
        self.context_menu = Menu(master, tearoff=0)
        self.context_menu.add_command(label="Pegar", command=self.paste_from_clipboard)
        self.context_menu.add_command(label="Borrar texto", command=self.clear_text)
        self.url_entry.bind("<Button-3>", self.show_context_menu)

        self.download_button = Button(master, text="Descargar", command=self.download, style="TButton")
        self.download_button.pack(pady=10)

        self.created_by_label = Label(master, text="Creado por Daniel Culpian", fg="#808080")
        self.created_by_label.pack(side="bottom", pady=5)

        self.url_entry.focus_set()

    def paste_from_clipboard(self):
        clipboard_content = self.master.clipboard_get()
        self.url_entry.delete(0, 'end')
        self.url_entry.insert(0, clipboard_content)

    def clear_text(self):
        self.url_entry.delete(0, 'end')

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def download(self):
        url = self.url_entry.get()

        try:
            yt = YouTube(url)
            carpeta_musica = os.path.join(os.getcwd(), 'musica')
            archivo_destino = os.path.join(carpeta_musica, yt.title + ".mp3")

            if os.path.exists(archivo_destino):
                messagebox.showinfo("Canción ya descargada", f'La canción "{yt.title}" ya está descargada en {carpeta_musica}')
            else:
                if not os.path.exists(carpeta_musica):
                    os.makedirs(carpeta_musica)
                    messagebox.showinfo("Carpeta creada", f'Se ha creado la carpeta "musica" en {carpeta_musica}')

                yt.streams.filter(only_audio=True)[-1].download(output_path=carpeta_musica, filename=yt.title + ".mp3")

                messagebox.showinfo("Descarga exitosa", "Descarga realizada con éxito!")

            self.url_entry.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Error", f"Error en la descarga: {str(e)}")

if __name__ == "__main__":
    root = Tk()
    app = MP3DownloaderApp(root)
    root.mainloop()
