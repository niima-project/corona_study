import requests
import base64

from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from django.views.generic.base import RedirectView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from users.models import User
from users.forms import UserRegisterForm
from polar_auth.settings import polar_key, polar_secret


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


@method_decorator(login_required, name='dispatch')
class AddAuthTokenView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        # The user get's redirected here with a token in the url
        user = self.request.user
        token = self.request.GET.get('code', '')

        # We ask for an access token using the received token
        # (this is where we authenticate ourselves)
        auth = f'{polar_key}:{polar_secret}'
        auth_bytes = auth.encode('ascii')
        base64_bytes = base64.b64encode(auth_bytes)
        base64_auth = base64_bytes.decode('ascii')

        headers = {
          'Authorization': f'Basic {base64_auth}'
        }
        data = f"grant_type=authorization_code&code={token}"

        token_response = requests.post('https://polarremote.com/v2/oauth2/token/',
                          data=data,
                          headers=headers
                          ).json()

        user.oauth2_token = token
        user.polar_id = token_response["x_user_id"]
        user.access_token = token_response["access_token"]
        user.save()
        print(user.polar_id)
        print(user.access_token)

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {token_response["access_token"]}'
        }
        json={"member-id": user.username}

        r = requests.post('https://www.polaraccesslink.com/v3/users', json=json, headers = headers)

        return reverse_lazy('home')


@method_decorator(login_required, name='dispatch')
class GetAuthenticationView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        url = "https://flow.polar.com/oauth2/authorization"
        url += "?response_type=code"
        url += "&scope=accesslink.read_all"
        url += f"&client_id={polar_key}"
        return url
