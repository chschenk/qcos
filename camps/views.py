from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import CampForm, FeeForm, CampFeeFormSet
from .models import Camp, Fee


class CampListView(LoginRequiredMixin, ListView):
	model = Camp
	paginate_by = 10


class CampDeleteView(LoginRequiredMixin, DeleteView):
	model = Camp
	success_url = reverse_lazy('list-camps')


@login_required(login_url=reverse_lazy('login'))
def add_camp(request):
	if request.method == "POST":
		form = CampForm(request.POST, request.FILES)
		if form.is_valid():
			camp = form.save(commit=False)
			formset = CampFeeFormSet(request.POST, request.FILES, instance=camp)
			if formset.is_valid():
				camp.save()
				formset.save()
				return HttpResponseRedirect("/camps/")
	else:
		form = CampForm()
		formset = CampFeeFormSet()
	return render(request, 'camps/camp_form.html', {'form': form, 'formset': formset, 'mode': 'Add'})


@login_required(login_url=reverse_lazy('login'))
def edit_camp(request, pk):
	camp = Camp.objects.get(pk=pk)
	if request.method == "POST":
		formset = CampFeeFormSet(request.POST, request.FILES, instance=camp)
		form = CampForm(request.POST, request.FILES, instance=camp)
		if formset.is_valid() and form.is_valid():
			form.save()
			formset.save()
			return HttpResponseRedirect("/camps/")
	else:
		form = CampForm(instance=camp)
		formset = CampFeeFormSet(instance=camp)
	return render(request, 'camps/camp_form.html', {'form': form, 'formset': formset, 'mode': 'Edit'})
