from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from taskman_backend.serializers.iterationSerializer import IterationSerializer
from taskman_backend.serializers.sessionSerializer import SessionSerializer
from taskman_backend.models.iteration import Iteration
from taskman_backend.models.session import Session
from datetime import datetime

@api_view(["PATCH", "POST"])
def all_iterations(request, id):
    try:
        targetSession = Session.objects.get(user=id)
        serializedSession = SessionSerializer(targetSession)
    except:
        return JsonResponse(data={"message": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "PATCH":
        project = request.GET.get("project", "")

        all_iterations = Iteration.objects.filter(project=project).order_by("version")
        serializedIterations = IterationSerializer(all_iterations, many = True)
        return JsonResponse(data={"data": serializedIterations.data}, status=status.HTTP_200_OK)
    elif request.method == "POST":
        project = request.data["project"]
        version = request.data["version"]
        title = request.data["title"]
        description = request.data["description"]
        start_date = request.data["start_date"]
        end_date = request.data["end_date"]
        created_at = datetime.now()
        updated_by = serializedSession.data["user"]
        serializedData = IterationSerializer(data={
            "project": project,
            "version": version,
            "title": title,
            "description": description,
            "start_date": start_date,
            "end_date": end_date,
            "created_at": created_at,
            "updated_at": created_at,
            "updated_by": updated_by
        })
        if serializedData.is_valid():
            serializedData.save()
            return JsonResponse(data={"data": serializedData.data}, status=status.HTTP_201_CREATED)
        return JsonResponse(data={"message": "The body is not valid"}, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse(data={"message": "The method is not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(["PATCH", "PUT", "DELETE"])
def single_iteration(request, userid, id):
    try:
        target = Iteration.objects.get(pk=id)
        targetIteration = IterationSerializer(target)
    except target.DoesNotExist:
        return JsonResponse(data={"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        targetSession = Session.objects.get(user=userid)
        serializedSession = SessionSerializer(targetSession)
    except:
        return JsonResponse(data={"message": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
    
    currentPasscode = request.data["passcode"]
    if serializedSession.data["passcode"] == currentPasscode:
        if request.method == "PATCH":
            iterationId = targetIteration.data["id"]
            project = targetIteration.data["project"]
            version = targetIteration.data["version"]
            title = targetIteration.data["title"]
            description = targetIteration.data["description"]
            start_date = targetIteration.data["start_date"]
            end_date = targetIteration.data["end_date"]
            created_at = targetIteration.data["created_at"]
            updated_at = targetIteration.data["updated_at"]
            updated_by = targetIteration.data["updated_by"]
            serializedIteration = IterationSerializer({
                "id": iterationId,
                "project": project,
                "version": version,
                "title": title,
                "description": description,
                "start_date": start_date,
                "end_date": end_date,
                "created_at": created_at,
                "updated_at": updated_at,
                "updated_by": updated_by
            })
            return JsonResponse(data={"data": serializedIteration.data}, status=status.HTTP_200_OK)
        elif request.method == "PUT":
            project = request.data["project"]
            version = request.data["version"]
            title = request.data["title"]
            description = request.data["description"]
            start_date = request.data["start_date"]
            end_date = request.data["end_date"]
            created_at = targetIteration.data["created_at"]
            updated_at = datetime.now()
            updated_by = targetSession.data["user"]
            updatedIterationSerialized = IterationSerializer(
                target,
                data={
                    "project": project,
                    "version": version,
                    "title": title,
                    "description": description,
                    "start_date": start_date,
                    "end_date": end_date,
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "updated_by": updated_by
                }
            )
            if updatedIterationSerialized.is_valid():
                updatedIterationSerialized.save()
                return JsonResponse(data={"data": updatedIterationSerialized.data}, status=status.HTTP_200_OK)
            return JsonResponse(data={"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == "DELETE":
            target.delete()
            return JsonResponse(data={"message": "Iteration removed successfully"}, status=status.HTTP_204_NO_CONTENT)
    return JsonResponse(data={"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
