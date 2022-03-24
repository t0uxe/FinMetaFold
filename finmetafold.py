# -*- encoding: utf-8 -*-

import argparse
import os
from PyPDF2 import PdfFileReader, PdfFileWriter, utils
from rich.console import Console
from rich._emoji_codes import EMOJI
from rich.table import Column, Table
console = Console()

def print_title():

    star = EMOJI['star']
    console.print(f"""[blue b]
{star*13}
 +-+-+-+-+-+-+-+-+-+-+-+
 |F|i|n|M|e|t|a|F|o|l|d| :blue_heart:
 +-+-+-+-+-+-+-+-+-+-+-+ 
{star*13}
    """)
    print()

def __prepare_table():
    table = Table(show_lines=False)
    table.add_column("[magenta]Field", style="dim", footer="lala")
    table.add_column("[magenta]Information")
    return table

def __readable_date(date):
    year = date[2:6]
    month = date[6:8]
    day = date[8:10]
    hour = date[10:12]
    minutes = date[12:14]

    readable_date = day + "/" + month + "/" + year + " - " + hour + ":" + minutes
    return readable_date

def __readable_dates(doc_info):
    if '/ModDate' in doc_info:
        doc_info['/ModDate'] = __readable_date(doc_info['/ModDate'])
    if "/CreationDate" in doc_info:
        doc_info['/CreationDate'] = __readable_date(doc_info['/CreationDate'])
    return doc_info


def printMeta(directory):
    for dirpath, dirnames, files in os.walk(directory): #para el diretorio, nombre y archivos en la carpeta docs
        for name in files: #recorremos los posibles fichreos
            ext = name.lower().rsplit('.', 1)[-1] # obtenemos la extensión del archivo a escanear
            if ext.lower() == "pdf":
                full_path_file = dirpath+os.path.sep+name
                
                # Abrimos el fichero para su lectura                
                with open(full_path_file, 'rb') as filepdf:
                    try:
                        pdfFile = PdfFileReader(filepdf, strict=False)
                        docInfo = pdfFile.getDocumentInfo() #creamos un diccionario con la info recolectada
                        if docInfo is not None:
                            docInfo = dict(docInfo)
                            console.rule(f"[bold magenta][i]{name}[/i]", style="bold")
                            table = __prepare_table()

                            if "/ModDate" or "/CreationDate" in docInfo:
                                try:
                                    docInfo = __readable_dates(docInfo)
                                except TypeError:
                                    pass

                            [table.add_row(str(metaItem[1:]), str(docInfo[metaItem])) for  metaItem in docInfo]
                            console.print(f":open_file_folder:[green b] Path: [cyan]{full_path_file}[/cyan]")
                            console.print(table)
                        print()
                    except utils.PdfReadError:
                        continue
                    except OSError:
                        continue

def check_arguments():
    parser = argparse.ArgumentParser(description='Directorio donde están los pdf.')
    parser.add_argument('directory', help='directorio a escanear')
    
    args = parser.parse_args()
    return args.directory

def main():
    directorio = check_arguments()
    if not os.path.isdir(directorio):
        console.print("\n[white on red blink][ERROR] El directorio no existe\n")
    else:
        print()
        print_title()
        printMeta(directorio)
    

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n\n--- Programa terminado por el usuario ---\n")