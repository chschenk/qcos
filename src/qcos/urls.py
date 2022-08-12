from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from qcos.base.views import DioceseCreateView, DioceseDeleteView, DioceseDetailView, DioceseListView, DioceseUpdateView
from qcos.base.views import DistrictCreateView, DistrictUpdateView, DistrictDeleteView, DistrictDetailView
from qcos.base.views import ClanCreateView, ClanDetailView, ClanDeleteView, ClanUpdateView, CampCreateView
from qcos.base.views import UserListView, UserCreateView, UserUpdateView, UserDeleteView, OrganizerListView
from qcos.base.views import OrganizerCreateView, OrganizerUpdateView, OrganizerDeleteView, OrganizerDetailView
from qcos.base.views import CampListView, CampDetailView, CampDeleteView, CampUpdateView, FeeCreateView, FeeDeleteView
from qcos.base.views import FeeUpdateView, RegistrationCreateView, UserDetailView, UserProfileView, RegistrationListView
from qcos.base.views import UserHomeView, RegistrationDetailView, RegistrationUpdateView, RegistrationDeleteView
from qcos.base.views import RegestrationCheckinStep1View, RegestrationCheckinStep2View, RegestrationCheckinStep3View
from qcos.base.views import WorkshopCreateView, WorkshopUpdateView, WorkshopDeleteView, WorkshopListView
from qcos.base.views import WorkshopAnnotateView, WorkshopPrintView, WorkshopPrintBatchListView
from qcos.base.views import WorkshopPrintBatchDownloadView, ParticipantCheckInListView, ParticipantCheckInView

urlpatterns = [
	path('admin/', admin.site.urls),
	path('accounts/', include('django.contrib.auth.urls')),

	path("select2/", include("django_select2.urls")),

	path('base/diocese', DioceseListView.as_view(), name="list-diocese"),
	path('base/diocese/create', DioceseCreateView.as_view(), name="create-diocese"),
	path('base/diocese/<int:pk>/delete', DioceseDeleteView.as_view(), name="delete-diocese"),
	path('base/diocese/<int:pk>/detail', DioceseDetailView.as_view(), name="detail-diocese"),
	path('base/diocese/<int:pk>/update', DioceseUpdateView.as_view(), name="update-diocese"),

	path('base/diocese/<int:diocese_pk>/create_district', DistrictCreateView.as_view(), name="create-district"),
	path('base/district/<int:pk>/delete', DistrictDeleteView.as_view(), name="delete-district"),
	path('base/district/<int:pk>/detail', DistrictDetailView.as_view(), name="detail-district"),
	path('base/district/<int:pk>/update', DistrictUpdateView.as_view(), name="update-district"),

	path('base/district/<int:district_pk>/create_clan', ClanCreateView.as_view(), name="create-clan"),
	path('base/clan/<int:pk>/delete', ClanDeleteView.as_view(), name="delete-clan"),
	path('base/clan/<int:pk>/detail', ClanDetailView.as_view(), name="detail-clan"),
	path('base/clan/<int:pk>/update', ClanUpdateView.as_view(), name="update-clan"),

	path('', UserHomeView.as_view(), name='home-user'),
	path('base/user', UserListView.as_view(), name='list-user'),
	path('base/user/profile', UserProfileView.as_view(), name='profile-user'),
	path('base/user/create', UserCreateView.as_view(), name='create-user'),
	path('base/user/<int:pk>/detail', UserDetailView.as_view(), name='detail-user'),
	path('base/user/<int:pk>/update', UserUpdateView.as_view(), name='update-user'),
	path('base/user/<int:pk>/delete', UserDeleteView.as_view(), name='delete-user'),

	path('base/organizer', OrganizerListView.as_view(), name='list-organizer'),
	path('base/organizer/create', OrganizerCreateView.as_view(), name='create-organizer'),
	path('base/organizer/<int:pk>/update', OrganizerUpdateView.as_view(), name='update-organizer'),
	path('base/organizer/<int:pk>/delete', OrganizerDeleteView.as_view(), name='delete-organizer'),
	path('base/organizer/<int:pk>/detail', OrganizerDetailView.as_view(), name='detail-organizer'),

	path('base/camp', CampListView.as_view(), name='list-camp'),
	path('base/camp/create', CampCreateView.as_view(), name='create-camp'),
	path('base/camp/<int:pk>/update', CampUpdateView.as_view(), name='update-camp'),
	path('base/camp/<int:pk>/delete', CampDeleteView.as_view(), name='delete-camp'),
	path('base/camp/<int:pk>/detail', CampDetailView.as_view(), name='detail-camp'),

	path('base/camp/<int:camp_pk>/registrations/<int:pk>/update', RegistrationUpdateView.as_view(), name='update-registration'),
	path('base/camp/<int:camp_pk>/registrations/<int:pk>/delete', RegistrationDeleteView.as_view(), name='delete-registration'),
	path('base/camp/<int:camp_pk>/registrations/<int:pk>/detail', RegistrationDetailView.as_view(), name='detail-registration'),
	path('base/camp/<int:camp_pk>/registrations/<int:pk>/checkin/step1', RegestrationCheckinStep1View.as_view(), name='checkin-registration-step1'),
	path('base/camp/<int:camp_pk>/registrations/<int:pk>/checkin/step2', RegestrationCheckinStep2View.as_view(), name='checkin-registration-step2'),
	path('base/camp/<int:camp_pk>/registrations/<int:pk>/checkin/step3', RegestrationCheckinStep3View.as_view(), name='checkin-registration-step3'),
	path('base/camp/<int:camp_pk>/registrations/<int:pk>/workshop/add', WorkshopCreateView.as_view(), name='create-workshop'),
	path('base/camp/<int:camp_pk>/registrations/<int:registration_pk>/workshops/<int:pk>/update', WorkshopUpdateView.as_view(), name='update-workshop'),
	path('base/camp/<int:camp_pk>/registrations/<int:registration_pk>/workshops/<int:pk>/delete', WorkshopDeleteView.as_view(), name='delete-workshop'),
	path('base/camp/<int:camp_pk>/registrations/participants', ParticipantCheckInListView.as_view(), name='list-checkin-participants'),
	path('base/camp/<int:camp_pk>/registrations/<int:pk>/checkin-participants', ParticipantCheckInView.as_view(), name='checkin-participant'),
	path('base/camp/<int:camp_pk>/workshops', WorkshopListView.as_view(), name='list-workshop'),
	path('base/camp/<int:camp_pk>/workshops/annotate', WorkshopAnnotateView.as_view(), name='annotate-workshop'),
	path('base/camp/<int:camp_pk>/workshops/print', WorkshopPrintView.as_view(), name='print-workshop'),
	path('base/camp/<int:camp_pk>/workshops/print/lists', WorkshopPrintBatchListView.as_view(), name='list-workshopprints'),
	path('base/camp/<int:camp_pk>/workshops/print/<int:batch_pk>/download', WorkshopPrintBatchDownloadView.as_view(), name='download-workshopprint'),
	path('base/camp/<int:camp_pk>/registrations', RegistrationListView.as_view(), name='list-registration'),
	path('base/camp/<int:camp_pk>/registrations/create', RegistrationCreateView.as_view(), name='create-registration'),


	path('base/camp/<int:camp_pk>/fee/create', FeeCreateView.as_view(), name='create-fee'),
	path('base/fee/<int:pk>/update', FeeUpdateView.as_view(), name='update-fee'),
	path('base/fee/<int:pk>/delete', FeeDeleteView.as_view(), name='delete-fee'),
]
