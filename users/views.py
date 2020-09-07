from django.shortcuts import render, redirect
from .forms import UserSignUpForm
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages

# Create your views here.
class UserSignUp(generic.CreateView):
    template_name = 'registration/signup.html'
    model = User
    form_class = UserSignUpForm
    success_url = '/'
    failed_message = 'The signup did not go through'

    def form_valid(self, form):
        super(UserSignUp, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)

        if new_user == None:
            print('------------------------login after signup authentication fail')
            return self.render_to_response(self.get_context_data(form=form, failed_message=self.failed_message))

        else:
            login(self.request, new_user)
            return redirect(self.get_success_url())

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("password_reset_done")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"form":password_reset_form})