from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView
from django.shortcuts import get_object_or_404
from .models import Diocese, District, Clan


class DioceseCreate(CreateView):
	model = Diocese
	fields = ['name']

	def get_success_url(self):
		return reverse('view-diocese', args=(self.object.pk,))

	def get_context_data(self, **kwargs):
		kwargs['mode'] = "Add"
		return super().get_context_data(**kwargs)


class DioceseList(ListView):
	model = Diocese


class DioceseUpdate(UpdateView):
	model = Diocese
	fields = ['name']
	success_url = reverse_lazy('list-dioceses')

	def get_context_data(self, **kwargs):
		kwargs['mode'] = "Edit"
		return super().get_context_data(**kwargs)


class DioceseDetail(DetailView):
	model = Diocese


class DioceseDelete(DeleteView):
	model = Diocese
	success_url = reverse_lazy('list-dioceses')


class DistrictCreate(CreateView):
	model = District
	fields = ['name']
	success_url = reverse_lazy('list-dioceses')

	def get_success_url(self):
		return reverse('view-district', args=(self.object.pk,))

	def get_context_data(self, **kwargs):
		diocese = get_object_or_404(Diocese, pk=self.kwargs['pk'])
		kwargs['diocese'] = diocese
		kwargs['mode'] = "Add"
		return super().get_context_data(**kwargs)

	def form_valid(self, form):
		form.instance.diocese = get_object_or_404(Diocese, pk=self.kwargs['pk'])
		return super(DistrictCreate, self).form_valid(form)


class DistrictUpdate(UpdateView):
	model = District
	fields = ['name']

	def get_success_url(self):
		return reverse('view-diocese', args=(self.object.diocese.pk,))

	def get_context_data(self, **kwargs):
		diocese = self.object.diocese
		kwargs['diocese'] = diocese
		kwargs['mode'] = "Edit"
		return super().get_context_data(**kwargs)


class DistrictDetail(DetailView):
	model = District


class DistrictDelete(DeleteView):
	model = District

	def get_success_url(self):
		return reverse('view-diocese', args=(self.object.diocese.pk,))


class ClanCreate(CreateView):
	model = Clan
	fields = ['name']

	def get_success_url(self):
		return reverse('view-district', args=(self.object.district.pk,))

	def get_context_data(self, **kwargs):
		district = get_object_or_404(District, pk=self.kwargs['pk'])
		kwargs['district'] = district
		kwargs['mode'] = "Add"
		return super().get_context_data(**kwargs)

	def form_valid(self, form):
		form.instance.district = get_object_or_404(District, pk=self.kwargs['pk'])
		return super(ClanCreate, self).form_valid(form)


class ClanUpdate(UpdateView):
	model = Clan
	fields = ['name']

	def get_success_url(self):
		return reverse('view-district', args=(self.object.district.pk,))

	def get_context_data(self, **kwargs):
		district = get_object_or_404(District, pk=self.kwargs['pk'])
		kwargs['district'] = district
		kwargs['mode'] = "Edit"
		return super().get_context_data(**kwargs)


class ClanDelete(DeleteView):
	model = Clan

	def get_success_url(self):
		return reverse('view-district', args=(self.object.district.pk,))
