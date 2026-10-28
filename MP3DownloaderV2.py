# Made by Daniel Culpian
# MP3Downloader GUI - Powered by spotDL

import os
import sys
import queue
import threading
import subprocess
import tkinter as tk

from pathlib import Path
from tkinter import ttk, messagebox, filedialog


# ---------------- CONFIGURACIÓN ----------------

APP_NAME = "MP3Downloader"
CARPETA_MUSICA = Path.cwd() / "musica"

BG = "#111318"
PANEL = "#191c24"
INPUT_BG = "#222631"
FG = "#f1f3f8"
MUTED = "#9299aa"
ACCENT = "#ed4242"
ACCENT_HOVER = "#ff5c5c"
GREEN = "#42d392"
BORDER = "#303542"


class MP3DownloaderApp:

    def __init__(self, master):
        self.master = master
        self.master.title(f"{APP_NAME} | by Daniel Culpian")
        self.master.geometry("680x610")
        self.master.minsize(580, 540)
        self.master.configure(bg=BG)

        self.events = queue.Queue()
        self.downloading = False
        self.process = None
        self.closing = False

        CARPETA_MUSICA.mkdir(parents=True, exist_ok=True)

        self.configure_styles()
        self.create_widgets()
        self.create_context_menu()

        self.url_entry.focus_set()
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.master.after(100, self.process_events)

    # ---------------- ESTILOS ----------------

    def configure_styles(self):
        style = ttk.Style(self.master)
        style.theme_use("clam")

        style.configure(
            "TButton",
            font=("Segoe UI", 10),
            padding=(12, 9),
            background=INPUT_BG,
            foreground=FG,
            borderwidth=0,
        )
        style.map(
            "TButton",
            background=[("active", "#353b49")],
            foreground=[("disabled", MUTED)],
        )

        style.configure(
            "Accent.TButton",
            background=ACCENT,
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=(16, 11),
        )
        style.map(
            "Accent.TButton",
            background=[
                ("active", ACCENT_HOVER),
                ("disabled", "#633333"),
            ],
        )

        style.configure(
            "Horizontal.TProgressbar",
            troughcolor=INPUT_BG,
            background=ACCENT,
            bordercolor=INPUT_BG,
            lightcolor=ACCENT,
            darkcolor=ACCENT,
        )

    # ---------------- INTERFAZ ----------------

    def create_widgets(self):
        # Cabecera
        header = tk.Frame(self.master, bg=BG)
        header.pack(fill="x", padx=30, pady=(24, 18))

        tk.Label(
            header,
            text="♫",
            font=("Segoe UI Symbol", 30, "bold"),
            bg=BG,
            fg=ACCENT,
        ).pack(side="left", padx=(0, 13))

        title_frame = tk.Frame(header, bg=BG)
        title_frame.pack(side="left", fill="x")

        tk.Label(
            title_frame,
            text="MP3Downloader",
            font=("Segoe UI", 23, "bold"),
            bg=BG,
            fg=FG,
        ).pack(anchor="w")

        tk.Label(
            title_frame,
            text="TU MÚSICA, ORGANIZADA Y LISTA PARA ESCUCHAR",
            font=("Segoe UI", 8, "bold"),
            bg=BG,
            fg=MUTED,
        ).pack(anchor="w", pady=(2, 0))

        # Panel principal
        panel = tk.Frame(
            self.master,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        panel.pack(fill="x", padx=30, pady=5)

        tk.Label(
            panel,
            text="  NUEVA DESCARGA",
            font=("Segoe UI", 9, "bold"),
            bg=PANEL,
            fg=ACCENT,
        ).pack(anchor="w", padx=18, pady=(18, 8))

        tk.Label(
            panel,
            text="Enlace de Spotify o búsqueda de canción",
            font=("Segoe UI", 11, "bold"),
            bg=PANEL,
            fg=FG,
        ).pack(anchor="w", padx=18)

        tk.Label(
            panel,
            text="Pega un enlace o escribe artista - título.",
            font=("Segoe UI", 9),
            bg=PANEL,
            fg=MUTED,
        ).pack(anchor="w", padx=18, pady=(4, 12))

        entry_frame = tk.Frame(panel, bg=INPUT_BG)
        entry_frame.pack(fill="x", padx=18, pady=(0, 14))

        self.url_entry = tk.Entry(
            entry_frame,
            font=("Segoe UI", 11),
            bg=INPUT_BG,
            fg=FG,
            insertbackground=FG,
            relief="flat",
            bd=0,
        )
        self.url_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(12, 4),
            ipady=12,
        )

        self.url_entry.bind("<Return>", lambda event: self.download())
        self.url_entry.bind("<Button-3>", self.show_context_menu)

        self.clear_button = ttk.Button(
            entry_frame,
            text="✕",
            width=3,
            command=self.clear_text,
        )
        self.clear_button.pack(side="right", padx=5, pady=5)

        self.download_button = ttk.Button(
            panel,
            text="↓   Descargar MP3",
            style="Accent.TButton",
            command=self.download,
        )
        self.download_button.pack(fill="x", padx=18, pady=(0, 18))

        # Estado
        status_panel = tk.Frame(self.master, bg=BG)
        status_panel.pack(fill="x", padx=30, pady=(17, 8))

        tk.Label(
            status_panel,
            text="ESTADO",
            font=("Segoe UI", 9, "bold"),
            bg=BG,
            fg=MUTED,
        ).pack(side="left")

        self.status_label = tk.Label(
            status_panel,
            text="Listo para descargar",
            font=("Segoe UI", 9),
            bg=BG,
            fg=GREEN,
        )
        self.status_label.pack(side="right")

        self.progress = ttk.Progressbar(
            self.master,
            mode="indeterminate",
            style="Horizontal.TProgressbar",
        )
        self.progress.pack(fill="x", padx=30, pady=(0, 12))

        # Registro de actividad
        log_header = tk.Frame(self.master, bg=BG)
        log_header.pack(fill="x", padx=30, pady=(7, 7))

        tk.Label(
            log_header,
            text="ACTIVIDAD",
            font=("Segoe UI", 9, "bold"),
            bg=BG,
            fg=MUTED,
        ).pack(side="left")

        self.clear_log_button = ttk.Button(
            log_header,
            text="Limpiar registro",
            command=self.clear_log,
        )
        self.clear_log_button.pack(side="right")

        log_frame = tk.Frame(self.master, bg=PANEL)
        log_frame.pack(fill="both", expand=True, padx=30, pady=(0, 12))

        self.log = tk.Text(
            log_frame,
            height=7,
            bg=PANEL,
            fg="#c7cddd",
            insertbackground=FG,
            font=("Consolas", 9),
            relief="flat",
            wrap="word",
            padx=12,
            pady=10,
            state="disabled",
        )
        self.log.pack(fill="both", expand=True)

        self.log.tag_configure("success", foreground=GREEN)
        self.log.tag_configure("error", foreground=ACCENT)
        self.log.tag_configure("info", foreground="#a9b8ff")

        # Pie
        footer = tk.Frame(self.master, bg=BG)
        footer.pack(fill="x", padx=30, pady=(0, 17))

        self.folder_button = ttk.Button(
            footer,
            text="📁  Abrir carpeta",
            command=self.open_folder,
        )
        self.folder_button.pack(side="left")

        tk.Label(
            footer,
            text="Creado por Daniel Culpian",
            font=("Segoe UI", 9),
            bg=BG,
            fg=MUTED,
        ).pack(side="right", pady=8)

    # ---------------- MENÚ CONTEXTUAL ----------------

    def create_context_menu(self):
        self.context_menu = tk.Menu(
            self.master,
            tearoff=0,
            bg=PANEL,
            fg=FG,
            activebackground=ACCENT,
            activeforeground="white",
        )
        self.context_menu.add_command(
            label="Pegar",
            command=self.paste_from_clipboard,
        )
        self.context_menu.add_command(
            label="Seleccionar todo",
            command=self.select_all,
        )
        self.context_menu.add_command(
            label="Borrar texto",
            command=self.clear_text,
        )

    def show_context_menu(self, event):
        self.context_menu.tk_popup(event.x_root, event.y_root)
        return "break"

    def paste_from_clipboard(self):
        try:
            content = self.master.clipboard_get()
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, content.strip())
        except tk.TclError:
            pass

    def select_all(self):
        self.url_entry.select_range(0, tk.END)
        self.url_entry.icursor(tk.END)

    def clear_text(self):
        self.url_entry.delete(0, tk.END)
        self.url_entry.focus_set()

    # ---------------- REGISTRO Y ESTADO ----------------

    def write_log(self, text, tag="info"):
        self.log.configure(state="normal")
        self.log.insert(tk.END, text + "\n", tag)
        self.log.see(tk.END)
        self.log.configure(state="disabled")

    def clear_log(self):
        if self.downloading:
            return

        self.log.configure(state="normal")
        self.log.delete("1.0", tk.END)
        self.log.configure(state="disabled")

    def set_status(self, text, color=MUTED):
        self.status_label.configure(text=text, fg=color)

    # ---------------- DESCARGA ----------------

    def download(self):
        if self.downloading:
            return

        query = self.url_entry.get().strip()

        if not query:
            messagebox.showwarning(
                "Campo vacío",
                "Introduce un enlace o una búsqueda de canción.",
                parent=self.master,
            )
            self.url_entry.focus_set()
            return

        # Evitar una entrada que parezca una opcion de consola.
        if query.startswith("-"):
            messagebox.showwarning(
                "Entrada no válida",
                "Introduce un enlace o una búsqueda válida.",
                parent=self.master,
            )
            return

        # Evitar duplicados evidentes en busquedas de una sola cancion.
        # Para playlists y albumes, spotDL gestiona los archivos existentes.
        if "spotify.com/track/" not in query.lower():
            pass
        else:
            # No se puede confirmar el nombre final del archivo
            # sin consultar primero los metadatos de Spotify.
            pass

        self.downloading = True
        self.download_button.configure(state="disabled")
        self.url_entry.configure(state="disabled")
        self.clear_button.configure(state="disabled")
        self.folder_button.configure(state="disabled")
        self.clear_log_button.configure(state="disabled")

        self.set_status("Descargando...", ACCENT)
        self.progress.start(12)
        self.write_log(f"Iniciando: {query}")

        thread = threading.Thread(
            target=self.download_worker,
            args=(query,),
            daemon=True,
        )
        thread.start()

    def download_worker(self, query):
        command = [
            sys.executable,
            "-m",
            "spotdl",
            "download",
            query,
            "--format",
            "mp3",
            "--output",
            str(CARPETA_MUSICA / "{artists} - {title}.{output-ext}"),
        ]

        try:
            # Se combina stdout y stderr para registrar los mensajes.
            self.process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1,
            )

            for line in self.process.stdout:
                line = line.strip()
                if line:
                    self.events.put(("log", line))

            return_code = self.process.wait()
            self.events.put(("finished", return_code))

        except FileNotFoundError:
            self.events.put((
                "error",
                "No se pudo ejecutar Python o spotDL. "
                "Comprueba la instalación.",
            ))
        except Exception as error:
            self.events.put(("error", str(error)))

    def process_events(self):
        try:
            while True:
                event = self.events.get_nowait()
                event_type = event[0]

                if event_type == "log":
                    self.write_log(event[1])

                elif event_type == "finished":
                    self.finish_download(event[1])

                elif event_type == "error":
                    self.finish_download(None, event[1])

        except queue.Empty:
            pass

        if not self.closing:
            self.master.after(100, self.process_events)

    def finish_download(self, return_code, error=None):
        self.progress.stop()
        self.downloading = False
        self.process = None

        self.download_button.configure(state="normal")
        self.url_entry.configure(state="normal")
        self.clear_button.configure(state="normal")
        self.folder_button.configure(state="normal")
        self.clear_log_button.configure(state="normal")

        if error:
            self.set_status("Error", ACCENT)
            self.write_log(f"Error: {error}", "error")
            messagebox.showerror(
                "Error de descarga",
                error,
                parent=self.master,
            )

        elif return_code == 0:
            self.set_status("Proceso completado", GREEN)
            self.write_log(
                "spotDL ha finalizado correctamente.",
                "success",
            )
            messagebox.showinfo(
                "Proceso completado",
                "spotDL ha terminado. Revisa la carpeta musica "
                "y el registro para confirmar el resultado.",
                parent=self.master,
            )
            self.clear_text()

        else:
            self.set_status("Descarga fallida", ACCENT)
            self.write_log(
                f"spotDL terminó con código {return_code}.",
                "error",
            )
            messagebox.showerror(
                "Descarga fallida",
                "spotDL no pudo completar la operación.\n\n"
                "Comprueba el enlace, la conexión, la instalación "
                "de spotDL y FFmpeg. Consulta el registro para "
                "ver los detalles.",
                parent=self.master,
            )

    # ---------------- CARPETA ----------------

    def open_folder(self):
        CARPETA_MUSICA.mkdir(parents=True, exist_ok=True)

        try:
            if sys.platform.startswith("win"):
                os.startfile(str(CARPETA_MUSICA))
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(CARPETA_MUSICA)])
            else:
                subprocess.Popen(["xdg-open", str(CARPETA_MUSICA)])
        except Exception as error:
            messagebox.showerror(
                "No se pudo abrir la carpeta",
                str(error),
                parent=self.master,
            )

    # ---------------- CIERRE ----------------

    def on_close(self):
        if self.downloading:
            confirm = messagebox.askyesno(
                "Descarga en curso",
                "Hay una descarga en marcha. ¿Quieres cerrar "
                "la ventana e intentar detenerla?",
                parent=self.master,
            )
            if not confirm:
                return

            if self.process and self.process.poll() is None:
                self.process.terminate()

        self.closing = True
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MP3DownloaderApp(root)
    root.mainloop()