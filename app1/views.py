from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from .models import TaskToPerform
from django.contrib.auth.mixins import LoginRequiredMixin


class Login_View(LoginView):
    template_name = 'app1/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'app1/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, *kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = TaskToPerform
    context_object_name = 'tasks'
    template_name = 'app1/task_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search_area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)
        context['search_input'] = search_input
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = TaskToPerform
    context_object_name = 'tasks'
    template_name = 'app1/task_detail.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = TaskToPerform
    fields = ['title', 'desc', 'complete']
    template_name = 'app1/task_form.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = TaskToPerform
    fields = ['title', 'desc', 'complete']
    template_name = 'app1/task_form.html'
    success_url = reverse_lazy('tasks')


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = TaskToPerform
    context_object_name = 'task'
    template_name = 'app1/task_to_perform_confirm_delete.html'
    success_url = reverse_lazy('tasks')
