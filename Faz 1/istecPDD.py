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
import re
import cv2
import csv
import time
import shutil
import pytesseract
from tika import parser
from pathlib import Path
from dataclasses import dataclass
from pdf2image import convert_from_path


@dataclass
class File:
    root: str
    imageFiles: list
    pdfFiles: list


@dataclass
class Text:
    path: str
    content: str
    state: bool
    matches: list


IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png")
PDF_EXTENSIONS = (".pdf")
PD_PATH = "/PersonalDataCheckerResults/PD"
ROOT_PATH = "/PersonalDataCheckerResults"
NONPD_PATH = "/PersonalDataCheckerResults/nonPD"
KEYWORDS = list()
PATTERNS = list()
PATH = str()
Texts = list()
Files = list()
pdCount = 0


def readKeywords(csvFile: str):
    with open(csvFile, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            KEYWORDS.append(line[0])


def readPatterns(file: str):
    with open(file, 'r') as File:
        while True:
            line1 = File.readline().rstrip("\n")
            line2 = File.readline().rstrip("\n")
            PATTERNS.append([line1, line2])
            if not line2:
                PATTERNS.pop()
                break


def getFiles():
    for root, dirs, files in os.walk(PATH):
        imageFiles = list()
        pdfFiles = list()

        for name in files:
            if name.lower().endswith(IMAGE_EXTENSIONS):
                imageFiles.append(name)
            elif name.lower().endswith(PDF_EXTENSIONS):
                pdfFiles.append(name)

        file = File(root=root, imageFiles=imageFiles, pdfFiles=pdfFiles)
        Files.append(file)


def makeDirectory(path):
    pth = Path(path)
    pth.mkdir(exist_ok=True, parents=True)


def pdfToText():
    for file in Files:
        for pdf in file.pdfFiles:
            pdfpath = file.root + "/" + pdf
            file_data = parser.from_file(pdfpath)
            text = file_data['content']
            if text is None:
                text = pdfOCR(file.root, pdf)
            Texts.append(Text(path=pdfpath, content=text,
                              state=False, matches=list()))


def pdfOCR(root, pdf):
    pdfpath = root + "/" + pdf
    pages = convert_from_path(pdf_path=pdfpath, grayscale=True, dpi=200)
    text = str()
    for page in pages:
        text += pytesseract.image_to_string(page)
    return text


def imageToText():
    for file in Files:
        for image in file.imageFiles:
            imgpath = file.root + "/" + image
            img = cv2.imread(imgpath)
            Texts.append(Text(path=imgpath, content=pytesseract.image_to_string(
                img), state=False, matches=list()))


def keywordDetector():
    for text in Texts:
        for keyword in KEYWORDS:
            if keyword in text.content:
                text.state = True
                text.matches.append(keyword)


def regexDetector():
    for text in Texts:
        for pattern in PATTERNS:
            result = re.search(str(pattern[1]), str(text.content))
            if result:
                text.state = True
                text.matches.append(pattern[0])


def placeFiles(move: bool):
    global pdCount
    global PATH

    makeDirectory(PATH + PD_PATH)
    makeDirectory(PATH + NONPD_PATH)

    with open(PATH + ROOT_PATH + "/results.csv", mode="w") as csvFile:
        for text in Texts:
            fileName = text.path.split("/")[-1]
            prefix = text.path.replace(fileName, "")
            suffix = prefix.replace(PATH, "")
            dst = str("")
            if text.state:
                pdCount += 1
                dst = PATH + PD_PATH + suffix
            else:
                dst = PATH + NONPD_PATH + suffix
            makeDirectory(dst)
            if move:
                os.replace(text.path, dst + fileName)
            else:
                shutil.copyfile(text.path, dst + fileName)
            csvWriter = csv.writer(
                csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csvWriter.writerow([text.path, text.state, text.matches])
            print(text.path, text.state, text.matches)


def start(Path: str, args: any):
    global PATH
    PATH = Path
    startTime = time.time()
    print("\nProgram çalışmaya başladı.")
    getFiles()
    pdfToText()
    imageToText()
    if args.regex is not None:
        readPatterns(file=args.regex)
        regexDetector()
    if args.keywords is not None:
        readKeywords(csvFile=args.keywords)
        keywordDetector()
    placeFiles(args.move)

    print(time.time()-startTime, "saniyede", len(Texts),
          "adet dosya işlendi. Bunlardan", pdCount, "tanesi kişisel veri içeriyordu.\n")
