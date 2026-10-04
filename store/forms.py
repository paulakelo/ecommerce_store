import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from .shipping import COUNTY_SHIPPING_RATES


class StoreAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Username"), widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label=_("Password"), widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class AccountDetailsForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email")
        labels = {
            "first_name": _("First name"),
            "last_name": _("Last name"),
            "email": _("Email address"),
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }


class CheckoutForm(forms.Form):
    first_name = forms.CharField(
        max_length=50, label=_("First name"), widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        max_length=50, label=_("Last name"), widget=forms.TextInput(attrs={"class": "form-control"})
    )
    phone_number = forms.CharField(
        max_length=25,
        label=_("M-Pesa phone number"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "712345678",
                "inputmode": "tel",
                "autocomplete": "tel-national",
            }
        ),
    )
    county = forms.ChoiceField(
        label=_("County"),
        choices=[("", _("Select your county"))]
        + [(county, _(f"{county} County")) for county in COUNTY_SHIPPING_RATES],
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    delivery_details = forms.CharField(
        max_length=200,
        label=_("Town, estate, street and nearest landmark"),
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    def clean_phone_number(self):
        phone = re.sub(r"[\s()-]", "", self.cleaned_data["phone_number"])
        if phone.startswith("+"):
            phone = phone[1:]
        if phone.startswith("0"):
            phone = "254" + phone[1:]
        elif re.fullmatch(r"[17]\d{8}", phone):
            phone = "254" + phone
        if not re.fullmatch(r"254[17]\d{8}", phone):
            raise forms.ValidationError(
                _("Enter a Kenyan M-Pesa number, such as 0712345678 or 254712345678.")
            )
        return phone
