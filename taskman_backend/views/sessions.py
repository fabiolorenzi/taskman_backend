from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from taskman_backend.serializers.sessionSerializer import SessionSerializer
from taskman_backend.serializers.userSerializer import UserSerializer
from taskman_backend.models.session import Session
from taskman_backend.models.user import User
from datetime import datetime, timedelta
from tools.security import generatePasscode

@api_view(["POST"])
def all_sessions(request):
    if request.method == "POST":
        email = request.data["email"]
        password = request.data["password"]

        all_users = User.objects.filter(email=email)
        all_users_ser = UserSerializer(all_users, many = True)

        for user in all_users_ser.data:
            if user["email"] == email and user["password"] == password:
                serializedData = SessionSerializer(data={
                    "user": user["id"],
                    "passcode": generatePasscode(user["id"]),
                    "expire": datetime.now() + timedelta(hours=8)
                })
                if serializedData.is_valid():
                    serializedData.save()
                    return JsonResponse(data={"data": serializedData.data}, status=status.HTTP_201_CREATED)
                return JsonResponse(data={"message": "The body is not valid"}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(data={"message": "Login failed"}, status=status.HTTP_401_UNAUTHORIZED)
    return JsonResponse(data={"message": "The method is not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
@api_view(["GET", "DELETE"])
def single_session(request):
    try:
        target = Session.objects.get(passcode=request.data["passcode"])
        targetSerialized = SessionSerializer(target)
    except:
        return JsonResponse(data={"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        checkDate = (datetime.now().strftime("%Y/%m/%d %H:%M:%S")).replace(" ", "T").replace("/", "-")
        if targetSerialized.data["expire"] < checkDate:
            target.delete()
            return JsonResponse(data={"message": "Session expired"}, status=status.HTTP_204_NO_CONTENT)
        return JsonResponse(data={"data": targetSerialized.data}, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        target.delete()
        return JsonResponse(data={"message": "Session removed successfully"}, status=status.HTTP_204_NO_CONTENT)
    return JsonResponse(data={"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)