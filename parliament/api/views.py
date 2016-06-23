
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from .serializers import UserSerializer
from .utils import uri_reader, transform_document_to_html, transform_document_to_pdf, validate_document, read_metadata, set_metadata, get_proponent_for_user, insert_proponent, delete_proponent, get_all_proponents, read_metadata_from_file, extract_parent_act, set_metadata_to_file, write_conference, remove_existing_file
from .database import get_document_from_uri, text_search, advanced_search_list, insert_document_from_string, delete_document_from_uri, accept_amendment_uri, insert_document_from_file
import time


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
            #login(request, user)
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
        keys = []
        values = []

        for a in data:
            if data[a] and a!='operator':
                keys.append(a)
                if a.startswith('datum'):
                    values.append(data[a].split("T")[0])
                else:
                    values.append(data[a])

        if 'operator' in data:
            operator = data['operator']
        else:
            operator = 'AND'

        result_uris = advanced_search_list(keys, values, operator)
        ret_val = []
        if len(result_uris) == 0:
            ret_val.append({'message': 'Nema rezultata'})
        else:
            for uri in result_uris:
                name, collection, doc_type, status = uri_reader(uri)
                ret_val.append({'uri': uri, 'name': name, 'type': doc_type, 'proces': status})

        return JsonResponse(ret_val, safe=False)



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
        datum_sednice = time.strftime("%Y-%m-%d")

        akti = []
        amandmani = []
        for uri in usvojeni:
            name, collection, doc_type, status = uri_reader(uri)
            if doc_type == 'akt':
                akti.append(uri)
            else:
                amandmani.append(uri)

        # usvajam prvo amandmane
        for amandman in amandmani:
            amandman_path = get_document_from_uri(amandman)
            amandman_uri = read_metadata_from_file(amandman_path, 'uri')
            parent_act = extract_parent_act(amandman_uri)
            remove_existing_file(amandman_path)
            # usvajam amandman
            accept_amendment_uri(amandman, parent_act)
            # zamjenim kolekciju i brisem
            amandman_path = get_document_from_uri(amandman)
            insert_document_from_file(amandman_path, 'usvojeniamandmani')
            delete_proponent(amandman)
            delete_document_from_uri(amandman)
            remove_existing_file(amandman_path)



        # usvajam akte
        for akt in akti:
            akt_path = get_document_from_uri(akt)
            #set_metadata_to_file(akt_path, 'status', 'usvojen')
            insert_document_from_file(akt_path, 'usvojeniakti')
            delete_proponent(akt)
            delete_document_from_uri(akt)
            remove_existing_file(akt_path)

        #print(len(usvojeni))
        #string_to_write = predsednik+","+datum_sednice+","+za+","+protiv+","+uzdrzani+","+len(usvojeni)+"\n"
        #print(string_to_write)
        #write_conference(string_to_write)
        all_uris = get_all_proponents()
        for prop_uri in all_uris:
            delete_document_from_uri(prop_uri)

        f = open('api/data/proponent.txt', 'w')
        f.write('')
        f.close()

        ret_val = []
        ret_val.append({'message': 'Nema rezultata'})
        return JsonResponse(ret_val, safe=False)


@csrf_exempt
def simple_search(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        data = data['ssearch']
        result_uris = text_search(data)
        ret_val = []
        if len(result_uris) == 0:
            ret_val.append({'message': 'Nema rezultata'})
        else:
            for uri in result_uris:
                name, collection, doc_type, status = uri_reader(uri)
                ret_val.append({'uri': uri, 'name': name, 'type': doc_type, 'proces': status})

        return JsonResponse(ret_val, safe=False)


@csrf_exempt
def create_act(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        data = data['act']
        if 'title' in data:
            naslov = data['title']
        if 'content' in data:
            sadrzaj = data['content'].encode('utf-8')


        #predlagac_akta = 'dragan'

        predlagac_akta = read_metadata(data['content'], 'predlagac')
        #sadrzaj = sadrzaj.decode('utf-8')

        if validate_document(sadrzaj, 'act'):
            insert_document_from_string(naslov, 'procesakti', sadrzaj)
            message = 'Ok'
        else:
            message = 'No'

        # dodaj u listu za istoriju
        insert_proponent('procesakti/'+naslov, predlagac_akta)

        list = []
        list.append({'message': message})
        return JsonResponse(list, safe=False)


@csrf_exempt
def create_amendment(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        data = data['amendment']
        if 'title' in data:
            naslov = data['title']
        if 'content' in data:
            sadrzaj = data['content']
        if 'act' in data:
            akt = data['act']

        predlagac_amandmana = read_metadata(sadrzaj, 'predlagac')

        #kratak_uri = 'procesamandmani/' + naslov
        novi_uri = "http://147.91.177.194:8000/v1/documents?uri=/"+ akt +"&database=Tim20"
        sadrzaj = set_metadata(sadrzaj, 'uri', novi_uri)

        if validate_document(sadrzaj, 'amendment'):
            insert_document_from_string(naslov, 'procesamandmani', sadrzaj)
            message = 'Ok'
        else:
            message = 'No'


        # dodaj u listu dodatih
        insert_proponent('procesamandmani/'+naslov, predlagac_amandmana)

        list = []
        list.append({'message': message})
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


@csrf_exempt
def discard_document(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        target_uri = data['uri']
        # brisemo iz proponent.txt
        delete_proponent(target_uri)
        # brisemo konacno iz baze
        delete_document_from_uri(target_uri)
        ret_val = []
        ret_val.append({'message': 'Nema rezultata'})
        return JsonResponse(ret_val, safe=False)


@csrf_exempt
def load_documents_for_user(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        username = data['username']
        uris = get_proponent_for_user(username)
        ret_val = []
        for uri in uris:
            name, collection, doc_type, status = uri_reader(uri)
            ret_val.append({'uri': uri, 'name': name, 'type': doc_type, 'proces': status, 'proponent': username})

        return JsonResponse(ret_val, safe=False)


@csrf_exempt
def load_process_documents(request):
    if request.method == 'GET':
        uris = get_all_proponents()
        ret_val = []
        for uri in uris:
            name, collection, doc_type, status = uri_reader(uri)
            ret_val.append({'uri': uri, 'name': name, 'type': doc_type, 'proces': status})

        return JsonResponse(ret_val, safe=False)