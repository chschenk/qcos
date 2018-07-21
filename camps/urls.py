from django.urls import path
from .views import CampListView, CampDeleteView, edit_camp, add_camp
urlpatterns = [
	path('', CampListView.as_view(), name="list-camps"),
	path('add/', add_camp, name='add-camp'),
	path('edit/<int:pk>/', edit_camp, name='edit-camp'),
	path('delete/<int:pk>/', CampDeleteView.as_view(), name='delete-camp'),
]