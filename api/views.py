from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveAPIView
from django.views.generic.base import View
from django.http.response import HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import uuid
from datetime import datetime
from json import loads as json_load
from api.serializer import TicketSerializer, TicketInfoSerializer, FeeSerializer, CampSerializer, ClanSerializer, RegistrationSerializer
from camps.models import Camp, Fee
from base.models import Clan
from camp_registration.models import Registration, Ticket, TicketInfo


class TicketsToPrint(ListAPIView):
	authentication_classes = (BasicAuthentication,)
	permission_classes = (IsAuthenticated,)
	queryset = Ticket.objects.filter(printed=False)
	serializer_class = TicketSerializer


class TicketInfoRetrieveView(RetrieveAPIView):
	authentication_classes = (BasicAuthentication,)
	permission_classes = (IsAuthenticated,)
	queryset = TicketInfo.objects.all()
	lookup_field = 'pk'
	serializer_class = TicketInfoSerializer


class FeeRetrieveView(RetrieveAPIView):
	authentication_classes = (BasicAuthentication,)
	permission_classes = (IsAuthenticated,)
	queryset = Fee.objects.all()
	lookup_field = 'pk'
	serializer_class = FeeSerializer


class CampRetrieveView(RetrieveAPIView):
	authentication_classes = (BasicAuthentication,)
	permission_classes = (IsAuthenticated,)
	queryset = Camp.objects.all()
	lookup_field = 'pk'
	serializer_class = CampSerializer


class ClanRetrieveView(RetrieveAPIView):
	authentication_classes = (BasicAuthentication,)
	permission_classes = (IsAuthenticated,)
	queryset = Clan.objects.all()
	lookup_field = 'pk'
	serializer_class = ClanSerializer


class RegistrationRetrieveView(RetrieveAPIView):
	authentication_classes = (BasicAuthentication,)
	permission_classes = (IsAuthenticated,)
	queryset = Registration.objects.all()
	lookup_field = 'pk'
	serializer_class = RegistrationSerializer


class MarkTicketPrinted(View):
	authentication_classes = (BasicAuthentication,)
	permission_classes = (IsAuthenticated,)

	def post(self, request, pk):
		return HttpResponseBadRequest(content="Bad request type")

	def get(self, request, pk):
		ticket = get_object_or_404(Ticket, pk=pk, printed=False)
		ticket.printed = True
		ticket.save()
		return JsonResponse({'success': True})


class RegisterTicket(View):
	authentication_classes = (BasicAuthentication,)
	permission_classes = (IsAuthenticated,)

	@csrf_exempt
	def dispatch(self, request, *args, **kwargs):
		return super(RegisterTicket, self).dispatch(request, *args, **kwargs)

	def post(self, request):
		data = json_load(request.body.decode('ascii'))
		if 'guid' not in data:
			return HttpResponseBadRequest(content="You should have a guid field in your request body")
		try:
			guid = uuid.UUID(data['guid'])
		except ValueError:
			return HttpResponseBadRequest(content="{} is not a valid uuid".format(data['guid']))
		ticket = get_object_or_404(Ticket, guid=guid)
		response = {'success': False}
		if ticket.registrated is None:
			ticket.registrated = datetime.now()
			ticket.save()
			response['success'] = True
		return JsonResponse(response)

	def get(self, request):
		return HttpResponseBadRequest(content="Bad request type")

