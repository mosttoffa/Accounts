from django.shortcuts import render, get_object_or_404, redirect 
from django.views.generic import View, TemplateView, CreateView, FormView
from .models import *
from django.urls import reverse_lazy
from .forms import RegistrationForm, LoginForm, PasswordForgotForm, PasswordResetForm 
from django.contrib.auth import authenticate, login, logout
# For password reset
from .utils import password_reset_token
from django.core.mail import send_mail

from django.conf import settings





# Create your views here.

# Class Based View
 
class HomeView(TemplateView):
    template_name = "home.html"



class RegistrationView(CreateView):
    template_name = "accounts/registration.html"
    form_class = RegistrationForm
    success_url = reverse_lazy('accounts:home')

    # form handle to create User
    def form_valid(self, form):  # Form_valid method is more robust then other methods
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        login(self.request, user)      # Instant Login after registration
        return super().form_valid(form)


class LogoutView(View):
    def get(self, request):      # request for logout and logout
        logout(request)
        return redirect("accounts:home")


class LoginView(FormView):
    template_name = "accounts/login.html"
    form_class = LoginForm
    success_url = reverse_lazy('accounts:home')
   
    #form_valid method is a type of post method, here used for authentic user
    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Customer.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials!"})

        return super().form_valid(form)



class ProfileView(TemplateView):
    template_name = "accounts/profile.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass 
        else:
            return redirect('/login/?next=/profile/')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        customer = self.request.user.customer 
        context['customer'] = customer 
        return context 



class PasswordForgotView(FormView):
    template_name = "accounts/forgotpassword.html"
    form_class = PasswordForgotForm
    success_url = "/forgotpassword/?m=s"

    def form_valid(self, form):
        # get email from user
        email = form.cleaned_data.get("email")
        # get current host ip/domain
        url = self.request.META['HTTP_HOST']
        # get customer and then user
        customer = Customer.objects.get(user__email=email)
        user = customer.user
        # send mail to the user with email
        text_content = 'Please Click the link below to reset your password. '
        html_content = url + "/resetpassword/" + email + \
            "/" + password_reset_token.make_token(user) + "/"
        send_mail(
            'Password Reset Link | Django Ecommerce',
            text_content + html_content,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return super().form_valid(form)


class PasswordResetView(FormView):
    template_name = "passwordreset.html"
    form_class = PasswordResetForm
    success_url = "/login/"

    def dispatch(self, request, *args, **kwargs):
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        token = self.kwargs.get("token")
        if user is not None and password_reset_token.check_token(user, token):
            pass
        else:
            return redirect(reverse("accounts:passworforgot") + "?m=e")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        password = form.cleaned_data['new_password']
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        return super().form_valid(form)



class ContactView(TemplateView):   # About View

    template_name = 'contact.html'

