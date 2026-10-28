# MP3Downloader

**MP3Downloader** is a Python project that provides two ways to download music using [spotDL](https://github.com/spotDL/spotify-downloader).

The project includes a lightweight command-line version and a graphical version with a modern user interface.

**Made by:** Daniel Culpian

---

## Table of Contents

- [Versions](#versions)
- [Requirements](#requirements)
- [Installation Guide](#installation-guide)
  - [1. Install Python](#1-install-python)
  - [2. Install FFmpeg](#2-install-ffmpeg)
  - [3. Install spotDL](#3-install-spotdl)
  - [4. Install the project dependencies](#4-install-the-project-dependencies)
- [How to Run](#how-to-run)
  - [Console Version](#console-version)
  - [Graphical Version](#graphical-version)
- [Download Location](#download-location)
- [Troubleshooting](#troubleshooting)
- [Disclaimer](#disclaimer)
- [Credits](#credits)

---

## Versions

### Console Version — `MP3DownloaderV1.py`

A lightweight, terminal-based application designed for users who prefer simplicity and low resource consumption.

**Features:**
- Download music using spotDL.
- Accept Spotify links and song searches.
- Support songs, albums and playlists, depending on the supplied link.
- Automatically create a `musica` folder for downloaded files.
- Display download results and errors in the terminal.
- Continue downloading without restarting the application.

### Graphical Version — `MP3DownloaderV2.py`

A desktop application featuring a modern, dark-themed interface.

**Features:**
- User-friendly graphical interface.
- Download music using Spotify links or artist and song title searches.
- Background download processing, keeping the interface responsive.
- Activity log displaying messages from spotDL.
- Animated progress indicator while downloads are running.
- Context menu with paste, select-all and clear-text options.
- Button to open the download folder.
- Basic error handling and download status notifications.

---

## Requirements

Before running either version, make sure you have installed the following software:

| Requirement | Purpose |
|---|---|
| Python 3.11 or a compatible version supported by spotDL | Runs the scripts |
| spotDL | Searches for tracks and downloads their corresponding audio |
| FFmpeg | Processes and converts audio to MP3 |
| Tkinter | Provides the graphical interface in V2; usually included with Python on Windows and macOS |

On Windows, spotDL may also require the Microsoft Visual C++ Redistributable. Check the [official spotDL installation guide](https://spotdl.readthedocs.io/en/latest/installation/) if you encounter compatibility issues.

**Important:** An internet connection is required. spotDL uses Spotify metadata and searches for matching audio on YouTube. A Spotify Premium subscription is not normally required for this workflow.

## Installation Guide

These instructions are intended for users who have little or no experience with Python.

### 1. Install Python

Download Python from the official website:

**[Download Python](https://www.python.org/downloads/)**

1. Open the website and download a compatible Python version.
2. Run the installer.
3. On Windows, enable **Add Python to PATH** before installing.
4. Complete the installation.

To check that Python is installed correctly, open a terminal:

- **Windows:** Command Prompt or PowerShell.
- **macOS:** Terminal.
- **Linux:** Your preferred terminal.

Run:

```bash
python --version
```

If the command is not recognized on Windows, try:

```powershell
py --version
```

On macOS or Linux, you may need:

```bash
python3 --version
```

The command should display your installed Python version.

### 2. Install FFmpeg

FFmpeg is required by spotDL to process audio and convert it to MP3.

#### Option A: Install FFmpeg through spotDL

After installing spotDL in the next step, you can try its built-in download command:

```bash
python -m spotdl --download-ffmpeg
```

This option installs FFmpeg for spotDL's use. It may be sufficient without configuring FFmpeg system-wide.

#### Option B: Install FFmpeg system-wide

**Windows**

1. Open the [official FFmpeg download page](https://ffmpeg.org/download.html).
2. Follow one of the links to a Windows build.
3. Download and extract the archive.
4. Add the folder containing `ffmpeg.exe` to your system's `PATH`.
5. Close and reopen the terminal.

Alternatively, if you have Windows Package Manager (`winget`), you can search for an available package:

```powershell
winget search ffmpeg
```

Choose a suitable package from the results and install it using the package ID shown by your system.

**macOS**

If [Homebrew](https://brew.sh/) is installed, run:

```bash
brew install ffmpeg
```

**Ubuntu / Debian Linux**

Run:

```bash
sudo apt update
sudo apt install ffmpeg
```

For other Linux distributions, use your distribution's package manager.

Finally, verify the installation:

```bash
ffmpeg -version
```

If the command displays version information, FFmpeg is available from the terminal.

For additional information, visit the [official FFmpeg website](https://ffmpeg.org/download.html).

### 3. Install spotDL

Open your terminal and run the command appropriate for your operating system.

**Windows:**

```powershell
python -m pip install -U spotdl
```

If `python` is not recognized but the Python launcher works, use:

```powershell
py -m pip install -U spotdl
```

**macOS / Linux:**

```bash
python3 -m pip install -U spotdl
```

Check that spotDL works:

```bash
python -m spotdl --version
```

On macOS or Linux, replace `python` with `python3` if necessary.

If you encounter an error during installation, consult the [spotDL installation guide](https://spotdl.readthedocs.io/en/latest/installation/).

### 4. Install the project dependencies

The graphical version uses Python's built-in Tkinter library. The console version does not need any additional third-party packages beyond spotDL and its dependencies.

For the colored terminal output in V1, install Colorama:

```bash
python -m pip install colorama
```

If your version of V1 no longer uses Colorama, this step is unnecessary.

For V2, Tkinter is usually included with Python on Windows. On Linux, you may need to install it separately.

**Ubuntu / Debian:**

```bash
sudo apt install python3-tk
```

Check whether Tkinter works by running:

```bash
python -m tkinter
```

If a small test window opens, Tkinter is working. On macOS or Linux, use `python3 -m tkinter` if required.

---

## How to Run

Download or clone this repository and open a terminal in the project folder.

Your project structure should look similar to this:

```text
MP3Downloader/
├── MP3DownloaderV1.py
├── MP3DownloaderV2.py
└── README.md
```

You can run either version independently.

### Console Version

Run the following command:

**Windows:**

```powershell
python MP3DownloaderV1.py
```

**macOS / Linux:**

```bash
python3 MP3DownloaderV1.py
```

The application will display a prompt asking for a Spotify URL or a song search.

Examples:

```text
https://open.spotify.com/track/...
```

```text
Daft Punk - Get Lucky
```

Follow the prompts in the terminal to start a download or exit the application.

### Graphical Version

Run the following command:

**Windows:**

```powershell
python MP3DownloaderV2.py
```

**macOS / Linux:**

```bash
python3 MP3DownloaderV2.py
```

The application window will open.

1. Paste a Spotify link or enter a song search.
2. Click **Download MP3** or press Enter.
3. Follow the activity log and status indicator.
4. Click **Open Folder** to access your downloaded files.

The graphical version runs the download process in a background thread, so the interface remains responsive while spotDL is working.

---

## Download Location

Both versions save downloads in a folder named `musica`.

By default, the folder is created in the current working directory from which the script is launched.

For example:

```text
MP3Downloader/
├── MP3DownloaderV1.py
├── MP3DownloaderV2.py
└── musica/
    ├── Artist - Song.mp3
    └── ...
```

The exact filenames depend on the metadata returned by spotDL and the output template configured in the script.

---

## Troubleshooting

### Python is not recognized

Python may not be installed correctly or may not be included in your `PATH`.

- Reinstall Python from [python.org](https://www.python.org/downloads/).
- On Windows, select **Add Python to PATH**.
- Restart the terminal after installation.

### spotDL is not installed or cannot be found

Install or update spotDL:

```bash
python -m pip install -U spotdl
```

The scripts invoke spotDL through Python, so the package must be installed in the same Python environment used to launch the application.

### FFmpeg is not found

Run:

```bash
ffmpeg -version
```

If the command fails, install FFmpeg or check that its executable directory is included in your `PATH`. You can also try the spotDL-specific installation command described above.

### Tkinter is not available

If V2 reports that Tkinter cannot be imported, install the appropriate Tkinter package for your Python installation. On Ubuntu or Debian, use:

```bash
sudo apt install python3-tk
```

### The download fails

Check the following:

- Your internet connection is working.
- The Spotify link is valid and accessible.
- spotDL is installed and up to date.
- FFmpeg is installed and working.
- The selected track can be matched to audio on YouTube.

Some downloads may fail because of unavailable tracks, changes to external services, network problems or other restrictions.

For more information, consult the [spotDL troubleshooting guide](https://spotdl.readthedocs.io/en/latest/troubleshooting/).

---

## Disclaimer

This project is provided for educational and personal use. Users are responsible for complying with applicable copyright laws, platform terms of service and the rights of music creators.

Only download content that you are legally authorized to download.

MP3Downloader is an independent project and is not affiliated with Spotify, YouTube or the developers of spotDL.

---

## Credits

**Created by Daniel Culpian**

Built with Python, Tkinter, Colorama and [spotDL](https://github.com/spotDL/spotify-downloader).
