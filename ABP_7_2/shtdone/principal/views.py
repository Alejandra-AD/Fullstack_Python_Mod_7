
from msilib.schema import ListView
from django.shortcuts import get_object_or_404, render,redirect
from django.views.generic import DetailView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .forms import LoginForm
from .models import Task

# Create your views here.
def home(request):
    return render(request,'tasks/home_tareas.html')

class LoginUsuarioView(TemplateView):
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, { "form": form })

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
            form.add_error('username', 'Credenciales incorrectas')
            return render(request, self.template_name, { "form": form })
        else:
            return render(request, self.template_name, { "form": form })

class TaskListView(TemplateView):
    template_name = 'tasks/task_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(completed=False).order_by('due_date')
        context['home'] = reverse_lazy('task_create')
        return context

class TaskView(TemplateView):
    template_name = 'task/task_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = get_object_or_404(Task, id=self.kwargs['task_id'])
        context['task'] = task
        return context

class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit_url'] = reverse_lazy('task_edit', kwargs={'pk': self.object.pk})
        context['delete_url'] = reverse_lazy('task_delete', kwargs={'pk': self.object.pk})
        context['complete_url'] = reverse_lazy('task_complete', kwargs={'pk': self.object.pk})
        context['return_url'] = reverse_lazy('task_list')
        return context