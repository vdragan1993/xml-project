
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from .serializers import UserSerializer
from .utils import uri_reader, transform_document_to_html, transform_document_to_pdf
from .database import get_document_from_uri



def index(request):
    return render(request, 'api/index.html')

@csrf_exempt
def users(request):
    if request.method == 'POST':
        response = {}
        data = JSONParser().parse(request)
        username = data['user']['username']
        password = data['user']['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            serializer = UserSerializer(user)
            response['user'] = serializer.data
            return JsonResponse(response)
        else:
            response['user'] = None
            return JsonResponse(response)


@csrf_exempt
def akti(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        data = data['akt']
        #prazna polja se ne salju uopste, osim datuma, oni su None ako nisu uneseni
        #prolazak za svako polje da se vidi je li tu
        if 'naslov' in data: naslov = data['naslov']
        else: naslov= None

        if 'predlagac' in data: predlagac = data['predlagac']
        else: predlagac= None

        if 'status' in data: status= data['status']
        else: status= None

        if 'kategorija' in data: kategorija = data['kategorija']
        else: kategorija= None

        if 'za_od' in data: za_od = data['za_od']
        else: za_od= None

        if 'za_do' in data: za_do = data['za_do']
        else: za_do= None

        if 'protiv_od' in data: protiv_od = data['protiv_od']
        else: protiv_od= None

        if 'protiv_do' in data: protiv_do = data['protiv_do']
        else: protiv_do= None

        if 'uzdrzani_od' in data: uzdrzani_od = data['uzdrzani_od']
        else: uzdrzani_od= None

        if 'uzdrzani_do' in data: uzdrzani_do = data['uzdrzani_do']
        else: uzdrzani_do= None

        if 'glasnik' in data: glasnik = data['glasnik']
        else: glasnik= None

        if 'operator' in data:
            op = data['operator']
        else:
            op = None

        #pretrazi akte na osnovu parametara
        #serijalizuj ih i smjeti u listu
        list = []
        list.append({'uri': 'uri', 'name': 'Naslov 1', 'type': "Akt", 'proces': "Usvojen"})
        list.append({'uri': predlagac, 'name':naslov, 'type': kategorija, 'proces':status})
        #return lista
        return JsonResponse(list, safe=False)

@csrf_exempt
def aktPdf(request):
    if request.method == 'POST':
        uri_json = JSONParser().parse(request)
        uri = uri_json['uri']
        file_path = get_document_from_uri(uri)
        name, collection, doc_type, status = uri_reader(uri)
        tip = 'amendment'
        if doc_type == 'akt':
            tip = 'act'
        pdf_file_path = transform_document_to_pdf(file_path, tip)
        f = open(pdf_file_path, 'rb')
        pdf = f.read()
        f.close()
        file_name = uri.split("/")[1]
        response = HttpResponse(pdf, 'applicatiion/pdf')
        response['Content-Disposition'] = 'attachment; filename='+file_name
        return response
    

@csrf_exempt
def aktXml(request):
    if request.method == 'POST':
        uri_json = JSONParser().parse(request)
        uri = uri_json['uri']
        file_path = get_document_from_uri(uri)
        f = open(file_path, 'rb')
        data = f.read()
        f.close()
        file_name = uri.split("/")[1]
        response = HttpResponse(data, 'application/xml')
        response['Content-Disposition'] = 'attachment; filenmame='+file_name
        return response


@csrf_exempt
def aktHtml(request):
    if request.method == 'POST':
        uri_json = JSONParser().parse(request)
        uri = uri_json['uri']
        file_path = get_document_from_uri(uri)
        name, collection, doc_type, status = uri_reader(uri)
        tip = 'amendment'
        if doc_type == 'akt':
            tip = 'act'
        html_file_path = transform_document_to_html(file_path, tip)
        f = open(html_file_path, 'rb')
        data = f.read()
        f.close()
        file_name = uri.split("/")[1]
        response = HttpResponse(data, 'text/html')
        response['Content-Disposition'] = 'attachment; filename='+file_name
        return response


@csrf_exempt
def create_conference(request):
    if request.method == 'POST':
        print("pozvao view new conference")
        data = JSONParser().parse(request)
        data = data['conference']
        print(data)
        if 'for' in data:
            za = data['for']
        if 'against' in data:
            protiv = data['against']
        if 'abstained' in data:
            uzdrzani = data['abstained']
        if 'president' in data:
            predsednik = data['president']
        if 'received' in data:
            usvojeni = data['received']
        list = []
        list.append({'president': predsednik, 'for': za, 'against': protiv, 'abstained': uzdrzani, 'received': usvojeni})
        for i in list:
            print(i)
        #return lista
        return JsonResponse(list, safe=False)


@csrf_exempt
def simple_search(request):
    if request.method == 'POST':
        print("pozvao view simple search")
        data = JSONParser().parse(request)
        data = data['ssearch']
        print(data)
        return JsonResponse(data, safe=False)


@csrf_exempt
def create_act(request):
    if request.method == 'POST':
        print("pozvao view create act")
        data = JSONParser().parse(request)
        data = data['act']
        if 'title' in data:
            naslov = data['title']
        if 'content' in data:
            sadrzaj = data['content']
        list = []
        list.append({'title': naslov, 'content': sadrzaj})
        print(list)
        return JsonResponse(list, safe=False)


@csrf_exempt
def create_amendment(request):
    if request.method == 'POST':
        print("pozvao view create amandman")
        data = JSONParser().parse(request)
        data = data['amendment']
        if 'title' in data:
            naslov = data['title']
        if 'content' in data:
            sadrzaj = data['content']
        if 'act' in data:
            akt = data['act']
        list = []
        list.append({'title': naslov, 'content': sadrzaj, 'act': akt})
        print(list)
        return JsonResponse(list, safe=False)


@csrf_exempt
def get_all(request):
    f = open('api/data/content.txt', 'r')
    lines = f.readlines()
    f.close()
    ret_val = []
    for line in lines:
        line = line[:-1]
        name, collection, doc_type, status = uri_reader(line)
        ret_val.append({'uri': line, 'name': name, 'type': doc_type, 'proces': status})
    return JsonResponse(ret_val, safe=False)