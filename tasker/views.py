from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from tasker.forms import TaskForm
from tasker.models import Tag, Task


class TagListView(generic.ListView):
    model = Tag


class TagCreateView(generic.CreateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("tasker:tag-list")


class TagUpdateView(generic.UpdateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("tasker:tag-list")


class TagDeleteView(generic.DeleteView):
    model = Tag
    success_url = reverse_lazy("tasker:tag-list")


class TaskListView(generic.ListView):
    model = Task

    def get_queryset(self):
        my_queryset = Task.objects.order_by("done", "-time_creation")
        return my_queryset


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasker:task-list")


class TaskUpdateView(generic.UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("tasker:task-list")


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy("tasker:task-list")


class ToggleToDoneView(generic.View):
    @staticmethod
    def get(request: HttpRequest, pk: int) -> HttpResponse:
        task = get_object_or_404(Task, pk=pk)
        task.done = not task.done
        task.save()
        return HttpResponseRedirect(reverse_lazy("tasker:task-list"))
