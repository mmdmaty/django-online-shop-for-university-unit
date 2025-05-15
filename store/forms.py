from django.forms import Form,ModelForm
from django import forms
from . import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField
from django import forms
from .models import ProductVariant

class AddCartForm(forms.Form):
    variant_id = forms.IntegerField()
    quantity = forms.IntegerField(max_value=30, min_value=1)
    inplace = forms.BooleanField(widget=forms.HiddenInput(), required=False)

    def clean_variant_id(self):
        variant_id = self.cleaned_data['variant_id']
        if not ProductVariant.objects.filter(id=variant_id).exists():
            raise forms.ValidationError("واریانت محصول نامعتبر است.")
        return variant_id




    


# class OrderForm(Form):
#     first_name = forms.CharField( max_length=150)
#     last_name = forms.CharField( max_length=150, )
#     phone_number = PhoneNumberField(region='IR',)
#     note = forms.CharField(widget=forms.Textarea())

class OrderForm(ModelForm):
    shipping_address = forms.ModelChoiceField(
        queryset=models.Address.objects.none(),
        label="آدرس‌های من",
        widget=forms.RadioSelect()  # تغییر به RadioSelect
    )

    class Meta:
        model = models.Order
        fields = ['first_name', 'last_name', 'shipping_address']

    def __init__(self, *args, **kwargs):
        customer = kwargs.pop('customer', None)
        super().__init__(*args, **kwargs)

        if customer:
            self.fields['shipping_address'].queryset = models.Address.objects.filter(customer=customer)



class AddressFrom(ModelForm):
    class Meta:
        model = models.Address
        fields = ['address','postal_code','city']


class Comments(ModelForm):
    class Meta:
        model = models.Comment
        fields = ['body','rating',]


class PaymentForm(Form):
    paied = forms.BooleanField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paied'].initial = True