import PyPDF2
import re
import xlwt
from xlwt import Workbook
import csv

# -*- coding: cp1254 -*-
wb = Workbook()


class objects:
    def __init__(self, name, count, regex):
        self.name = name
        self.count = count
        self.regex = regex


with open('isimler_w.txt', 'r') as file:
    str1 = ""

    for ele in file.readlines():
        str1 += ele

wordlistisim = str1.split(' ')
isim_soyisim_regex = '''(((([A-Z]{1})[a-z]+)\s){1,3})((([A-Z]{1})[a-z]+)|([A-Z]+))'''
array = ["kredi_banka_", "telefon", "ipv4", "ipv6", "email",
         "date", "sabit_telefon", "plaka", "iban", "adres", "tc_no", "dogum_tarihi"]
liste = ['''([0-9]{4})\s?([0-9]{4})\s?([0-9]{4})\s?([0-9]{4})''',
         '''(05|5|905)([0-9]{2})\s?([0-9]{3})\s?([0-9]{2})\s?([0-9]{2})''',
         '''(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)''',
         '''(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}| 
        ([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:) 
        {1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1 
        ,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4} 
        :){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{ 
        1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA 
        -F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a 
        -fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0 
        -9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0, 
        4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1} 
        :){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9 
        ])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0 
        -9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4] 
        |1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4] 
        |1{0,1}[0-9]){0,1}[0-9]))''', '''([a-z0-9!#$%&'*+\/=?^_`{|.}~-]+@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)''','''\d{1,2}/\d{1,2}/\d{4}''',
         '''(0|90?)(\s?)(322|416|272|472|382|358|312|242|478|466|256|266|378|488|458|228|426|434|374|248|224|286|376|364|258|412|380|284|424|446|442|222|342|454|456|438|326|476|246|324|212|216|232|370|338|474|366|352|318|288|386|348|344|262|332|274|422|236|482|252|436|384|388|452|328|464|264|362|484|368|346|414|486|282|356|462|428|276|432|226|354|372|392)(\s?)([0-9]{3})(\s?)([0-9]{2})(\s?)([0-9]{2})''',
         '''(([0-8][0-9])(\s)(([A-Z]{1})|([a-z]{1}))(\s)(\d{4,5}))|(([0-8][0-9])(\s)(([A-Z]{2})|([a-z]{2}))(\s)(\d{3,4}))|(([0-8][0-9])(\s)(([A-Z]{3})|([a-z]{3}))(\s)(\d{2,3}))''',
         '''((IBAN|iban|Iban)(\s?\:?\s?))*((TR|tr)([0-9]{24})|(TR|tr)([0-9]{2})(\s)([0-9]{4})(\s)([0-9]{4})(\s)([0-9]{4})(\s)([0-9]{4})(\s)([0-9]{4})(\s)([0-9]{2}))''',
         '''([^ ]+?) (\s[A-Za-z0-9.-](?=) )?(.*?) (?:Sokak|Cadde|Yol|Bulvar|Mahalle|mah|Mah|sok|cad|Sok|Cad|No|Daire)\W?(?=\s|$)''',
         '''[1-9]{1}[0-9]{9}[02468]{1}''',
         '''^(?:(?:31(/|-|.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(/|-|.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(/|-|.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(/|-|.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})''']
listofobjects = []
count = 0
for i in array:
    listofobjects.append(objects(array[count], 0, liste[count]))
    count = count+1

kredi_banka_ = []
telefon_ = []
plaka_ = []
ipv4_ = []
ipv6_ = []
iban_ = []
email_ = list()
date_ = []
sabit_telefon_ = []
adres_ = []
tc_no_ = []
dogum_tarihi_ = []

input1 = input()

def readtextfiles():
    
    with open(input1, 'r') as file:
        str1 = ""

        for ele in file.readlines():
            str1 += ele

    return str1


            
   
    
def controlisim(str):

    for isim in wordlistisim:
        if str == isim:
            return 1


result_set = []


def isValidTCID(value):
    value = str(value)

    if not len(value) == 11:
        return False

    if not value.isdigit():
        return False

    if int(value[0]) == 0:
        return False

    digits = [int(d) for d in str(value)]

    if not sum(digits[:10]) % 10 == digits[10]:
        return False

    if not (((7 * sum(digits[:9][-1::-2])) - sum(digits[:9][-2::-2])) % 10) == digits[9]:
        return False

    return True


def read_name_surname():
    textf = readtextfiles()
    res = textf.split(' ')
    isim = ''
    for i in range(0, len(res), 1):
        if controlisim(res[i]) == 1 and controlisim(res[i+1]) == 1 and controlisim(res[i+2]) == 1 and controlisim(res[i+3]) != 1:
            isim = isim+res[i]+' '+res[i+1]+' '+res[i+2]+' '+res[i+3]
            matches = re.search(isim_soyisim_regex, isim)
            if matches:
                result_set.append(isim)
            res[i] = ''
            res[i+1] = ''
            res[i+2] = ''
            res[i+3] = ''
            isim = ''
        elif controlisim(res[i]) == 1 and controlisim(res[i+1]) == 1 and controlisim(res[i+2]) != 1:
            isim = isim+res[i]+' '+res[i+1]+' '+res[i+2]
            matches = re.search(isim_soyisim_regex, isim)
            if matches:
                result_set.append(isim)
            res[i] = ''
            res[i+1] = ''
            res[i+2] = ''
            isim = ''
        elif controlisim(res[i]) == 1 and controlisim(res[i+1]) == 1 and controlisim(res[i+2]) == 1 and controlisim(res[i+3]) == 1:
            isim = isim+res[i]+' '+res[i+1]+' '+res[i+2]+' '+res[i+3]
            matches = re.search(isim_soyisim_regex, isim)
            if matches:
                result_set.append(isim)
            res[i] = ''
            res[i+1] = ''
            res[i+2] = ''
            res[i+3] = ''
            isim = ''
        elif controlisim(res[i]) == 1 and controlisim(res[i+1]) == 1 and controlisim(res[i+2]) == 1:
            isim = isim+res[i]+' '+res[i+1]+' '+res[i+2]
            matches = re.search(isim_soyisim_regex, isim)
            if matches:
                result_set.append(isim)
            res[i] = ''
            res[i+1] = ''
            res[i+2] = ''
            isim = ''
        elif controlisim(res[i]) == 1 and controlisim(res[i+1]) != 1:
            isim = isim+res[i]+' '+res[i+1]
            matches = re.search(isim_soyisim_regex, isim)
            if matches:
                result_set.append(isim)
            res[i] = ''
            res[i+1] = ''
            isim = ''
        elif controlisim(res[i]) == 1 and controlisim(res[i+1]) != 1:
            isim = isim+res[i]+' '+res[i+1]
            matches = re.search(isim_soyisim_regex, isim)
            if matches:
                result_set.append(isim)
            res[i] = ''
            res[i+1] = ''
            isim = ''


def read_and_write():
    str2 = readtextfiles()
    for i in range(0, len(listofobjects), 1):
        matches = re.findall(listofobjects[i].regex, str2)
        if matches:
            if listofobjects[i].name == 'email':
                for match in matches:
                    email_.append(match)
            elif listofobjects[i].name == 'telefon':
                for match in matches:
                    temp = "".join(match)
                    telefon_.append(temp)
              
            elif listofobjects[i].name == 'iban':
                for match in matches:
                    temp = "".join(match)
                    iban_.append(temp)
            elif listofobjects[i].name == 'ipv4':
                for match in matches:
                    temp = "".join(match)
                    ipv4_.append(temp)
                
            elif listofobjects[i].name == 'ipv6':
                for match in matches:
                    temp = "".join(match)
                    ipv6_.append(temp)
               
            elif listofobjects[i].name == 'kredi_banka':
                for match in matches:
                    temp = "".join(match)
                    kredi_banka_.append(temp)
              
            elif listofobjects[i].name == 'sabit_telefon':
                for match in matches:
                    temp = "".join(match)
                    sabit_telefon_.append(temp)
            elif listofobjects[i].name == 'plaka':
                for match in matches:
                    plaka_.append(match)

            elif listofobjects[i].name == 'tc_no':
                for match in matches:
                    if isValidTCID(match):
                        tc_no_.append(match)

           # elif listofobjects[i].name == 'adres':
            #    for match in matches:
             #       temp = "".join(match)
              #      adres_.append(temp)
          
            elif listofobjects[i].name == 'date':
                 for match in matches:
                     date_.append(match)
    read_name_surname()
    write_excel("email", email_)
    write_excel("telefon", telefon_)
    write_excel("isim_soyisim", result_set)
    write_excel("iban", iban_)
    write_excel("ipv4", ipv4_)
    write_excel("ipv6", ipv6_)
    write_excel("plaka", plaka_)
    write_excel("sabit_telefon", sabit_telefon_)
    write_excel("date", date_)
    write_excel("tc_no", tc_no_)
    
 
    


def write_excel(sheet_name, list_name):
    sheet1 = wb.add_sheet(sheet_name)
    for i in range(0, len(list_name), 1):
        sheet1.write(i, 0, list_name[i])



def main():
    read_and_write()
    wb.save('outputs.xls')
   

if __name__ == "__main__":
    main()
