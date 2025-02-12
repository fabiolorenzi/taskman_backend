from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from taskman_backend.serializers.userSerializer import UserSerializer
from taskman_backend.serializers.sessionSerializer import SessionSerializer
from taskman_backend.models.user import User
from taskman_backend.models.session import Session
from datetime import datetime
from settings_data import environment

@api_view(["GET", "POST"])
def all_users(request):
    if request.method == "GET":
        if environment == "Development":
            all_users = User.objects.all().order_by("id")
            serializedData = UserSerializer(all_users, many = True)
            return JsonResponse(data={"data": serializedData.data}, status=status.HTTP_200_OK)
        return JsonResponse(data={"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    elif request.method == "POST":
        name = request.data["name"]
        surname = request.data["surname"]
        email = request.data["email"]
        password = request.data["password"]
        created_at = datetime.now()
        serializedData = UserSerializer(data={
            "name": name,
            "surname": surname,
            "email": email,
            "password": password,
            "created_at": created_at,
            "updated_at": created_at
        })
        if serializedData.is_valid():
            serializedData.save()
            return JsonResponse(data={"data": serializedData.data}, status=status.HTTP_201_CREATED)
        return JsonResponse(data={"message": "The body is not valid"}, status=status.HTTP_400_BAD_REQUEST)
       
@api_view(["GET", "PUT", "DELETE"])
def single_user(request, id):
    try:
        target = User.objects.get(pk=id)
        targetUser = UserSerializer(target)
    except target.DoesNotExist:
        return JsonResponse(data={"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        targetSession = Session.objects.get(user=id)
        serializedSession = SessionSerializer(targetSession)
    except:
        return JsonResponse(data={"message": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
    
    currentPasscode = request.data["passcode"]
    if serializedSession.data["passcode"] == currentPasscode:
        if request.method == "GET":
            userId = targetUser.data["id"]
            name = targetUser.data["name"]
            surname = targetUser.data["surname"]
            email = targetUser.data["email"]
            password = targetUser.data["password"]
            created_at = targetUser.data["created_at"]
            updated_at = targetUser.data["updated_at"]

            serializedUser = UserSerializer({
                "id": userId,
                "name": name,
                "surname": surname,
                "email": email,
                "password": password,
                "created_at": created_at,
                "updated_at": updated_at
            })
            return JsonResponse(data={"data": serializedUser.data}, status=status.HTTP_200_OK)
        elif request.method == "PUT":
            name = request.data["name"]
            surname = request.data["surname"]
            email = request.data["email"]
            password = request.data["password"]
            created_at = targetUser.data["created_at"]
            updated_at = datetime.now().strftime("%Y/%m/%d %H:%M:%S").replace(" ", "T").replace("/", "-")
            updatedUserSerialized = UserSerializer(
                target,
                data={
                    "name": name,
                    "surname": surname,
                    "email": email,
                    "password": password,
                    "created_at": created_at,
                    "updated_at": updated_at
                }
            )
            if updatedUserSerialized.is_valid():
                updatedUserSerialized.save()
                return JsonResponse(data={"data": updatedUserSerialized.data}, status=status.HTTP_200_OK)
            return JsonResponse(data={"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == "DELETE":
            target.delete()
            targetSession.delete()
            return JsonResponse(data={"message": "User removed successfully"}, status=status.HTTP_204_NO_CONTENT)
    return JsonResponse(data={"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)