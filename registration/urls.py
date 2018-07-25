from django.urls import path
from .views import add_registration, edit_registration, process_registration, finalize_registration
from .views import RegistrationList, CampList, RegistrationDelete

app_name = "registration"
urlpatterns = [
	path('', CampList.as_view(template_name="registration/registration_camp_list.html"), name="list-registrations"),
	path('manage/<int:pk>', RegistrationList.as_view(), name="manage-registrations"),
	path('manage/<int:pk>/add', add_registration, name="add-registration"),
	path('registration/<int:pk>/process', process_registration, name="process-registration"),
	path('registration/<int:pk>/finalize', finalize_registration, name="finalize-registration"),
	path('registration/<int:pk>/edit', edit_registration, name="edit-registration"),
	path('registration/<int:pk>/delete', RegistrationDelete.as_view(), name="delete-registration"),
]