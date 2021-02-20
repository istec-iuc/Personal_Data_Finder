"""
ISTEC Personal Data Detector (Şubat 2021)

Ahmet KÖKEN
ahmetkkn07@gmail.com
https://github.com/ahmetkkn07

Bu proje, csv dosyası olarak verilen anahtar kelimelere ve/veya 
düzenli ifadelere göre eşleşme yakalar. PDF ve görüntü dosyalarında
arama yapar ve bu dosyalara bir klasör içerisinde sınıflandırarak
hangi dosyada ne tür kişisel veri bulunduğunu gösteren bir csv çıktı üretir.
"""


import os
import argparse
import istecPDD


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-p", "--path", help="input folder", type=dir_path)
        parser.add_argument("-k", "--keywords", help="keyword list")
        parser.add_argument("-r", "--regex", help="regex pattern list")
        parser.add_argument(
            "-m", "--move", action='store_true')  # default False
        args = parser.parse_args()
        Path = args.path
    except NotADirectoryError:
        print("Hatalı klasör yolu!")
        exit()
    else:
        istecPDD.start(Path=Path, args=args)


if __name__ == "__main__":
    main()
