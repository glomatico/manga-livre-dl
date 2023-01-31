# Manga Livre DL
I don't really read manga, but a friend of mine asked me to create a script to download manga from https://mangalivre.net/. And so I did it.

## Setup
Install using pip:
```
pip install manga-livre-dl
```

## Usage
```
usage: manga-livre-dl [-h] [-c CHAPTER_SELECTION [CHAPTER_SELECTION ...]] [-f FINAL_PATH] [-p] [-n] [-e] [-v]
                   url [url ...]

positional arguments:
  url                   mangalivre.net manga URL

options:
  -h, --help            show this help message and exit
  -c CHAPTER_SELECTION [CHAPTER_SELECTION ...], --chapter-selection CHAPTER_SELECTION [CHAPTER_SELECTION ...]
                        Chapter selection. Can be "all", "last" or a list of chapters (default: ['all'])
  -f FINAL_PATH, --final-path FINAL_PATH
                        Final path (default: Manga Livre DL)
  -p, --print-chapters  Print chapters and exit (default: False)
  -n, --no-pdf          Don't make PDF (default: False)
  -e, --print-exceptions
                        Print exceptions (default: False)
  -v, --version         show program's version number and exit
```