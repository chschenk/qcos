from django.shortcuts import get_object_or_404, HttpResponseRedirect, render
from django.views.generic import CreateView, DeleteView, DetailView, ListView
from uuid import uuid4
from django.urls import reverse
from camps.models import Camp
from .models import Registration, TicketInfo, Ticket
from .forms import RegistrationForm, TicketInfoForm, FinalizeRegistrationForm


class RegistrationList(ListView):
	model = Registration

	def get_queryset(self):
		camp = get_object_or_404(Camp, pk=self.kwargs['pk'])
		return Registration.objects.filter(camp=camp)

	def get_context_data(self, **kwargs):
		camp = get_object_or_404(Camp, pk=self.kwargs['pk'])
		kwargs['camp'] = camp
		return super().get_context_data(**kwargs)


class CampList(ListView):
	model = Camp


class RegistrationDelete(DeleteView):
	model = Registration

	def get_success_url(self):
		return reverse('registration:manage-registrations', args=(self.object.camp.pk,))


def add_registration(request, **kwargs):
	camp = get_object_or_404(Camp, pk=kwargs['pk'])
	if request.method == "POST":
		forms = list()
		form = RegistrationForm(request.POST, request.FILES)
		if form.is_valid():
			valid = True
			for fee in camp.fee_set.all():
				instance = TicketInfo()
				instance.fee = fee
				ticket_info_form = TicketInfoForm(request.POST, request.FILES,
												  prefix="TicketInfo-{}".
												  format(fee.pk), instance=instance)
				valid = valid and ticket_info_form.is_valid()
				forms.append(ticket_info_form)
			registration = form.save(commit=False)
			if valid:
				registration.camp = camp
				registration.save()
				for info in forms:
					ticket_info = info.save(commit=False)
					if ticket_info.quantity <= 0:
						continue
					ticket_info.registration = registration
					ticket_info.save()
				return HttpResponseRedirect(reverse('registration:manage-registrations', args=(kwargs['pk'],)))
	else:
		form = RegistrationForm()
		forms = list()
		for fee in camp.fee_set.all():
			instance = TicketInfo()
			instance.fee = fee
			forms.append(TicketInfoForm(instance=instance, prefix="TicketInfo-{}".format(fee.pk)))
	return render(request, 'registration/registration_form.html', {'form': form, 'formset': forms, 'mode': 'Add'})


def edit_registration(request, **kwargs):
	registration = get_object_or_404(Registration, pk=kwargs['pk'])
	if request.method == "POST":
		forms = list()
		form = RegistrationForm(request.POST, request.FILES, instance=registration)
		if form.is_valid():
			valid = True
			for fee in registration.camp.fee_set.all():
				instance = TicketInfo()
				instance.fee = fee
				for info in registration.ticketinfo_set.all():
					if info.fee == fee:
						instance = info
				ticket_info_form = TicketInfoForm(request.POST, request.FILES,
												  prefix="TicketInfo-{}".
												  format(fee.pk), instance=instance)
				valid = valid and ticket_info_form.is_valid()
				forms.append(ticket_info_form)
			registration = form.save(commit=False)
			if valid:
				registration.save()
				for info in forms:
					ticket_info = info.save(commit=False)
					if ticket_info.quantity <= 0:
						continue
					ticket_info.registration = registration
					ticket_info.save()
				return HttpResponseRedirect(reverse('registration:manage-registrations', args=(registration.camp.pk,)))
	else:
		form = RegistrationForm(instance=registration)
		forms = list()
		for fee in registration.camp.fee_set.all():
			instance = TicketInfo()
			instance.fee = fee
			for info in registration.ticketinfo_set.all():
				if info.fee == fee:
					instance = info
			forms.append(TicketInfoForm(instance=instance, prefix="TicketInfo-{}".format(fee.pk)))
	return render(request, 'registration/registration_form.html', {'form': form, 'formset': forms, 'mode': 'Edit'})


def process_registration(request, **kwargs):
	registration = get_object_or_404(Registration, pk=kwargs['pk'])
	return render(request, 'registration/registration_process.html', {'registration': registration})


def finalize_registration(request, **kwargs):
	registration = get_object_or_404(Registration, pk=kwargs['pk'])
	if request.method == "POST":
		form = FinalizeRegistrationForm(request.POST, request.FILES, instance=registration)
		#print(form.errors)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('registration:manage-registrations', args=(registration.camp.pk,)))
	else:
		#Generating tickets
		for info in registration.ticketinfo_set.all():
			for i in range(len(info.ticket_set.all()), info.quantity):
				ticket = Ticket()
				ticket.ticket_info = info
				guid = uuid4()
				test = Ticket.objects.filter(guid=guid)
				while len(test)>0:
					guid=uuid4()
					test = Ticket.objects.filter(guid=guid)
				ticket.guid = guid
				ticket.save()

	form = FinalizeRegistrationForm(instance=registration)
	return render(request, 'registration/registration_finalize.html', {'form': form, 'registration': registration})
