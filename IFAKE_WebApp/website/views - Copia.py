import datetime
from django.shortcuts import render, redirect, HttpResponseRedirect
import asyncio
from multiprocessing import Pool
import numpy as np
import subprocess


#import streamlit as st
import sys
import os
from website.ImageForgeryDetection.FakeImageDetector import FID
##from website.videoForgeryDetection.videoFunctions import *
from django.core.files.storage import FileSystemStorage

import website.ImageForgeryDetection.double_jpeg_compression as djc  # ADD1
import website.ImageForgeryDetection.noise_variance as nvar
import website.ImageForgeryDetection.copy_move_cfa as cfa
import website.ImageForgeryDetection.copy_move_sift as sift

from optparse import OptionParser
from json import dumps
from pdf2image import convert_from_path


from website.VideoForgeryDetection.detect_video import detect_video_forgery
from PIL import Image
from PIL.ExifTags import TAGS
from .forensic_analyzer import ForensicAnalyzer


# Create your views here.

fileurl = ''
inputImageUrl = ''
result = {}
inputVideoUrl = ''
fileVideoUrl = ''
infoDict = {}
inputImage=''


def getMetaData(path):
    global infoDict
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS

        # Abrir imagem
        image = Image.open(path)

        # Informações básicas
        infoDict = {
            "Format": image.format,
            "Mode": image.mode,
            "Size": f"{image.size[0]}x{image.size[1]}",
        }

        # Tentar extrair EXIF
        try:
            exif = image.getexif()
            if exif:
                for tag_id in exif:
                    tag = TAGS.get(tag_id, tag_id)
                    data = exif.get(tag_id)
                    infoDict[tag] = str(data)
        except:
            pass

    except Exception as e:
        print(f"Erro ao extrair metadados: {e}")
        infoDict = {"Error": "Não foi possível extrair metadados"}


def get_video_metadata(filename):
    result = subprocess.Popen(['hachoir-metadata', filename, '--raw', '--level=3'],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    results = result.stdout.read().decode('utf-8').split('\r\n')

    properties = {}

    for item in results:

        if item.startswith('- duration: '):
            duration = item.lstrip('- duration: ')
            if '.' in duration:
                t = datetime.datetime.strptime(item.lstrip('- duration: '), '%H:%M:%S.%f')
            else:
                t = datetime.datetime.strptime(item.lstrip('- duration: '), '%H:%M:%S')
            seconds = (t.microsecond / 1e6) + t.second + (t.minute * 60) + (t.hour * 3600)
            properties['duration'] = round(seconds)

        if item.startswith('- width: '):
            properties['width'] = int(item.lstrip('- width: '))

        if item.startswith('- height: '):
            properties['height'] = int(item.lstrip('- height: '))

    return properties


def index(request):
    return render(request, "index.html")


def video(request):
    return render(request, "video.html")


def image(request):
    return render(request, "image.html")


def pdf(request):
    return render(request, "pdf.html")


#pdf2image for loop
def runPdf2image(request):
    global filePdfUrl, inputPdfUrl
    if request.POST.get('run'):
        inputPdf = request.FILES['input_pdf'] if 'input_pdf' in request.FILES else None
        if inputPdf:
            fs = FileSystemStorage()
            file = fs.save(inputPdf.name, inputPdf)
            fileurl = fs.url(file)
            inputPdfUrl = '../media/' + inputPdf.name
            fileurl = os.getcwd() + '/media/' + inputPdf.name
            images = convert_from_path(fileurl)
            imageurl = []
            pdfImagesResults=[]
            for i in range(len(images)):
                # Save pages as images in the pdf
                images[i].save(fileurl.strip(".pdf") + 'page' + str(i) + '.jpg', 'JPEG')
                #This list is used to generate table on pdf.html
                pageName=inputPdf.name.strip(".pdf") + 'page' + str(i) + '.jpg'
                imageurl.append('../media/' + pageName)
                imagefileurl = os.getcwd()  +'/media/'+pageName
                res = FID().predict_result(imagefileurl)
                result = {'type': res[0], 'confidence': res[1]}
                pdfImagesResults.append(result)
            res=zip(imageurl,pdfImagesResults)

        return render(request, "pdf.html", {'input_pdf': inputPdfUrl, 'pdf_img': res,})

    if request.POST.get('passImage'):
            global inputImageUrl, inputImage
            inputImage=''
            counter = request.POST.get('passImage')
            inputImageUrl = request.POST.get('image_url-'+counter)
            return render(request, "image.html",{'input_image': inputImageUrl,})



def runAnalysis(request):
    global fileurl, inputImageUrl, result, infoDict,inputImage
    
    if request.POST.get('run'):
            inputImage=''
            if inputImageUrl=='' or 'input_image' in request.FILES:   
                inputImg = request.FILES['input_image'] if 'input_image' in request.FILES else None
                if inputImg:
                    fs = FileSystemStorage()
                    file = fs.save(inputImg.name, inputImg)
                    fileurl =  os.getcwd() +fs.url(file)
                    inputImageUrl = '../media/' + inputImg.name
            elif inputImageUrl!='':
                #inputImageUrl = inputImageUrl
                fileurl = os.getcwd() + '/media/' + os.path.basename(inputImageUrl)

            getMetaData(fileurl)
            print('fileurl---------------------------',fileurl)
            res = FID().predict_result(fileurl)

            if res[0] == 'Authentic':
                result = {'type': res[0], 'confidence': res[1]}
                inputImage=inputImageUrl
                inputImageUrl=''

                return render(request, "image.html",
                              {'result': result, 'input_image': inputImage, 'metadata': infoDict.items()})

            elif res[0] == 'Forged':
                # cmd = OptionParser("usage: %prog image_file [options]")
                # cmd.add_option('', '--imauto', help='Automatically search identical regions. (default: %default)', default=1)
                # cmd.add_option('', '--imblev',help='Blur level for degrading image details. (default: %default)', default=8)
                # cmd.add_option('', '--impalred',help='Image palette reduction factor. (default: %default)', default=15)
                # cmd.add_option('', '--rgsim', help='Region similarity threshold. (default: %default)', default=5)
                # cmd.add_option('', '--rgsize',help='Region size threshold. (default: %default)', default=1.5)
                # cmd.add_option('', '--blsim', help='Block similarity threshold. (default: %default)',default=200)
                # cmd.add_option('', '--blcoldev', help='Block color deviation threshold. (default: %default)', default=0.2)
                # cmd.add_option('', '--blint', help='Block intersection threshold. (default: %default)', default=0.2)
                # opt, args = cmd.parse_args()
                # if not args:
                #     cmd.print_help()
                #     sys.exit()
                # im_str = args[0]

                # print('\nRunning double jpeg compression detection...\n')
                # double_compressed = djc.detect(fileurl)      # check type of forgery
                # if(double_compressed): compression= 'Double compressed'
                # else: compression= 'Single compressed'

                # print('\nRunning noise variance inconsistency detection...')
                # noise_forgery = nvar.detect(fileurl)

                # if(noise_forgery): noise_var=1
                # else: noise_var= 0

                # print('\nRunning CFA artifact detection...\n')
                # identical_regions_cfa = cfa.detect(fileurl, opt, args)
                # identical_regions = dumps(identical_regions_cfa)
                # print(identical_regions_cfa, 'identical regions detected')

                # res= FID().predict_result(fileurl) called above
                
                result = {'type': res[0], 'confidence': res[
                    1]}  # 'compression':compression, 'noise_var':noise_var, 'identical_regions': identical_regions}
                inputImage=inputImageUrl
                inputImageUrl=''
                return render(request, "image.html",
                              {'result': result, 'input_image': inputImage, 'metadata': infoDict.items()})


def runVideoAnalysis(request):
    global inputVideoUrl, fileVideoUrl
    if request.POST.get('run'):
        input_video = request.FILES['input_video'] if 'input_video' in request.FILES else None
        if input_video:
            fs = FileSystemStorage()
            file = fs.save(input_video.name, input_video)
            inputVideoUrl = '../media/' + input_video.name
            fileVideoUrl = os.getcwd() + '/media/' + input_video.name
            # getProcessingVideo()
            return render(request, "video.html", {'input_video': inputVideoUrl, })

    if request.POST.get('detect'):
        properties = get_video_metadata(fileVideoUrl)
        result = detect_video_forgery(fileVideoUrl)
        return render(request, "video.html",
                      {'input_video': inputVideoUrl, 'result': result, 'metadata': properties.items()})


def getImages(request):
    global fileurl, inputImageUrl, result,inputImage
    outputImageUrl = "../media/tempresaved.jpg"
    if request.POST.get('mask'):
        FID().genMask(fileurl)
        return render(request, "image.html", {'url': outputImageUrl, 'input_image': inputImage, 'result': result,
                                              'metadata': infoDict.items()})

    if request.POST.get('ela'):
        FID().show_ela(fileurl)
        return render(request, "image.html", {'url': outputImageUrl, 'input_image': inputImage, 'result': result,
                                              'metadata': infoDict.items()})

    if request.POST.get('edge_map'):
        FID().detect_edges(fileurl)
        return render(request, "image.html", {'url': outputImageUrl, 'input_image': inputImage, 'result': result,
                                              'metadata': infoDict.items()})

    if request.POST.get('lum_gradiend'):
        outputImageUrl = "../media/luminance_gradient.tiff"
        FID().luminance_gradient(fileurl)
        return render(request, "image.html", {'url': outputImageUrl, 'input_image': inputImage, 'result': result,
                                              'metadata': infoDict.items()})

    if request.POST.get('na'):
        FID().apply_na(fileurl)
        return render(request, "image.html", {'url': outputImageUrl, 'input_image': inputImage, 'result': result,
                                              'metadata': infoDict.items()})
    if request.POST.get('copy_move_sift'):
        cmsift = sift.CopyMoveSIFT(fileurl)
        return render(request, "image.html", {'url': outputImageUrl, 'input_image': inputImage, 'result': result,
                                              'metadata': infoDict.items()})

def pdf(request):
    """
    Lida com a página de análise de documentos, agora com tradução.
    """
    # Dicionário para traduzir os campos do relatório
    TRANSLATION_MAP = {
        'File Type': 'Tipo de Arquivo',
        'Author': 'Autor',
        'Creator': 'Software Criador',
        'Producer': 'Software Produtor (PDF)',
        'Created Date': 'Data de Criação (Documento)',
        'Modified Date': 'Data de Modificação (Documento)',
        'Page Count': 'Contagem de Páginas',
        'Sheet Count': 'Contagem de Planilhas',
        'Last Printed': 'Última Impressão',
        'Revision': 'Número da Revisão',
        'Size Bytes': 'Tamanho (Bytes)',
        'Last Modified': 'Última Modificação (Sistema)',
        'Created': 'Criação (Sistema)',
        'File Name': 'Nome do Arquivo',
        # Adicione outras chaves que possam aparecer aqui
    }

    if request.method != 'POST':
        context = {'description_text': get_forensic_tools_description()}
        return render(request, "pdf.html", context)

    doc1 = request.FILES.get('document1')
    doc2 = request.FILES.get('document2')

    if not doc1:
        context = {
            'error': 'Por favor, envie pelo menos um arquivo.',
            'description_text': get_forensic_tools_description()
        }
        return render(request, "pdf.html", context)

    fs = FileSystemStorage()
    file1_name = fs.save(doc1.name, doc1)
    file1_path = fs.path(file1_name)

    analyzer = ForensicAnalyzer()
    analysis_results = analyzer.analyze_document(file1_path)

    # --- LÓGICA DE FORMATAÇÃO E TRADUÇÃO ---
    def format_and_translate(original_dict):
        formatted_dict = {}
        for key, value in original_dict.items():
            # Formata (ex: 'created_date' -> 'Created Date')
            english_key = key.replace('_', ' ').title()
            # Traduz usando o dicionário, ou mantém a chave formatada se não houver tradução
            portuguese_key = TRANSLATION_MAP.get(english_key, english_key)
            formatted_dict[portuguese_key] = value
        return formatted_dict

    if 'file_system_metadata' in analysis_results:
        analysis_results['file_system_metadata'] = format_and_translate(analysis_results['file_system_metadata'])

    if 'document_metadata' in analysis_results and 'error' not in analysis_results['document_metadata']:
        analysis_results['document_metadata'] = format_and_translate(analysis_results['document_metadata'])
    # --- FIM DA LÓGICA ---

    if doc2:
        file2_name = fs.save(doc2.name, doc2)
        file2_path = fs.path(file2_name)
        comparison_results = analyzer.compare_files(file1_path, file2_path)
        analysis_results['comparison_results'] = comparison_results
    
    context = {
        'results': analysis_results,
        'description_text': get_forensic_tools_description()
    }
    return render(request, "pdf.html", context)

def get_forensic_tools_description():
    """
    Função auxiliar para retornar o dicionário com a descrição das ferramentas.
    """
    return {
        'title': 'Análise Forense de Documentos',
        'tools_used': 'PyPDF2, python-docx, openpyxl, hashlib.',
        'tools': [
            {'name': 'PyPDF2', 'desc': 'Biblioteca Python para leitura e extração de metadados de arquivos PDF.'},
            {'name': 'python-docx', 'desc': 'Biblioteca para manipulação e extração de informações de arquivos DOCX.'},
            {'name': 'openpyxl', 'desc': 'Biblioteca para leitura e análise de arquivos XLS/XLSX.'},
            {'name': 'hashlib', 'desc': 'Biblioteca nativa do Python para cálculo de hashes (MD5, SHA256) para verificação de integridade de arquivos.'}
        ],
        'description': 'Essas bibliotecas foram utilizadas para implementar a análise forense de documentos digitais, permitindo a extração de metadados (como autor, datas de criação/modificação) e o cálculo de hashes para verificar a integridade e detectar possíveis cópias ou alterações em arquivos PDF, DOCX e XLS/XLSX.'
    }