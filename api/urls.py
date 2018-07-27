from django.urls import path
from .views import TicketsToPrint, TicketInfoRetrieveView, RegisterTicket, MarkTicketPrinted
from .views import FeeRetrieveView, CampRetrieveView, ClanRetrieveView, RegistrationRetrieveView


urlpatterns = [
	path('ticketstoprint/', TicketsToPrint.as_view(), name="tickets-to-print"),
	path('ticketinfo/<int:pk>/', TicketInfoRetrieveView.as_view(), name='ticketinfo-detail'),
	path('registerTicket/', RegisterTicket.as_view(), name='registerTicket'),
	path('markTicketPrinted/<int:pk>/', MarkTicketPrinted.as_view(), name='markTicketPrinted'),
	path('fee/<int:pk>/', FeeRetrieveView.as_view(), name='fee-detail'),
	path('camp/<int:pk>/', CampRetrieveView.as_view(), name='camp-detail'),
	path('clan/<int:pk>/', ClanRetrieveView.as_view(), name='clan-detail'),
	path('registration/<int:pk>/', RegistrationRetrieveView.as_view(), name='registration-detail'),
]