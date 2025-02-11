from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from taskman_backend.serializers.userSerializer import UserSerializer
from taskman_backend.models.user import User
from datetime import datetime, timedelta
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
        print(name)
        print(surname)
        print(email)
        print(password)
        print(created_at)
        serializedData = UserSerializer(data={
            "name": name,
            "surname": surname,
            "email": email,
            "password": password,
            "created_at": created_at,
            "updated_at": created_at
        })
        print(serializedData)
        if serializedData.is_valid():
            serializedData.save()
            return JsonResponse(data={"data": serializedData.data}, status=status.HTTP_201_CREATED)
        return JsonResponse(data={"message": "The body is not valid"}, status=status.HTTP_400_BAD_REQUEST)

'''        
@api_view(["GET", "PUT", "DELETE"])
def single_user(request, id):
    try:
        target = User.objects.get(pk=id)
    except target.DoesNotExist:
        return JsonResponse(data={"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    targetAdmin = UserSerializer(target)
    if checkToken(token, targetAdmin.data):
        if request.method == "GET":
            adminId = targetAdmin.data["id"]
            username = targetAdmin.data["username"]
            email = targetAdmin.data["email"]
            password = decrypt(targetAdmin.data["password"].encode(), admin_salt)
            created_at = targetAdmin.data["created_at"]
            updated_at = targetAdmin.data["updated_at"]
            auth_from = targetAdmin.data["auth_from"]
            auth_until = targetAdmin.data["auth_until"]
            serializedAdmin = AdminSerializer({
                "id": adminId,
                "username": username,
                "email": email,
                "password": password,
                "created_at": created_at,
                "updated_at": updated_at
            })
            return JsonResponse(data={"data": serializedAdmin.data}, status=status.HTTP_200_OK)
        elif request.method == "PUT":
            username = request.data["username"]
            email = request.data["email"]
            password = crypt(request.data["password"], admin_salt)
            created_at = targetAdmin.data["created_at"]
            updated_at = datetime.now().strftime("%Y/%m/%d %H:%M:%S").replace(" ", "T").replace("/", "-")
            auth_from = updated_at
            auth_until = (datetime.now() + timedelta(hours=24)).strftime("%Y/%m/%d %H:%M:%S").replace(" ", "T").replace("/", "-")
            updatedAdminSerialized = AdminSerializer(
                target,
                data={
                    "username": username,
                    "email": email,
                    "password": password.decode(),
                    "created_at": created_at,
                    "updated_at": updated_at
                }
            )
            if updatedAdminSerialized.is_valid():
                updatedAdminSerialized.save()
                new_token = (
                        "id:" + str(updatedAdminSerialized.data["id"]) +
                        ">>username:" + updatedAdminSerialized.data["username"] +
                        ">>email:" + updatedAdminSerialized.data["email"] +
                        ">>password:" + updatedAdminSerialized.data["password"] +
                        ">>created_at:" + updatedAdminSerialized.data["created_at"] +
                        ">>updated_at:" + updated_at +
                        ">>auth_from:" + updatedAdminSerialized.data["auth_from"] +
                        ">>auth_until:" + updatedAdminSerialized.data["auth_until"]
                )
                return JsonResponse(data={"token": crypt(new_token, admin_salt).decode(), "data": updatedAdminSerialized.data}, status=status.HTTP_200_OK)
            return JsonResponse(data={"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == "DELETE":
            target.delete()
            return JsonResponse(data={"message": "Admin removed successfully"}, status=status.HTTP_204_NO_CONTENT)
    return JsonResponse(data={"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
'''