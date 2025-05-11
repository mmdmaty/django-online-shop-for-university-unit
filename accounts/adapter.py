from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.contrib.auth import get_user_model, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages  # اینو اضافه کن

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get('email', '').lower()
        if email:
            try:
                user = User.objects.get(email=email)
                sociallogin.connect(request, user)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                # اینجا پیام خوش‌آمدگویی رو دستی میفرستیم
                messages.success(request, f" {user.email} با موفقیت وارد شدی.")
                raise ImmediateHttpResponse(HttpResponseRedirect(reverse('home')))
            except User.DoesNotExist:
                pass
