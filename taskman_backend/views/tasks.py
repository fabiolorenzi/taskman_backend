from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from taskman_backend.serializers.taskSerializer import TaskSerializer
from taskman_backend.serializers.sessionSerializer import SessionSerializer
from taskman_backend.models.task import Task
from taskman_backend.models.session import Session
from datetime import datetime

@api_view(["GET", "POST"])
def all_tasks(request, id):
    try:
        targetSession = Session.objects.get(user=id)
        serializedSession = SessionSerializer(targetSession)
    except:
        return JsonResponse(data={"message": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        project = request.GET.get("project", "")
        iteration = request.GET.get("iteration", "")

        all_tasks = Task.models.filter(project=project).filter(iteration=iteration).order_by("version")
        serializedTasks = TaskSerializer(all_tasks, many = True)
        return JsonResponse(data={"data": serializedTasks.data}, status=status.HTTP_200_OK)
    elif request.method == "POST":
        number = request.data["number"]
        title = request.data["title"]
        description = request.data["description"]
        type = request.data["type"]
        priority = request.data["priority"]
        status = request.data["status"]
        project = request.data["project"]
        user = request.data["user"]
        iteration = request.data["iteration"]
        created_at = datetime.now()
        updated_by = serializedSession.data["user"]
        serializedData = TaskSerializer(data={
            "number": number,
            "title": title,
            "description": description,
            "type": type,
            "priority": priority,
            "status": status,
            "project": project,
            "user": user,
            "iteration": iteration,
            "created_at": created_at,
            "updated_at": created_at,
            "updated_by": updated_by
        })
        if serializedData.is_valid():
            serializedData.save()
            return JsonResponse(data={"data": serializedData.data}, status=status.HTTP_201_CREATED)
        return JsonResponse(data={"message": "The body is not valid"}, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse(data={"message": "The method is not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(["GET", "PUT", "DELETE"])
def single_task(request, userid, id):
    try:
        target = Task.objects.get(pk=userid)
        targetTask = TaskSerializer(target)
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
            taskId = targetTask.data["id"]
            number = targetTask.data["number"]
            title = targetTask.data["title"]
            description = targetTask.data["description"]
            type = targetTask.data["type"]
            priority = targetTask.data["priority"]
            status = targetTask.data["status"]
            project = targetTask.data["project"]
            user = targetTask.data["user"]
            iteration = targetTask.data["iteration"]
            created_at = targetTask.data["created_at"]
            updated_at = targetTask.data["updated_at"]
            updated_by = targetTask.data["updated_by"]
            serializedTask= TaskSerializer({
                "id": taskId,
                "number": number,
                "title": title,
                "description": description,
                "type": type,
                "priority": priority,
                "status": status,
                "project": project,
                "user": user,
                "iteration": iteration,
                "created_at": created_at,
                "updated_at": updated_at,
                "updated_by": updated_by
            })
            return JsonResponse(data={"data": serializedTask.data}, status=status.HTTP_200_OK)
        elif request.method == "PUT":
            number = request.data["number"]
            title = request.data["title"]
            description = request.data["description"]
            type = request.data["type"]
            priority = request.data["priority"]
            status = request.data["status"]
            project = request.data["project"]
            user = request.data["user"]
            iteration = request.data["iteration"]
            created_at = targetTask.data["created_at"]
            updated_at = datetime.now()
            updated_by = targetSession.data["user"]
            updatedTaskSerialized = TaskSerializer(
                target,
                data={
                    "number": number,
                    "title": title,
                    "description": description,
                    "type": type,
                    "priority": priority,
                    "status": status,
                    "project": project,
                    "user": user,
                    "iteration": iteration,
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "updated_by": updated_by
                }
            )
            if updatedTaskSerialized.is_valid():
                updatedTaskSerialized.save()
                return JsonResponse(data={"data": updatedTaskSerialized.data}, status=status.HTTP_200_OK)
            return JsonResponse(data={"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == "DELETE":
            target.delete()
            return JsonResponse(data={"message": "Task removed successfully"}, status=status.HTTP_204_NO_CONTENT)
    return JsonResponse(data={"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)