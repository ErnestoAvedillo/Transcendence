import requests
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import logging
import json
from django.conf import settings 

logger = logging.getLogger('django')
logger.setLevel(logging.DEBUG)



from django.http import HttpResponse
def index(request):
    with open("/home/luis/proyects/Transcendence/gateway/gateway/index.html", 'r') as file:
        file_content = file.read()
    return HttpResponse(file_content, content_type='text/html')


def custom_404_view(request, exception=None):
    response_data = {
        'status': 'error',
        'message': 'The requested resource was not found',
        'data': None
    }
    return JsonResponse(response_data, status=404)


def match(request, subpath):
    data = json.loads(request.body) 
    response = requests.post(f'http://matches:8000/match/{subpath}/', json=data)
    return JsonResponse(response.json(), status=response.status_code)


def user(request, subpath):
    response = None
    try:
        if request.method == "POST": 
            try:
                data = json.loads(request.body) 
            except json.JSONDecodeError:
                    return JsonResponse({'status': 'error', 'message':'Invalid Json body', 'data' : None}, status=400)
            response = requests.post(f'http://usermanagement:8000/user/{subpath}/', json=data)
        elif request.method == "GET":
            response = requests.get(f'http://usermanagement:8000/user/{subpath}')
        try:
            response_data = response.json()
            return JsonResponse(response_data, status=response.status_code)
        except ValueError:
            # DJANGO Returns HTMLS if in DEBUG Mode, So I am just returning the HTML as DATA
            if settings.DEBUG:
                return HttpResponse(response.text, status=response.status_code, content_type='text/html')
            return JsonResponse({'status' : 'error', 'data' : None, 'message' : 'Internal error B'}, status=500)
    except:
        return JsonResponse({'status' : 'error', 'data' : None, 'message' : 'Internal error C'}, status=500)
 