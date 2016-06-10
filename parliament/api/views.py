import api.database as db
import api.utils as utils
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello XML.")
