from django import forms


class ContactForm(forms.Form):
    contact_name = forms.CharField(required=False, label="Name")
    contact_email = forms.EmailField(required=True, label="Email")

