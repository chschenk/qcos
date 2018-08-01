from django.urls import path
from .views import CampListView, CampDeleteView, CampAddView, CampEditView

app_name = 'camps'
urlpatterns = [
	path('', CampListView.as_view(), name="list-camps"),
	path('add/', CampAddView.as_view(), name='add-camp'),
	path('edit/<int:pk>/', CampEditView.as_view(), name='edit-camp'),
	path('delete/<int:pk>/', CampDeleteView.as_view(), name='delete-camp'),
]