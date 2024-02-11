import os, requests
from bs4 import BeautifulSoup
from zipfile import ZipFile,ZIP_DEFLATED
from urllib.parse import urlparse

def get_hrefs(id, value):
    return soup.find_all(attrs={id: value})

def zip_folder(zip_name, zipped_folder):
    with ZipFile(zip_name, "w", ZIP_DEFLATED) as zip_object:
        for folder_name, sub_folders, file_names in os.walk(zipped_folder):
            for filename in file_names:
                file_path = os.path.join(folder_name, filename)
                zip_object.write(file_path, os.path.basename(file_path))

def download_and_zip_anexos(hrefs):
    anexos = [] 

    for anexo in hrefs:
        get_anexo = anexo.get("href")

        if ".pdf" in get_anexo:
            if "Anexo_I" in get_anexo or "Anexo_II" in get_anexo:
                anexos.append(get_anexo)

    for anexo in anexos:
        anexo_stream = requests.get(anexo)
        url_parsed = urlparse(anexo)
        file_name = url_parsed.path.split("/")[-1]

        with open(f"{os.getcwd()}" + "/anexos/" + file_name, "wb") as file:
            file.write(anexo_stream.content)
    
    zip_folder(os.getcwd() + "/anexos.zip", os.getcwd() + "/anexos")

html = requests.get(
    "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    ).content

soup = BeautifulSoup(html, 'html.parser')

hrefs = get_hrefs("class", "internal-link")

download_and_zip_anexos(hrefs)