from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import OperationalError
from django.conf import settings
from django.contrib.auth import authenticate, login, logout, get_user_model
from .wrappers import validate_credentials, require_post, require_get
import json
import logging

#If testing we dont have usermodel.User so we want to use default
try:
    from usermodel.models import User
except:
    pass
from .models import UserStatus
User = get_user_model()



if not settings.DEBUG:
    logger = logging.getLogger('django')
    logger.setLevel(logging.DEBUG)

def custom_404_view(request, exception=None):
    response_data = {
        'status': 'error',
        'message': 'The requested resource was not found',
        'data': None
    }
    return JsonResponse(response_data, status=404)

             
@require_post
@validate_credentials
def create_user(request):
    username = request.username
    password = request.password
    try:
        user = User.objects.get(username=username)
        return JsonResponse({'status' : 'error',
                                'message' : "User already Exists",
                                'data' : None},
                                status=409)
    except User.DoesNotExist:
        user = User(username=username)
        try:
            user.set_password(password)
            user.save()
            user_status, created = UserStatus.objects.get_or_create(user=user)
        except OperationalError:
            return JsonResponse({'status' : 'error',
                                'message' : 'Internal database error',
                                'data' : None, },
                                status=500)
        return JsonResponse({'status' : 'success',
                                'message' : 'User created successfully',
                                'data' : {'id': user.id, 'username': user.username}},
                                status=201)
    except OperationalError:
        return JsonResponse({'status' : 'error',
                            'message' : 'Internal database error',
                            'data' : None},
                            status=500)
    except:
        return JsonResponse({'status' : 'error',
                        'message' : 'Internal error',
                        'data' : None,}, 
                        status=500)    
    


@require_post
@validate_credentials
def login_user(request):
    username = request.username
    password = request.password
    try:
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user_status= UserStatus.objects.get(user=user)
            user_status.change_status(True) 
            return JsonResponse({'status' : 'success',
                                'message': 'user is logged in',
                                'data' : None},
                                status=200)
        else:
            return JsonResponse({'status' : 'error',
                                    'message': 'Invalid credentials',
                                    'data' : None},
                                    status=401)
    except OperationalError:
        return JsonResponse({'status' : 'error',
                                'message' : 'Internal database error',
                                'data' : None,}, 
                                status=500)
    except:
        return JsonResponse({'status' : 'error',
                        'message' : 'Internal error',
                        'data' : None,}, 
                        status=500)
    
@require_post
def logout_user(request):
    try:
        if request.user.is_authenticated:
            user_status = UserStatus.objects.get(user=request.user)
            logout(request)
            user_status.change_status(False) 
            return JsonResponse({'status' : 'success',
                                'message': 'user has been logged out',
                                'data' : None},
                                status=200)        
        else:
            return JsonResponse({'status' : 'error',
                                    'message': 'Forbidden',
                                    'data' : None},
                                    status=403)
    except OperationalError:
        return JsonResponse({'status' : 'error',
                                'message' : 'Internal database error',
                                'data' : None,}, 
                                status=500)
    except:
        return JsonResponse({'status' : 'error',
                        'message' : 'Internal error',
                        'data' : None,}, 
                        status=500)
    

@require_get
def is_logged_in(request):
    try:
        if request.user.is_authenticated:
            return JsonResponse({'status': 'success', 
                                'message':'User is logged in', 
                                'data' : None}, 
                                status=200)
        else:
            return JsonResponse({'status': 'error', 
                                'message':'Unauthorized', 
                                'data' : None}, 
                                status=401)
    except OperationalError:
        return JsonResponse({'status' : 'error', 
                                'data' : None, 
                                'message' : 'Internal database error'}, 
                                status=500)

@require_get
def list_users(request):
    try:
        users = User.objects.all().values('id', 'username')
        return JsonResponse({'status' : 'success', 
                                'data' : list(users), 
                                'message' : 'All registered users'}, 
                                status=200)
    except OperationalError:
        return JsonResponse({'status' : 'error', 
                        'data' : None, 
                        'message' : 'Internal database error'}, 
                        status=500)


@require_get
def user_status(request):
    username = request.GET.get('username')
    if username is None:
            return JsonResponse({'status': 'error', 'message': 'No username provided', 'data': None}, status=400)
    try:
        user_status = UserStatus.objects.get(user=User.objects.get(username=username))
        return JsonResponse({'status' : 'success',
                            'message' : "Retrieved status",
                            'data' : {'is_online' : user_status.is_online}},
                            status=200)     

    except User.DoesNotExist:
        return JsonResponse({'status' : 'error',
                            'message' : "User does not exists",
                            'data' : None},
                            status=404)
    except OperationalError:
        return JsonResponse({'status' : 'error', 
                        'data' : None, 
                        'message' : 'Internal database error'}, 
                        status=500)
    
""" @require_post   
def change_status(request): """