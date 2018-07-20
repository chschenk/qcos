from django.forms import widgets
from django.forms import ModelForm, inlineformset_factory
from .models import Camp, Fee

class CampForm(ModelForm):
	class Meta:
		model = Camp
		fields = ['name', 'description', 'startdate', 'enddate']
		widgets = {
			'startdate': widgets.SelectDateWidget(),
			'enddate': widgets.SelectDateWidget()
		}

class FeeForm(ModelForm):
	class Meta:
		model = Fee
		fields = ['name', 'price', 'startdate', 'enddate']
		widgets = {
			'startdate': widgets.SelectDateWidget(),
			'enddate': widgets.SelectDateWidget()
		}


CampFeeFormSet = inlineformset_factory(Camp, Fee, form=FeeForm, extra=1)