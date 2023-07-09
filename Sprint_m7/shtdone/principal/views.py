
from collections import UserDict
from msilib.schema import ListView
from django.db.models import Q
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import DetailView,CreateView,TemplateView,DeleteView,View
from django.views.generic.edit import UpdateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from .forms import LoginForm, TaskFilterForm,TaskForm
from .models import Task,Etiqueta,Observation,TaskStatus,Priority

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
        # tasks = Task.objects.filter(user=self.request.user, completed=False)
        tasks = Task.objects.filter(user=self.request.user)
        if filter_form.is_valid():
            name = filter_form.cleaned_data.get('name')
            due_date = filter_form.cleaned_data.get('due_date')
            etiquetas = filter_form.cleaned_data.get('etiqueta')
            priority = filter_form.cleaned_data.get('priority')

            if name:
                tasks = tasks.filter(title__icontains=name)

            if due_date:
                tasks = tasks.filter(due_date=due_date)

            if etiquetas:
                tasks = tasks.filter(etiqueta=etiquetas)

            if priority:
                tasks = tasks.filter(priority=priority)

        context['tasks'] = tasks
        context['filter_form'] = filter_form
        context['etiqueta'] = Etiqueta.objects.all()
        context['priority'] = Priority.objects.all()

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

    def post(self, request, *args, **kwargs):
        task = self.get_object()  #  instancia la tarea
        task.completed = True  # Marca la tarea como completada
        task.status = TaskStatus.objects.get(name='Completada')  # Establece el estado de la tarea como 'Completada'
        task.save()  # Guarda los cambios en la base de datos
        messages.success(request, 'La tarea ha sido marcada como completada.')  # Agrega un mensaje de éxito
        return redirect('task_list')  # Redirige a la vista de listado de tareas

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.object  # Obtener la instancia de la tarea actual
        context['task'] = task
        context['edit_url'] = reverse_lazy('task_edit', kwargs={'pk': task.pk})
        context['delete_url'] = reverse_lazy('task_delete', kwargs={'pk': task.pk})
        context['complete_url'] = reverse_lazy('task_complete', kwargs={'pk': task.pk})
        context['status'] = TaskStatus.objects.get(name='Completada')
        context['priority'] = task.priority  # Agregar la prioridad al contexto
        context['return_url'] = reverse_lazy('task_list')
        context['observations'] = Observation.objects.filter(task=task)
        return context



class TaskCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'tasks/task_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TaskForm()
        context['users'] = User.objects.all()  # Obtener la lista de usuarios
        return context

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = form.cleaned_data['user']  # Asignar el usuario seleccionado
            task.save()
            return redirect('task_list')
        else:
            return render(request, self.template_name, {'form': form})

# class TaskEditView(UpdateView):
#     model = Task
#     form_class = TaskForm
#     template_name = 'tasks/task_form.html'
#     pk_url_kwarg = 'pk'

#     def get_success_url(self):
#         return reverse_lazy('task_detail', kwargs={'pk': self.object.pk})
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['priorities'] = Priority.objects.all()  # Obtener la lista de prioridades
#         context['users'] = User.objects.all()
#         return context

class TaskEditView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    pk_url_kwarg = 'pk'

    def get_success_url(self):
        return reverse_lazy('task_detail', kwargs={'pk': self.object.pk})
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        task = self.get_object()
        kwargs['initial'] = {
            'title': task.title,
            'description': task.description,
            'due_date': task.due_date,
            'etiqueta': task.etiqueta,
            'priority': task.priority,
            'user': task.user,
        }
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['priorities'] = Priority.objects.all()  # Obtener la lista de prioridades
        context['users'] = User.objects.all()
        return context



class ObservationCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'tasks/observation_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_id = self.kwargs['task_id']
        context['task_id'] = task_id
        # Obtener las observaciones existentes para la tarea actual
        observations = Observation.objects.filter(task_id=task_id)
        context['observations'] = observations
        return context

    def post(self, request, *args, **kwargs):
        task_id = self.kwargs['task_id']
        observations = request.POST.get('observations')
        user = request.user
        # Guardar la nueva observación en la base de datos
        Observation.objects.create(task_id=task_id, observations=observations, user=user)
        return redirect('task_detail', pk=task_id)
    
class ObservationUpdateView(LoginRequiredMixin, UpdateView):
    model = Observation
    fields = ['observations']


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list') 

class TaskCompleteView(View):
    def get(self, request, pk):
        task = Task.objects.get(pk=pk)
        task.completed = True
        task.save()
        return redirect('task_list')