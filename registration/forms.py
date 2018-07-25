from registration.models import Registration, TicketInfo
from django.forms.models import ModelForm


class TicketInfoForm(ModelForm):
	class Meta:
		model = TicketInfo
		fields = ['quantity']


class RegistrationForm(ModelForm):
	class Meta:
		model = Registration
		fields = ['clan', 'contact_name', 'email', 'telephone', 'comment']


class FinalizeRegistrationForm(ModelForm):
	class Meta:
		model = Registration
		fields = ['rules_accepted', 'paid', 'comment']
