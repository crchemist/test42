from django import forms

class ContactForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    jabber = forms.EmailField()
    skype = forms.CharField(max_length=250)
    other_contacts = forms.CharField()

    date_of_birth = forms.DateField()
    bio = forms.CharField()

    photo = forms.ImageField(required=False)
