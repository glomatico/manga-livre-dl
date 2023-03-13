from .manga_livre_dl import MangaLivreDl
import argparse
import traceback

__version__ = '1.4'


def main():
    parser = argparse.ArgumentParser(
        formatter_class = argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        'url',
        nargs='+',
        help='mangalivre.net manga URL'
    )
    parser.add_argument(
        '-c',
        '--chapter-selection',
        nargs = '+',
        default = ['all'],
        help = 'Chapter selection. Can be "all", "last" or a list of chapters'
    )
    parser.add_argument(
        '-f',
        '--final-path',
        default = 'Manga Livre DL',
        help = 'Final path'
    )
    parser.add_argument(
        '-o',
        '--overwrite',
        action = 'store_true',
        help = 'Overwrite existing files'
    )
    parser.add_argument(
        '-p',
        '--print-chapters',
        action = 'store_true',
        help = 'Print chapters and exit'
    )
    parser.add_argument(
        '-a',
        '--ask-scan',
        action = 'store_true',
        help = 'Ask for scan selection'
    )
    parser.add_argument(
        '-n',
        '--no-pdf',
        action = 'store_true',
        help = "Don't make PDF and delete images"
    )
    parser.add_argument(
        '-e',
        '--print-exceptions',
        action = 'store_true',
        help = 'Print exceptions'
    )
    parser.add_argument(
        '-v',
        '--version',
        action = 'version',
        version = f'%(prog)s {__version__}'
    )
    args = parser.parse_args()
    dl = MangaLivreDl(args.final_path, args.no_pdf, args.ask_scan)
    error_count = 0
    for i, url in enumerate(args.url):
        try:
            manga_chapters = dl.get_manga_chapters(url, args.chapter_selection)
            if args.print_chapters:
                for manga_chapter in manga_chapters:
                    print(manga_chapter['number'])
                break
            for chapter in manga_chapters:
                print(f'Downloading {chapter["name"]} Chapter {chapter["number"]} (URL {i + 1}/{len(args.url)})')
                final_location = dl.get_final_location(chapter)
                scan_key = dl.get_scan_key(chapter)
                if not args.overwrite and dl.check_exists(final_location):
                    continue
                try:
                    dl.download_manga_chapter(chapter, final_location, scan_key)
                    dl.make_pdf(final_location)
                except KeyboardInterrupt:
                    exit()
                except:
                    error_count += 1
                    print(f'Failed to download {chapter["name"]} Chapter {chapter["number"]} (URL {i + 1}/{len(args.url)})')
                    if args.print_exceptions:
                        traceback.print_exc()
        except SystemExit:
            exit(0)
        except KeyboardInterrupt:
            exit(0)
        except:
            error_count += 1
            print(f'Failed to download URL {i + 1}')
            if args.print_exceptions:
                traceback.print_exc()
    if not args.print_chapters:
        print(f'Done ({error_count} error(s))')


if __name__ == '__main__':
    main()
