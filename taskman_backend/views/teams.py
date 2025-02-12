from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from taskman_backend.serializers.teamSerializer import TeamSerializer
from taskman_backend.serializers.sessionSerializer import SessionSerializer
from taskman_backend.models.team import Team
from taskman_backend.models.session import Session
from datetime import datetime

@api_view(["GET", "POST"])
def all_teams(request):
    try:
        targetSession = Session.objects.get(user=id)
        serializedSession = SessionSerializer(targetSession)
    except:
        return JsonResponse(data={"message": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        project = request.GET.get("project", "")

        all_team = Team.models.filter(project=project).order_by("user")
        serializedTeam = TeamSerializer(all_team, many = True)
        return JsonResponse(data={"data": serializedTeam.data}, status=status.HTTP_200_OK)
    elif request.method == "POST":
        user = request.data["user"]
        role = request.data["role"]
        project = request.data["project"]
        created_at = datetime.now()
        serializedData = TeamSerializer(data={
            "user": user,
            "role": role,
            "project": project,
            "created_at": created_at,
            "updated_at": created_at
        })
        if serializedData.is_valid():
            serializedData.save()
            return JsonResponse(data={"data": serializedData.data}, status=status.HTTP_201_CREATED)
        return JsonResponse(data={"message": "The body is not valid"}, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse(data={"message": "The method is not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(["GET", "PUT", "DELETE"])
def single_team(request, id):
    try:
        target = Team.objects.get(pk=id)
        targetTeam = TeamSerializer(target)
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
            teamId = targetTeam.data["id"]
            user = targetTeam.data["user"]
            role = targetTeam.data["role"]
            project = targetTeam.data["project"]
            created_at = targetTeam.data["created_at"]
            updated_at = targetTeam.data["updated_at"]
            serializedTeam = TeamSerializer({
                "id": teamId,
                "user": user,
                "role": role,
                "project": project,
                "created_at": created_at,
                "updated_at": updated_at
            })
            return JsonResponse(data={"data": serializedTeam.data}, status=status.HTTP_200_OK)
        elif request.method == "PUT":
            user = request.data["user"]
            role = request.data["role"]
            project = request.data["project"]
            created_at = targetTeam.data["created_at"]
            updated_at = datetime.now()
            updatedTeamSerialized = TeamSerializer(
                target,
                data={
                    "user": user,
                    "role": role,
                    "project": project,
                    "created_at": created_at,
                    "updated_at": updated_at
                }
            )
            if updatedTeamSerialized.is_valid():
                updatedTeamSerialized.save()
                return JsonResponse(data={"data": updatedTeamSerialized.data}, status=status.HTTP_200_OK)
            return JsonResponse(data={"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == "DELETE":
            target.delete()
            return JsonResponse(data={"message": "Team user removed successfully"}, status=status.HTTP_204_NO_CONTENT)
    return JsonResponse(data={"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)