from django import forms


class NewsletterForm(forms.Form):
    contact_email = forms.EmailField(required=True, label="",
    widget=forms.TextInput(attrs={'autocapitalize': "off", 'autocorrect': "off", 'name': "MERGE0",
                                  'class': "required email form-control", 'id': "mce-EMAIL",
                                  'placeholder': "Email-Adresse eingeben", 'value': ""}))


class ContactForm(forms.Form):
    name = forms.CharField(required=True, label="", widget=forms.TextInput(attrs={'id': 'name', 'class': "form-control col-md-4",
                                                                                  'placeholder': "Name"}))
    email = forms.EmailField(required=True, label="", widget=forms.TextInput(attrs={'id': 'email',
                                                                                    'class': "form-control col-md-4",
                                                                                    'placeholder': "Ihre Email-Adresse"}))
    message = forms.CharField(required=True, label="", widget=forms.Textarea(attrs={'id': 'message', 'class': 'form-control',
                                                                                    'placeholder': "Ihre Nachricht an uns",
                                                                                    'style': 'resize:none', 'rows': '25',
                                                                                    'cols': '10'}))


class LoginForm(forms.Form):
    username = forms.CharField(required=True, label="", widget=forms.TextInput(attrs={'placeholder': "Nutzername"}))
    password = forms.CharField(widget=forms.PasswordInput(render_value=False, attrs={'placeholder': "Passwort"}))
