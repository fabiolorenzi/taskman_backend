from django.http import JsonResponse
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework import status
from taskman_backend.serializers.projectSerializer import ProjectSerializer
from taskman_backend.serializers.sessionSerializer import SessionSerializer
from taskman_backend.models.project import Project
from taskman_backend.models.session import Session
from datetime import datetime

@api_view(["GET", "POST"])
def all_projects(request, id):
    try:
        targetSession = Session.objects.get(user=id)
        serializedSession = SessionSerializer(targetSession)
    except:
        return JsonResponse(data={"message": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
    
    currentPasscode = request.data["passcode"]
    if serializedSession.data["passcode"] == currentPasscode:
        if request.method == "GET":
            main_user = request.GET.get("main_user", "")
            user = request.GET.get("user", "")
            if serializedSession.data["user"] != main_user and serializedSession.data["user"] != user:
                return JsonResponse(data={"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

            all_projects = Project.models.filter(Q(main_user=main_user)).order_by("name")
            serializedProject = ProjectSerializer(all_projects, many = True)
            return JsonResponse(data={"data": serializedProject.data}, status=status.HTTP_200_OK)
        elif request.method == "POST":
            name = request.data["name"]
            description = request.data["description"]
            main_user = serializedSession.data["user"]
            created_at = datetime.now()
            serializedData = ProjectSerializer(data={
                "name": name,
                "description": description,
                "main_user": main_user,
                "created_at": created_at,
                "updated_at": created_at
            })
            if serializedData.is_valid():
                serializedData.save()
                return JsonResponse(data={"data": serializedData.data}, status=status.HTTP_201_CREATED)
            return JsonResponse(data={"message": "The body is not valid"}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(data={"message": "The method is not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    return JsonResponse(data={"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)



    # REVIEW THE GET ALL TO ALLOW TO CHECK THE TEAMS AND SEE IF THE USER
    # SHOULD BE ABLE TO SEE THAT PROJECT

@api_view(["GET", "PUT", "DELETE"])
def single_project(request, userid, id):
    try:
        target = Project.objects.get(pk=id)
        targetProject = ProjectSerializer(target)
    except target.DoesNotExist:
        return JsonResponse(data={"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        targetSession = Session.objects.get(user=userid)
        serializedSession = SessionSerializer(targetSession)
    except:
        return JsonResponse(data={"message": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
    
    currentPasscode = request.data["passcode"]
    if serializedSession.data["passcode"] == currentPasscode:
        if request.method == "GET":
            if serializedSession.data["user"] == targetProject.data["main_user"]:
                projectId = targetProject.data["id"]
                name = targetProject.data["name"]
                description = targetProject.data["description"]
                main_user = targetProject.data["main_user"]
                created_at = targetProject.data["created_at"]
                updated_at = targetProject.data["updated_at"]
                serializedProject = ProjectSerializer({
                    "id": projectId,
                    "name": name,
                    "description": description,
                    "main_user": main_user,
                    "created_at": created_at,
                    "updated_at": updated_at
                })
                return JsonResponse(data={"data": serializedProject.data}, status=status.HTTP_200_OK)
        elif request.method == "PUT":
            if serializedSession.data["user"] == targetProject.data["main_user"]:
                name = request.data["name"]
                description = request.data["description"]
                main_user = request.data["main_user"]
                created_at = targetProject.data["created_at"]
                updated_at = datetime.now()
                updatedProjectSerialized = ProjectSerializer(
                    target,
                    data={
                        "name": name,
                        "description": description,
                        "main_user": main_user,
                        "created_at": created_at,
                        "updated_at": updated_at
                    }
                )
                if updatedProjectSerialized.is_valid():
                    updatedProjectSerialized.save()
                    return JsonResponse(data={"data": updatedProjectSerialized.data}, status=status.HTTP_200_OK)
                return JsonResponse(data={"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == "DELETE":
            if serializedSession.data["user"] == targetProject.data["main_user"]:
                target.delete()
                return JsonResponse(data={"message": "Project removed successfully"}, status=status.HTTP_204_NO_CONTENT)
    return JsonResponse(data={"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)