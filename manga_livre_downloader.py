from requests import Session
from pathlib import Path
import imgdl
from PIL import Image
import shutil
from argparse import ArgumentParser
import traceback

class MangaLivreDownloader:
    def __init__(self, final_path, no_pdf):
        self.final_path = Path(final_path)
        self.no_pdf = no_pdf
        self.session = Session()
        self.session.headers.update({
            'authority': 'mangalivre.net',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5,ru;q=0.4,es;q=0.3,ja;q=0.2',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        })
    
    def get_manga_chapters(self, url, chapter_selection):
        manga_id = url.split('/')[-1]
        manga_chapters = []
        offset = 0
        while True:
            response = self.session.get(f'https://mangalivre.net/series/chapters_list.json?page={offset}&id_serie={manga_id}').json()['chapters']
            if not response:
                break
            manga_chapters.extend(response)
            offset += 1
            if chapter_selection[0] == 'all':
                continue
            if chapter_selection[0] == 'last':
                break
        manga_chapters.reverse()
        count = 1
        for i in range(len(manga_chapters)):
            for j in range(i + 1, len(manga_chapters)):
                if manga_chapters[i]['number'] == manga_chapters[j]['number']:
                    manga_chapters[j]['number'] = f'{manga_chapters[i]["number"]}_{count}'
                    count += 1
            count = 1
        if chapter_selection[0] == 'last':
            manga_chapters = [manga_chapters[-1]]
        elif chapter_selection[0] != 'all':
            manga_chapters = [manga_chapter for manga_chapter in manga_chapters if manga_chapter['number'] in chapter_selection]
        if not manga_chapters:
            raise Exception('No chapters found.')
        return manga_chapters
    

    def get_manga_chapter_images(self, manga_chapter):
        return [manga_chapter_images['legacy'] for manga_chapter_images in self.session.get(f'https://mangalivre.net/leitor/pages/{manga_chapter["releases"][list(manga_chapter["releases"].keys())[0]]["id_release"]}.json').json()['images']]

    
    def get_sanizated_string(self, dirty_string, is_folder):
        for character in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']:
            dirty_string = dirty_string.replace(character, '_')
        if dirty_string[-1:] == '.' and is_folder:
            dirty_string = dirty_string[:-1] + '_'
        return dirty_string.strip()
    

    def download_manga_chapter_images(self, manga_chapter, manga_chapter_images):
        manga_chapter_images_path = self.final_path / self.get_sanizated_string(manga_chapter["name"], True) / f'Chapter {self.get_sanizated_string(manga_chapter["number"], True)}'
        manga_chapter_images_path.mkdir(parents=True, exist_ok=True)
        manga_chapter_images_location = [
            manga_chapter_images_path / f'{i + 1:02d}.{manga_chapter_images[i].split(".")[-1]}' for i in range(len(manga_chapter_images))
        ]
        imgdl.download(manga_chapter_images, manga_chapter_images_location, force = True)
        if not self.no_pdf:
            images = [Image.open(manga_chapter_images_location[i]) for i in range(len(manga_chapter_images_location))]
            images[0].save(
                manga_chapter_images_path.parent / f'Chapter {self.get_sanizated_string(manga_chapter["number"], False)}.pdf',
                save_all = True,
                append_images=images[1:]
            )
            shutil.rmtree(manga_chapter_images_path)


if __name__ == '__main__':
    parser = ArgumentParser(description = 'Download manga from mangalivre.net')
    parser.add_argument(
        'url',
        nargs='+',
        help='mangalivre.net manga url.',
        metavar='<url>'
    )
    parser.add_argument(
        '-c',
        '--chapter-selection',
        nargs = '+',
        default = ['all'],
        help = 'Chapter selection. Can be "all", "last" or a list of chapter numbers. Default is "all".',
        metavar = '<chapter>'
    )
    parser.add_argument(
        '-o',
        '--final-path',
        default = 'Manga Livre Downloader',
        help = 'Final path.',
        metavar = '<final_path>'
    )
    parser.add_argument(
        '-p',
        '--print-chapters',
        action = 'store_true',
        help = 'Print chapters and exit.'
    )
    parser.add_argument(
        '-n',
        '--no-pdf',
        action = 'store_true',
        help = "Don't make PDF."
    )
    parser.add_argument(
        '-e',
        '--print-exceptions',
        action = 'store_true',
        help = 'Print exceptions.'
    )
    args = parser.parse_args()
    manga_livre_downloader = MangaLivreDownloader('Manga Livre Downloader', args.no_pdf)
    error_count = 0
    for i in range(len(args.url)):
        try:
            manga_chapters = manga_livre_downloader.get_manga_chapters(args.url[i], args.chapter_selection)
            if args.print_chapters:
                for manga_chapter in manga_chapters:
                    print(manga_chapter['number'])
                break
            for j in range(len(manga_chapters)):
                print(f'Downloading {manga_chapters[j]["name"]} Chapter {manga_chapters[j]["number"]} (URL {i + 1})...')
                try:
                    manga_chapter_images = manga_livre_downloader.get_manga_chapter_images(manga_chapters[j])
                    manga_livre_downloader.download_manga_chapter_images(manga_chapters[j], manga_chapter_images)
                except KeyboardInterrupt:
                    exit()
                except:
                    error_count += 1
                    print(f'* Failed to download {manga_chapters[j]["name"]} Chapter {manga_chapters[j]["number"]} (URL {i + 1}).')
                    if args.print_exceptions:
                        traceback.print_exc()
        except SystemExit:
            exit(0)
        except KeyboardInterrupt:
            exit(0)
        except:
            error_count += 1
            print(f'* Failed to download URL {i + 1}')
            if args.print_exceptions:
                traceback.print_exc()
    if not args.print_chapters:
        print(f'Finished ({error_count} error(s)).')
