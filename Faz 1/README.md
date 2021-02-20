ISTEC Kişisel Veri Algılayıcı
=============================

ISTEC PDD, csv dosyası olarak verilen anahtar kelimelere ve/veya düzenli
ifadelere göre eşleşme yakalar. PDF ve görüntü dosyalarında arama yapar
ve bu dosyalara bir klasör içerisinde sınıflandırarak hangi dosyada ne
tür kişisel veri bulunduğunu gösteren bir csv çıktı üretir.

### Ön Koşullar

1.  [Python](https://www.python.org/) kurulumunu gerçekleştirin.
2.  [Tesseract](https://digi.bib.uni-mannheim.de/tesseract/)
    kütüphanesini bilgisayarınıza yükleyin.
3.  Gerekli Python paketlerini, aşağıdaki komutu terminalde çalıştırarak
    kurun.
```
pip3 install -r requirements.txt
```

### Nasıl Çalışır?

Ön koşulları tamamladıkran sonra klasörde terminali açın ve aşağıdaki
komutu isteğinize göre şekillendirerek çalıştırın.
```
python3 main.py -p <path> -k <keywords.csv> -r <patterns.txt> -m
```

-   -p \<path\> paremetresi ile programın analiz edeceği klasörün yolu
    verilir. (Zorunlu)
-   -k \<keywords.csv\> parametresi ile csv formatında anahtar
    kelimelerin bulunduğu dosyanın yolu belirtilir. (İsteğe Bağlı)
-   -r \<patterns.txt\> parametresi ile düzenli ifadelerin bulunduğu
    dosyanın yolu belirtilir. (İsteğe Bağlı)
-   -m parametresi verilirse dosyalar bulunduğu konumdan taşınır, bu
    parametre verilmez ise dosyaların yapısı korunur ve kopyası
    oluşturulur.

