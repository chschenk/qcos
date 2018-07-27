from rest_framework import serializers
from camps.models import Camp, Fee
from base.models import Clan
from camp_registration.models import Registration, Ticket, TicketInfo


class TicketSerializer(serializers.ModelSerializer):
	class Meta:
		model = Ticket
		fields = ('pk', 'guid', 'registrated', 'ticket_info')


class TicketInfoSerializer(serializers.ModelSerializer):
	class Meta:
		model = TicketInfo
		fields = ('quantity', 'fee', 'registration')


class FeeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Fee
		fields = ('name', 'price', 'startdate', 'enddate', 'camp')


class CampSerializer(serializers.ModelSerializer):
	class Meta:
		model = Camp
		fields = ('name', 'startdate', 'enddate')


class ClanSerializer(serializers.ModelSerializer):
	class Meta:
		model = Clan
		fields = ('name',)


class RegistrationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Registration
		fields = ('clan', 'comment')
