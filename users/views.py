from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from users.models import User
from users.forms import UserRegisterForm


@method_decorator(login_required, name='dispatch')
class UserDetailView(DetailView):
    model = User
    template_name = "users/detailview.html"

    def get_object(self):
        return self.request.user


class RegistrationView(SuccessMessageMixin, CreateView):
    template_name = 'users/registration.html'
    success_url = reverse_lazy('login')
    form_class = UserRegisterForm
    success_message = "Your profile was created successfully"
