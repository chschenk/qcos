from django.forms import Form, ModelForm, ModelMultipleChoiceField
from django.forms import modelformset_factory, inlineformset_factory
from django.forms.fields import CharField, EmailField, MultipleChoiceField, BooleanField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django_select2.forms import Select2MultipleWidget
from qcos.base.models import TicketInfo, Registration
from django.utils.translation import gettext as _

class SignUpForm(UserCreationForm):
	first_name = CharField(max_length=30, required=False, help_text='Optional.')
	last_name = CharField(max_length=30, required=False, help_text='Optional.')
	email = EmailField(max_length=254, help_text='Required. Inform a valid email address.')

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email',)


class OrganizerForm(ModelForm):
	members = ModelMultipleChoiceField(queryset=User.objects.all(), widget=Select2MultipleWidget, required=False)

	class Meta:
		model = Group
		fields = ('name',)

	def __init__(self, *args, **kwargs):
		self.group = kwargs['instance']
		initial = kwargs.pop('initial', dict())
		if self.group is not None:
			initial['members'] = [x for x in User.objects.filter(groups=self.group)]
		kwargs['initial'] = initial
		super(OrganizerForm, self).__init__(*args, **kwargs)

	def save(self, commit=True):
		group = super(OrganizerForm, self).save(commit=commit)
		for user in group.user_set.all():
			group.user_set.remove(user)
		for user in self.cleaned_data['members']:
			group.user_set.add(user)
		group.save()
		return group


class TicketInfoForm(ModelForm):
	class Meta:
		model = TicketInfo
		fields = ('quantity',)


class RegistrationForm(ModelForm):
	class Meta:
		model = Registration
		fields = ('clan', 'contact_name', 'email', 'telephone', 'comment')
		# ToDo: add chained select2

#class TicketInfoFormSet(BaseFormSet):
#TicketInfoFormSet = inlineformset_factory()


class CheckInFormStep1(ModelForm):
	class Meta:
		model = Registration
		fields = ('paid', 'present_participants', 'comment')


class CheckInFormStep2(ModelForm):
	class Meta:
		model = Registration
		fields = ('rules_accepted', 'picture_rights', 'staff_confirmed')
	#signature = BooleanField(required=True, label="Lagerregeln anerkannt",
	#						 help_text="Lagerreglen anerkannt und unterschrieben")
	#dsgvo = BooleanField(required=True, label="Formular für die Bildrechte abgegeben",
	#					 help_text="Formular für die Bildrechte abgegeben und dementsprechend Bändchen herausgegeben")
	#staff_confirmation = BooleanField(required=True, label="Formular für Bestätigung über den Einsatzes geeigneten Personals",
	#					 help_text="Formular für die Bestätigung über den Einsatzes geeigneten Personals")
	trash_bags = BooleanField(required=True, label="Mülltüten ausgegeben",
						 help_text="Mülltüten ausgegeben 1 x Gelber Sack und 1 x Blauer Sack")


class WorkshopAnnotateForm(Form):
	annotate = BooleanField(required=True, label=_("Annotate all workshop with status ok"))


class WorkshopPrintForm(Form):
	generate_batch = BooleanField(required=True, label=_("Generate a print batch for all unprinted workshops"))