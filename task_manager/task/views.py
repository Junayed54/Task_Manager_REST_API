from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer
from django.shortcuts import get_object_or_404

class TaskListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            images_data = request.FILES.getlist('images')
            task = serializer.save(user=request.user, images=images_data)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Task, pk=pk, user=self.request.user)

    def get(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        return self.update_task(request, pk)

    def patch(self, request, pk):
        return self.update_task(request, pk, partial=True)

    def update_task(self, request, pk, partial=False):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()

            # Handle multiple images
            images_data = request.FILES.getlist('images')
            for image_data in images_data:
                TaskImage.objects.create(task=task, image=image_data)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = self.get_object(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# class TaskDetailView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get_object(self, pk):
#         return get_object_or_404(Task, pk=pk, user=self.request.user)

#     def get(self, request, pk):
#         task = self.get_object(pk)
#         serializer = TaskSerializer(task)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         task = self.get_object(pk)
#         serializer = TaskSerializer(task, data=request.data)
#         if serializer.is_valid():
#             serializer.save()

#             # Handle multiple images
#             images_data = request.FILES.getlist('images')
#             for image_data in images_data:
#                 TaskImage.objects.create(task=task, image=image_data)

#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         task = self.get_object(pk)
#         task.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
