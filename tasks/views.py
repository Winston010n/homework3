from rest_framework import generics, mixins

from .models import Task
from .serializers import TaskSerializer


class TaskListCreateView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    """Представление для получения списка задач и создания новой задачи."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        # list() сериализует queryset с many=True и возвращает список (200).
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # create() проверяет данные и сохраняет задачу (201 или ошибки 400).
        return self.create(request, *args, **kwargs)


class TaskDetailView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """Представление для чтения, изменения и удаления одной задачи по pk."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        # retrieve() возвращает данные задачи (200); если ее нет, DRF ответит 404.
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        # update() проверяет и полностью заменяет данные задачи (200 или 400).
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        # partial_update() проверяет и сохраняет только переданные поля (200 или 400).
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # destroy() удаляет задачу и отвечает без тела (204); если ее нет — 404.
        return self.destroy(request, *args, **kwargs)


# DRF формирует 400 для ошибок сериализатора и 404 для отсутствующего pk.
# 3xx здесь не нужен: эти операции не перенаправляют клиента. Неожиданные ошибки
# остаются 500 и обрабатываются общим обработчиком Django/DRF, а не маскируются здесь.