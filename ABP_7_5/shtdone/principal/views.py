
from msilib.schema import ListView
from django.db.models import Q
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView,CreateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .forms import LoginForm, TaskFilterForm,TaskForm
from .models import Task,Etiqueta

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

class TaskListView(LoginRequiredMixin, TemplateView):
    template_name = 'tasks/task_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_form = TaskFilterForm(self.request.GET or None)
        tasks = Task.objects.filter(user=self.request.user, completed=False)

        if filter_form.is_valid():
            name = filter_form.cleaned_data.get('name')
            due_date = filter_form.cleaned_data.get('due_date')
            etiquetas = filter_form.cleaned_data.get('etiqueta')

            if name:
                tasks = tasks.filter(title__icontains=name)

            if due_date:
                tasks = tasks.filter(due_date=due_date)

            if etiquetas:
                tasks = tasks.filter(etiqueta=etiquetas)

        context['tasks'] = tasks
        context['filter_form'] = filter_form
        context['etiqueta'] = Etiqueta.objects.all()
        return context




class TaskView(TemplateView):
    template_name = 'task/task_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = get_object_or_404(Task, id=self.kwargs['task_id'])
        context['task'] = task
        return context

# class TaskDetailView(DetailView):
#     model = Task
#     template_name = 'tasks/task_detail.html'
#     context_object_name = 'task'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['edit_url'] = reverse_lazy('task_edit', kwargs={'pk': self.object.pk})
#         context['delete_url'] = reverse_lazy('task_delete', kwargs={'pk': self.object.pk})
#         context['complete_url'] = reverse_lazy('task_complete', kwargs={'pk': self.object.pk})
#         context['return_url'] = reverse_lazy('task_list')
#         return context
class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.object  # Obtener la instancia de la tarea actual
        context['task'] = task
        context['edit_url'] = reverse_lazy('task_edit', kwargs={'pk': task.pk})
        context['delete_url'] = reverse_lazy('task_delete', kwargs={'pk': task.pk})
        context['complete_url'] = reverse_lazy('task_complete', kwargs={'pk': task.pk})
        context['return_url'] = reverse_lazy('task_list')
        return context


class TaskCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'tasks/task_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TaskForm()
        # context['edit_url'] = reverse_lazy('task_edit', kwargs={'pk': self.object.pk})
        return context

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
        else:
            return render(request, self.template_name, {'form': form})

class TaskEditView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    pk_url_kwarg = 'pk'

    def get_success_url(self):
        return reverse_lazy('task_detail', kwargs={'pk': self.object.pk})
