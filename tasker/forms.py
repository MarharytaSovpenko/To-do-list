from django import forms

from tasker.models import Tag, Task


class TaskForm(forms.ModelForm):
    task_tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Task
        fields = "__all__"
