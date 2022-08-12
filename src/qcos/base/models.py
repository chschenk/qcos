from django.db.models import Model, ForeignKey, CASCADE, PROTECT, SET_NULL
from django.db.models.fields import CharField, SlugField, DateField, DecimalField, TextField, DateTimeField
from django.db.models.fields import EmailField, BooleanField, PositiveIntegerField
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group


class Diocese(Model):
	name = CharField(max_length=100)

	class Meta:
		default_permissions = ('view')

	def __str__(self):
		return self.name


class District(Model):
	name = CharField(max_length=100)
	diocese = ForeignKey(Diocese, on_delete=CASCADE)

	class Meta:
		default_permissions = ('view')

	def __str__(self):
		return self.name


class Clan(Model):
	name = CharField(max_length=100)
	district = ForeignKey(District, on_delete=CASCADE)

	class Meta:
		default_permissions = ('view')

	def __str__(self):
		return self.name


class Camp(Model):
	name = CharField(max_length=100)
	organizer = ForeignKey(Group, on_delete=CASCADE)
	description = CharField(max_length=500)
	slug = SlugField(max_length=100)
	start_date = DateField()
	end_date = DateField()

	class Meta:
		default_permissions = ()

	def registration_quantity(self):
		count = 0
		for fee in self.fee_set.all():
			count += fee.quantity()
		return count

	def __str__(self):
		return self.name


class Fee(Model):
	camp = ForeignKey(Camp, on_delete=CASCADE)
	name = CharField(max_length=100)
	price = DecimalField(decimal_places=2, max_digits=4)
	start_date = DateField(null=True, blank=True)
	end_date = DateField(null=True, blank=True)

	class Meta:
		default_permissions = ()

	def quantity(self):
		count = 0
		for ticket_info in self.ticketinfo_set.all():
			count += ticket_info.quantity
		return count


	def __str__(self):
		return self.name


class Registration(Model):
	clan = ForeignKey(Clan, on_delete=PROTECT)
	camp = ForeignKey(Camp, on_delete=CASCADE)
	telephone = CharField(max_length=100)
	contact_name = CharField(max_length=100)
	email = EmailField(max_length=100)
	comment = TextField(max_length=1000, null=True, blank=True)
	paid = DecimalField(decimal_places=2, max_digits=6, default=0)
	present_participants = PositiveIntegerField(default=0)
	#ToDo: Replace with ticket model
	registered_participants = PositiveIntegerField(default=0)
	#ToDo: Move into JsonField(?) and make this configurable
	rules_accepted = BooleanField(default=False)
	staff_confirmed = BooleanField(default=False)
	picture_rights = BooleanField(default=False)


	class Meta:
		default_permissions = ()

	def get_full_ticket_info(self):
		ticket_infos = list()
		fees = self.camp.fee_set.order_by('id')
		for fee in fees:
			data = dict()
			data['name'] = fee.name
			data['price'] = fee.price
			try:
				data['quantity'] = self.ticketinfo_set.get(fee=fee).quantity
			except ObjectDoesNotExist:
				data['quantity'] = 0
			data['full_price'] = data['quantity'] * fee.price
			ticket_infos.append(data)
		return ticket_infos

	def participants(self):
		participants = 0
		for info in self.ticketinfo_set.all():
			participants += info.quantity
		return participants

	def get_price(self):
		price = 0
		for info in self.ticketinfo_set.all():
			price += (info.fee.price * info.quantity)
		return price

	def get_ticket_infos(self):
		ticket_infos = list()
		fees = self.camp.fee_set.order_by('id')
		for fee in fees:
			try:
				info = self.ticketinfo_set.get(fee=fee).quantity
			except ObjectDoesNotExist:
				info = 0
			ticket_infos.append(info)
		return ticket_infos


class TicketInfo(Model):
	registration = ForeignKey(Registration, on_delete=CASCADE)
	fee = ForeignKey(Fee, on_delete=PROTECT)
	quantity = PositiveIntegerField(default=0)

	class Meta:
		default_permissions = ()

	def price(self):
		return self.quantity * self.fee.price

	def __str__(self):
		return str(self.quantity)


class Ticket(Model):
	ticket_info = ForeignKey(TicketInfo, on_delete=PROTECT)
	registered = DateTimeField(null=True)
	issued = BooleanField()

	class Meta:
		default_permissions = ()

WORKSHOP_STATUS=(
	("OK", "Workshop OK"),
	("FE", "Workshop fehlt"),
	("NO", "Workshop nicht OK"),
	("UN", "Workshop unklar"),
)

class WorkshopPrintBatch(Model):
	created = DateTimeField(auto_now_add=True)
	camp = ForeignKey(Camp, on_delete=CASCADE)


class Workshop(Model):
	registration = ForeignKey(Registration, on_delete=CASCADE)
	name = CharField(max_length=100)
	description = TextField(max_length=1000, null=True, blank=True)
	printed = ForeignKey(WorkshopPrintBatch, null=True, on_delete=SET_NULL)
	annotated_id = PositiveIntegerField(null=True)
	status = CharField(max_length=2, choices=WORKSHOP_STATUS, default="FE")

	def __str__(self):
		return self.name

