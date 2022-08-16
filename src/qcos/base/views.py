from io import BytesIO
from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView, FormView, View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils.translation import gettext as _
from django.urls.base import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.db.models import Max
from django.http import HttpResponse
from xlwt import Workbook
from xlsxwriter import Workbook
from qcos.base.models import Diocese, District, Clan, Camp, Fee, Registration, TicketInfo, Workshop, WorkshopPrintBatch
from qcos.base.forms import SignUpForm, OrganizerForm, TicketInfoForm, RegistrationForm, CheckInFormStep1
from qcos.base.forms import CheckInFormStep2, WorkshopAnnotateForm, WorkshopPrintForm


class DioceseCreateView(LoginRequiredMixin, CreateView):
	model = Diocese
	fields = ['name']

	def get_success_url(self):
		return reverse('detail-diocese', args=(self.object.pk,))

	def get_context_data(self, **kwargs):
		kwargs['mode'] = _("Create")
		return super(DioceseCreateView, self).get_context_data(**kwargs)


class DioceseListView(LoginRequiredMixin, ListView):
	model = Diocese
	ordering = ['name']


class DioceseUpdateView(LoginRequiredMixin, UpdateView):
	model = Diocese
	fields = ['name']

	def get_success_url(self):
		return reverse('detail-diocese', args=(self.object.pk,))

	def get_context_data(self, **kwargs):
		kwargs['mode'] = _("Update")
		return super(DioceseUpdateView, self).get_context_data(**kwargs)


class DioceseDetailView(LoginRequiredMixin, DetailView):
	model = Diocese


class DioceseDeleteView(LoginRequiredMixin, DeleteView):
	model = Diocese
	success_url = reverse_lazy('list-diocese')


class DistrictCreateView(LoginRequiredMixin, CreateView):
	model = District
	fields = ['name']

	def get_success_url(self):
		return reverse('detail-district', args=(self.object.pk,))

	def get_context_data(self, **kwargs):
		diocese = get_object_or_404(Diocese, pk=self.kwargs['diocese_pk'])
		kwargs['diocese'] = diocese
		kwargs['mode'] = _("Create")
		return super(DistrictCreateView, self).get_context_data(**kwargs)

	def form_valid(self, form):
		form.instance.diocese = get_object_or_404(Diocese, pk=self.kwargs['diocese_pk'])
		return super(DistrictCreateView, self).form_valid(form)


class DistrictListView(LoginRequiredMixin, ListView):
	model = District
	ordering = ['name']


class DistrictUpdateView(LoginRequiredMixin, UpdateView):
	model = District
	fields = ['name']

	def get_success_url(self):
		return reverse('detail-district', args=(self.object.pk,))

	def get_context_data(self, **kwargs):
		diocese = self.object.diocese
		kwargs['diocese'] = diocese
		kwargs['mode'] = _("Update")
		return super(DistrictUpdateView, self).get_context_data(**kwargs)


class DistrictDetailView(LoginRequiredMixin, DetailView):
	model = District


class DistrictDeleteView(LoginRequiredMixin, DeleteView):
	model = District

	def get_success_url(self):
		return reverse('detail-diocese', args=(self.object.diocese.pk,))


class ClanCreateView(LoginRequiredMixin, CreateView):
	model = Clan
	fields = ['name']

	def get_success_url(self):
		return reverse('detail-district', args=(self.object.district.pk,))

	def get_context_data(self, **kwargs):
		district = get_object_or_404(District, pk=self.kwargs['district_pk'])
		kwargs['district'] = district
		kwargs['mode'] = _("Create")
		return super(ClanCreateView, self).get_context_data(**kwargs)

	def form_valid(self, form):
		form.instance.district = get_object_or_404(District, pk=self.kwargs['district_pk'])
		return super(ClanCreateView, self).form_valid(form)


class ClanListView(LoginRequiredMixin, ListView):
	model = Clan
	ordering = ['name']


class ClanUpdateView(LoginRequiredMixin, UpdateView):
	model = Clan
	fields = ['name']

	def get_success_url(self):
		return reverse('detail-district', args=(self.object.district.pk,))

	def get_context_data(self, **kwargs):
		district = self.object.district
		kwargs['district'] = district
		kwargs['mode'] = _("Update")
		return super(ClanUpdateView, self).get_context_data(**kwargs)


class ClanDetailView(LoginRequiredMixin, DetailView):
	model = Clan


class ClanDeleteView(LoginRequiredMixin, DeleteView):
	model = Clan

	def get_success_url(self):
		return reverse('detail-district', args=(self.object.district.pk,))


class UserListView(LoginRequiredMixin, ListView):
	model = User
	ordering = ['username']


class UserCreateView(PermissionRequiredMixin, CreateView):
	form_class = SignUpForm
	success_url = reverse_lazy('list-user')
	template_name = "auth/user_form.html"
	permission_required = "user.create"

	def get_context_data(self, **kwargs):
		ctx = super(UserCreateView, self).get_context_data(**kwargs)
		ctx['mode'] = _('Create')
		return ctx


class UserUpdateView(PermissionRequiredMixin, UpdateView):
	permission_required = 'user.update'
	fields = ('username', 'first_name', 'last_name', 'email')
	context_object_name = 'object'
	model = User
	success_url = reverse_lazy('list-user')

	def get_context_data(self, **kwargs):
		ctx = super(UserUpdateView, self).get_context_data(**kwargs)
		ctx['mode'] = _('Update')
		return ctx


class UserDeleteView(PermissionRequiredMixin, DeleteView):
	permission_required = 'user.delete'
	model = User
	context_object_name = 'object'
	success_url = reverse_lazy('list-user')


class UserDetailView(PermissionRequiredMixin, DetailView):
	permission_required = 'user.view'
	context_object_name = 'object'
	model = User


class UserProfileView(LoginRequiredMixin, TemplateView):
	template_name = "auth/user_profile.html"


class OrganizerListView(PermissionRequiredMixin, ListView):
	permission_required = 'group.view'
	model = Group
	ordering = ['name']


class OrganizerCreateView(PermissionRequiredMixin, CreateView):
	permission_required = 'group.create'
	model = Group
	fields = ('name', )
	success_url = reverse_lazy('list-organizer')

	def get_context_data(self, **kwargs):
		ctx = super(OrganizerCreateView, self).get_context_data(**kwargs)
		ctx['mode'] = _('Create')
		return ctx


class OrganizerUpdateView(PermissionRequiredMixin, UpdateView):
	permission_required = 'group.update'
	model = Group
	form_class = OrganizerForm
	success_url = reverse_lazy('list-organizer')

	def get_context_data(self, **kwargs):
		ctx = super(OrganizerUpdateView, self).get_context_data(**kwargs)
		ctx['mode'] = _('Update')
		return ctx


class OrganizerDeleteView(PermissionRequiredMixin, DeleteView):
	permission_required = 'group.delete'
	model = Group
	success_url = reverse_lazy('list-organizer')


class OrganizerDetailView(PermissionRequiredMixin, DetailView):
	permission_required = 'group.update'
	model = Group


class CampListView(LoginRequiredMixin, ListView):
	model = Camp
	ordering = ['name']


class CampCreateView(LoginRequiredMixin, CreateView):
	model = Camp
	fields = '__all__'

	def get_context_data(self, **kwargs):
		ctx = super(CampCreateView, self).get_context_data(**kwargs)
		ctx['mode'] = _('Create')
		return ctx

	def get_success_url(self):
		return reverse('detail-camp', args=(self.object.pk,))


class CampMixin:

	def get_context_data(self, **kwargs):
		ctx = super(CampMixin, self).get_context_data(**kwargs)
		ctx['camp'] = Camp.objects.get(pk=self.kwargs['camp_pk'])
		return ctx


class RegistrationMixin:

	def get_context_data(self, **kwargs):
		ctx = super(RegistrationMixin, self).get_context_data(**kwargs)
		ctx['registration'] = Registration.objects.get(pk=self.kwargs['pk'])
		ctx['clan'] = ctx['registration'].clan
		return ctx


class CampUpdateView(LoginRequiredMixin, UpdateView):
	model = Camp
	fields = '__all__'

	def get_context_data(self, **kwargs):
		ctx = super(CampUpdateView, self).get_context_data(**kwargs)
		ctx['mode'] = _('Update')
		return ctx

	def get_success_url(self):
		return reverse('detail-camp', args=(self.object.pk,))


class CampDeleteView(LoginRequiredMixin, DeleteView):
	model = Camp
	success_url = reverse_lazy('list-camp')


class CampDetailView(LoginRequiredMixin, DetailView):
	model = Camp


class FeeCreateView(LoginRequiredMixin, CampMixin, CreateView):
	model = Fee
	fields = ('name', 'price', 'start_date', 'end_date')

	def get_context_data(self, **kwargs):
		ctx = super(FeeCreateView, self).get_context_data(**kwargs)
		ctx['mode'] = _('Create')
		return ctx

	def form_valid(self, form):
		form.instance.camp = get_object_or_404(Camp, pk=self.kwargs['camp_pk'])
		return super(FeeCreateView, self).form_valid(form)

	def get_success_url(self):
		return reverse('detail-camp', args=(self.object.camp.pk,))


class FeeDeleteView(LoginRequiredMixin, CampMixin, DeleteView):
	model = Fee

	def get_success_url(self):
		return reverse('detail-camp', args=(self.object.camp.pk,))


class FeeUpdateView(LoginRequiredMixin, CampMixin, UpdateView):
	model = Fee
	fields = ('name', 'price', 'start_date', 'end_date')

	def get_context_data(self, **kwargs):
		ctx = super(FeeUpdateView, self).get_context_data(**kwargs)
		ctx['mode'] = _('Update')
		return ctx

	def get_success_url(self):
		return reverse('detail-camp', args=(self.object.camp.pk,))


class RegistrationCreateView(LoginRequiredMixin, View):
	template_name = "base/registration_form.html"

	def get(self, request, *args, **kwargs):
		camp = get_object_or_404(Camp, pk=kwargs['camp_pk'])
		form = RegistrationForm
		formset = list()
		for fee in camp.fee_set.all():
			instance = TicketInfo()
			instance.fee = fee
			formset.append(TicketInfoForm(instance=instance, prefix="TicketInfo-{}".format(fee.pk)))
		return render(request, self.template_name, {'camp': camp, 'form': form, 'formset': formset, 'mode': _('New')})

	def post(self, request, *args, **kwargs):
		camp = get_object_or_404(Camp, pk=kwargs['camp_pk'])
		formset = list()
		form = RegistrationForm(request.POST, request.FILES)
		if form.is_valid():
			valid = True
			for fee in camp.fee_set.all():
				instance = TicketInfo()
				instance.fee = fee
				ticket_info_form = TicketInfoForm(request.POST, request.FILES, prefix="TicketInfo-{}".format(fee.pk), instance=instance)
				valid = valid and ticket_info_form.is_valid()
				formset.append(ticket_info_form)
			registration = form.save(commit=False)
			if valid:
				registration.camp = camp
				registration.save()
				for info in formset:
					ticket_info = info.save(commit=False)
					if ticket_info.quantity <= 0:
						continue
					ticket_info.registration = registration
					ticket_info.save()
				return HttpResponseRedirect(reverse('list-registration', args=(kwargs['camp_pk'],)))
		return self.get(request, *args, **kwargs)


class RegistrationUpdateView(LoginRequiredMixin, View):
	template_name = "base/registration_form.html"

	def get(self, request, *args, **kwargs):
		camp = get_object_or_404(Camp, pk=kwargs['camp_pk'])
		registration = get_object_or_404(Registration, pk=kwargs['pk'])
		form = RegistrationForm(instance=registration)
		formset = list()
		for fee in camp.fee_set.all():
			instance = TicketInfo()
			instance.fee = fee
			for ticket_info in registration.ticketinfo_set.all():
				if fee.pk == ticket_info.fee.pk:
					instance = ticket_info
			formset.append(TicketInfoForm(instance=instance, prefix="TicketInfo-{}".format(fee.pk)))
		return render(request, self.template_name, {'camp': camp, 'form': form, 'formset': formset, 'mode': _('Update')})

	def post(self, request, *args, **kwargs):
		camp = get_object_or_404(Camp, pk=kwargs['camp_pk'])
		formset = list()
		registration = get_object_or_404(Registration, pk=kwargs['pk'])
		form = RegistrationForm(request.POST, request.FILES, instance=registration)
		if form.is_valid():
			valid = True
			for fee in camp.fee_set.all():
				instance = TicketInfo()
				instance.fee = fee
				for ticket_info in registration.ticketinfo_set.all():
					if fee.pk == ticket_info.fee.pk:
						instance = ticket_info
				ticket_info_form = TicketInfoForm(request.POST, request.FILES, prefix="TicketInfo-{}".format(fee.pk), instance=instance)
				valid = valid and ticket_info_form.is_valid()
				formset.append(ticket_info_form)
			registration = form.save(commit=False)
			if valid:
				registration.camp = camp
				registration.save()
				for info in formset:
					ticket_info = info.save(commit=False)
					if ticket_info.quantity <= 0:
						continue
					ticket_info.registration = registration
					ticket_info.save()
				return HttpResponseRedirect(reverse('list-registration', args=(kwargs['camp_pk'],)))
		return self.get(request, *args, **kwargs)


class RegistrationListView(LoginRequiredMixin, CampMixin, ListView):
	model = Registration
	ordering = ['clan.name']

	def get_queryset(self):
		return Registration.objects.filter(camp_id=self.kwargs.get('camp_pk'))


class RegistrationDetailView(LoginRequiredMixin, CampMixin, DetailView):
	model = Registration


class RegistrationDeleteView(LoginRequiredMixin, CampMixin, DeleteView):
	model = Registration

	def get_success_url(self):
		return reverse('list-registration', args=(self.kwargs['camp_pk'],))


class UserHomeView(LoginRequiredMixin, TemplateView):
	template_name = "auth/user_home.html"


class RegestrationCheckinStep1View(LoginRequiredMixin, CampMixin, RegistrationMixin, UpdateView):
	template_name = "base/checkin_step1.html"
	model = Registration
	form_class = CheckInFormStep1

	def get_success_url(self):
		return reverse('checkin-registration-step2', args=(self.kwargs['camp_pk'], self.kwargs['pk']))


class RegestrationCheckinStep2View(LoginRequiredMixin, CampMixin, RegistrationMixin, UpdateView):
	template_name = "base/checkin_step2.html"
	model = Registration
	form_class = CheckInFormStep2

	def get_success_url(self):
		return reverse('checkin-registration-step3', args=(self.kwargs['camp_pk'], self.kwargs['pk']))


class RegestrationCheckinStep3View(LoginRequiredMixin, CampMixin, RegistrationMixin, TemplateView):
	template_name = "base/checkin_step3.html"


class WorkshopCreateView(LoginRequiredMixin, CampMixin, RegistrationMixin, CreateView):
	model = Workshop
	fields = ('name', 'description', 'status')

	def get_context_data(self, **kwargs):
		ctx = super(WorkshopCreateView, self).get_context_data(**kwargs)
		ctx['mode'] = _('Create')
		return ctx

	def form_valid(self, form):
		form.instance.registration = get_object_or_404(Registration, pk=self.kwargs['pk'])
		return super(WorkshopCreateView, self).form_valid(form)

	def get_success_url(self):
		return reverse('detail-registration', args=(self.kwargs['camp_pk'], self.kwargs['pk']))


class WorkshopUpdateView(LoginRequiredMixin, CampMixin, RegistrationMixin, UpdateView):
	model = Workshop
	fields = ('name', 'description', 'status')

	def get_context_data(self, **kwargs):
		ctx = super(WorkshopUpdateView, self).get_context_data(**kwargs)
		ctx['mode'] = _('Update')
		return ctx

	def get_success_url(self):
		return reverse('detail-registration', args=(self.kwargs['camp_pk'], self.kwargs['registration_pk']))


class WorkshopDeleteView(LoginRequiredMixin, CampMixin, RegistrationMixin, DeleteView):
	model = Workshop

	def get_success_url(self):
		return reverse('detail-registration', args=(self.kwargs['camp_pk'], self.kwargs['registration_pk']))


class WorkshopListView(LoginRequiredMixin, CampMixin, ListView):
	model = Workshop
	ordering = ['workshop.registration', 'name', 'annotated_id']

	def get_queryset(self):
		camp = get_object_or_404(Camp, pk=self.kwargs['camp_pk'])
		return Workshop.objects.filter(registration__camp=camp)


class WorkshopAnnotateView(LoginRequiredMixin, CampMixin, FormView):
	form_class = WorkshopAnnotateForm
	template_name = "base/workshop_annotate.html"

	def form_valid(self, form):
		camp = get_object_or_404(Camp, pk=self.kwargs['camp_pk'])
		index =  Workshop.objects.filter(registration__camp=camp).aggregate(Max('annotated_id'))['annotated_id__max']
		if index is None:
			index = 0
		index += 1
		workshops = Workshop.objects.filter(registration__camp=camp, status="OK", annotated_id=None)
		for workshop in workshops:
			workshop.annotated_id = index
			index += 1
			workshop.save()
		return super(WorkshopAnnotateView, self).form_valid(form)

	def get_success_url(self):
		return reverse('list-workshop', args=(self.kwargs['camp_pk'], ))


class WorkshopPrintView(LoginRequiredMixin, CampMixin, FormView):
	form_class = WorkshopPrintForm
	template_name = "base/workshop_print.html"

	def form_valid(self, form):
		camp = get_object_or_404(Camp, pk=self.kwargs['camp_pk'])
		workshops = Workshop.objects.filter(registration__camp=camp, printed=None).exclude(annotated_id=None)
		if len(workshops)==0:
			return super(WorkshopPrintView, self).form_valid(form)
		batch = WorkshopPrintBatch()
		batch.camp= camp
		batch.save()
		workshops = Workshop.objects.filter(registration__camp=camp, printed=None).exclude(annotated_id=None)
		for workshop in workshops:
			workshop.printed = batch
			workshop.save()
		return super(WorkshopPrintView, self).form_valid(form)

	def get_success_url(self):
		return reverse('list-workshop', args=(self.kwargs['camp_pk'], ))


class WorkshopPrintBatchListView(LoginRequiredMixin, CampMixin, ListView):
	model = WorkshopPrintBatch
	ordering = ['created']

	def get_queryset(self):
		camp = get_object_or_404(Camp, pk=self.kwargs['camp_pk'])
		return WorkshopPrintBatch.objects.filter(camp=camp)


class WorkshopPrintBatchDownloadView(LoginRequiredMixin, View):

	def get(self, request, *args, **kwargs):
		batch = get_object_or_404(WorkshopPrintBatch, pk=self.kwargs['batch_pk'])
		output = BytesIO()
		workbook = Workbook(output)
		sheet = workbook.add_worksheet(_("Workshops"))
		sheet.write(0, 0, _("Diocese"))
		sheet.write(0, 1, _("District"))
		sheet.write(0, 2, _("Clan"))
		sheet.write(0, 3, _("Name"))
		sheet.write(0, 4, _("Workshop ID"))
		row = 1
		for workshop in batch.workshop_set.all():
			sheet.write(row, 0, str(workshop.registration.clan.district.diocese))
			sheet.write(row, 1, str(workshop.registration.clan.district))
			sheet.write(row, 2, str(workshop.registration.clan))
			sheet.write(row, 3, str(workshop.name))
			sheet.write(row, 4, int(workshop.annotated_id))
			row += 1

		workbook.close()
		output.seek(0)
		filename="Workshops-{}.xlsx".format(batch.created.strftime("%Y-%m-%d-%H-%M"))
		response = HttpResponse(output,
								content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
		response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
		return response


class ParticipantCheckInListView(LoginRequiredMixin, CampMixin, ListView):
	template_name = "base/participant_checkin_list.html"
	model = Registration
	ordering = ['clan.district.dioces.name', 'clan.district.name', 'clan.name']

	def get_queryset(self):
		return Registration.objects.filter(camp_id=self.kwargs.get('camp_pk'))


class ParticipantCheckInView(LoginRequiredMixin, CampMixin, RegistrationMixin, UpdateView):
	template_name = "base/participant_checkin.html"
	model = Registration
	fields = ('registered_participants', )

	def get_success_url(self):
		return reverse('list-checkin-participants', args=(self.kwargs['camp_pk'],))

class RegistrationDownloadView(LoginRequiredMixin, View):

	def get(self, request, *args, **kwargs):
		camp = get_object_or_404(Camp, pk=self.kwargs['camp_pk'])
		output = BytesIO()
		workbook = Workbook(output)
		sheet = workbook.add_worksheet(_("Registrations"))
		col = 0
		sheet.write(0, col, _("Diocese"))
		col += 1
		sheet.write(0, col, _("District"))
		col += 1
		sheet.write(0, col, _("Clan"))
		col += 1
		for fee in camp.fee_set.all().order_by('pk'):
			sheet.write(0, col, _(fee.name))
			col += 1
		sheet.write(0, col, _("Participants"))
		col += 1
		sheet.write(0, col, _("Present participants"))
		col += 1
		sheet.write(0, col, _("Registered participants"))
		col += 1
		sheet.write(0, col, _("Price"))
		col += 1
		sheet.write(0, col, _("Paid"))
		col += 1
		sheet.write(0, col, _("Rules accepted"))
		col += 1
		sheet.write(0, col, _("Picture rights"))
		col += 1
		sheet.write(0, col, _("Staff confirmed"))
		col += 1
		sheet.write(0, col, _("Comment"))
		col += 1
		sheet.write(0, col, _("Contact"))
		col += 1
		sheet.write(0, col, _("E-Mail"))
		col += 1
		sheet.write(0, col, _("Telephone"))

		row = 1
		for registration in camp.registration_set.all():
			col = 0
			sheet.write(row, col, str(registration.clan.district.diocese))
			col += 1
			sheet.write(row, col, str(registration.clan.district))
			col += 1
			sheet.write(row, col, str(registration.clan))
			col += 1
			for fee in camp.fee_set.all().order_by('pk'):
				quantity = 0
				try:
					info = registration.ticketinfo_set.get(fee=fee)
					quantity = info.quantity
				except TicketInfo.DoesNotExist:
					quantity = 0
				sheet.write(row, col, int(quantity))
				col += 1
			sheet.write(row, col, int(registration.participants()))
			col += 1
			sheet.write(row, col, int(registration.present_participants))
			col += 1
			sheet.write(row, col, int(registration.registered_participants))
			col += 1
			sheet.write(row, col, float(registration.get_price()))
			col += 1
			sheet.write(row, col, float(registration.paid))
			col += 1
			answer = "X" if registration.rules_accepted else ""
			sheet.write(row, col, answer)
			col += 1
			answer = "X" if registration.picture_rights else ""
			sheet.write(row, col, answer)
			col += 1
			answer = "X" if registration.staff_confirmed else ""
			sheet.write(row, col, answer)
			col += 1
			sheet.write(row, col, str(registration.comment))
			col += 1
			sheet.write(row, col, str(registration.contact_name))
			col += 1
			sheet.write(row, col, str(registration.email))
			col += 1
			sheet.write(row, col, str(registration.telephone))
			col += 1
			row += 1
		workbook.close()
		output.seek(0)
		filename="Registrations-{}.xlsx".format(camp.name)
		response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
		response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
		return response