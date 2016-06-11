import api.database as db
import api.utils as utils
from django.shortcuts import render


def index(request):
    return render(request, 'api/index.html')
