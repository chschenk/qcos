from django.shortcuts import render
from django.views.generic import ListView, DeleteView, View
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CampForm, FeeForm, CampFeeFormSet
from .models import Camp, Fee


class CampListView(LoginRequiredMixin, ListView):
	model = Camp
	paginate_by = 10


class CampDeleteView(LoginRequiredMixin, DeleteView):
	model = Camp
	success_url = reverse_lazy('list-camps')


class CampAddView(LoginRequiredMixin, View):

	def post(self, request):
		form = CampForm(request.POST, request.FILES)
		if form.is_valid():
			camp = form.save(commit=False)
			formset = CampFeeFormSet(request.POST, request.FILES, instance=camp)
			if formset.is_valid():
				camp.save()
				formset.save()
				return HttpResponseRedirect("/camps/")

	def get(self, request):
		form = CampForm()
		formset = CampFeeFormSet()
		return render(request, 'camps/camp_form.html', {'form': form, 'formset': formset, 'mode': 'Add'})


class CampEditView(LoginRequiredMixin, View):

	def post(self, request, pk):
		camp = Camp.objects.get(pk=pk)
		formset = CampFeeFormSet(request.POST, request.FILES, instance=camp)
		form = CampForm(request.POST, request.FILES, instance=camp)
		if formset.is_valid() and form.is_valid():
			form.save()
			formset.save()
			return HttpResponseRedirect("/camps/")

	def get(self, request, pk):
		camp = Camp.objects.get(pk=pk)
		form = CampForm(instance=camp)
		formset = CampFeeFormSet(instance=camp)
		return render(request, 'camps/camp_form.html', {'form': form, 'formset': formset, 'mode': 'Edit'})
