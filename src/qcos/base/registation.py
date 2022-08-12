from django.http.response import HttpResponseNotAllowed
from django.views.generic.base import TemplateResponseMixin


class BaseRegistrationCreateFlowStep:

	def __init__(self, camp):
		self.camp = camp
		self.request = None #Needed?

	@property
	def identifier(self):
		raise NotImplementedError()

	@property
	def identifier(self):
		raise NotImplementedError()

	@property
	def priority(self):
		return 100

	def is_applicable(self, request):
		return True

	def is_completed(self, request):
		raise NotImplementedError()

	def get_next_applicable(self, request):
		if hasattr(self, '_next') and self._next:
			if not self._next.is_applicable(request):
				return self._next.get_next_applicable(request)
			return self._next

	def get_prev_applicable(self, request):
		if hasattr(self, '_previous') and self._previous:
			if not self._previous.is_applicable(request):
				return self._previous.get_prev_applicable(request)
		return self._previous

	def get(self, request):
		return HttpResponseNotAllowed([])

	def post(self, request):
		return HttpResponseNotAllowed([])