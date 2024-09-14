from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import UserCreationForm, EditUserForm

User = get_user_model()


class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/registration_form.html"
    success_url = reverse_lazy("authorization:login")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("blog:index")


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditUserForm
    template_name = "blog/user.html"

    def get_object(self):
        return self.request.user
