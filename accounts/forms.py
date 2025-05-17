from django import forms
from django.forms import ModelForm,Form
from django.contrib.auth import get_user_model

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_instance = self.instance  
        self.fields['email'].disabled = True

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        entered_email = self.cleaned_data.get('email')
        original_email = self.user_instance.email

        if entered_email != original_email:
            raise forms.ValidationError("شما اجازه تغییر ایمیل را ندارید.")
        
        return entered_email


from allauth.account.forms import SignupForm
from phonenumber_field.formfields import PhoneNumberField

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=30,
        label='نام*',
        required=True,
        help_text='نام خود را وارد کنید.'
    )

    last_name = forms.CharField(
        max_length=30,
        label='نام خانوادگی',
        required=True,
        help_text='نام خانوادگی خود را وارد کنید.'
    )
    email = forms.EmailField(label='ایمیل*')
    phone_number = PhoneNumberField(region="IR", label='شماره موبایل', required=True)

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.save()
        return user
    
