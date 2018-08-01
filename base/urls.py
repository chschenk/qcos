from django.urls import path
from .views import DioceseCreate, DioceseDelete, DioceseDetail, DioceseList, DioceseUpdate
from .views import DistrictCreate, DistrictDelete, DistrictDetail, DistrictUpdate
from .views import ClanCreate, ClanDelete, ClanUpdate

app_name = "base"
urlpatterns = [
	path('', DioceseList.as_view(), name="list-dioceses"),
	path('diocese/', DioceseList.as_view(), name="list-dioceses"),
	path('diocese/add/', DioceseCreate.as_view(), name="add-diocese"),
	path('diocese/edit/<int:pk>/', DioceseUpdate.as_view(), name="edit-diocese"),
	path('diocese/delete/<int:pk>/', DioceseDelete.as_view(), name="delete-diocese"),
	path('diocese/view/<int:pk>/', DioceseDetail.as_view(), name="view-diocese"),

	path('diocese/view/<int:pk>/add/', DistrictCreate.as_view(), name="add-district"),
	path('district/edit/<int:pk>/', DistrictUpdate.as_view(), name="edit-district"),
	path('district/delete/<int:pk>/', DistrictDelete.as_view(), name="delete-district"),
	path('district/view/<int:pk>/', DistrictDetail.as_view(), name="view-district"),

	path('district/view/<int:pk>/add/', ClanCreate.as_view(), name="add-clan"),
	path('clan/edit/<int:pk>/', ClanUpdate.as_view(), name="edit-clan"),
	path('clan/delete/<int:pk>/', ClanDelete.as_view(), name="delete-clan"),
]