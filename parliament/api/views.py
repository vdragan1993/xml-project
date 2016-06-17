
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from .serializers import UserSerializer


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


def aktPdf(request):
    '''
    Ovako sam ja za IIS radila download pdf-a, ovo dole ['Content-Disposition'] je da ga ne otvara nego downloaduje

    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    file = open('test.pdf', "w+b")
    pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file,encoding='utf-8')
    file.seek(0)
    pdf = file.read()
    file.close()
    response = HttpResponse(pdf, 'application/pdf')
    response['Content-Disposition'] = 'attachment; filename=name.pdf'
    return response'''


def aktXml(request):
    print("gadjaj uri i povuci xml")


def aktHtml(request):
    print("isto sr**e")


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