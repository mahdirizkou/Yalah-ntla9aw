from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt # i want testin postman 
from django.contrib.auth.hashers import make_password, check_password
from user.models import User

@csrf_exempt
def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already registered"}, status=400)

        hashed_password = make_password(password)

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
            type="member"  
        )

        
        request.session['user_id'] = user.id_user

        return JsonResponse({
            "message": "User registered successfully",
            "user": {
                "id": user.id_user,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "type": user.type
            }
        }, status=201)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({"error": "Email or password incorrect"}, status=400)

        if check_password(password, user.password):
            request.session['user_id'] = user.id_user
            return JsonResponse({
                "message": "Login successful",
                "user": {
                    "id": user.id_user,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "type": user.type
                }
            })
        else:
            return JsonResponse({"error": "Email or password incorrect"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
