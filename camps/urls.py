from django.urls import path
from .views import CampListView, CampCreateView, CampUpdateView, CampDeleteView, edit_camp, add_camp
urlpatterns = [
    path('', CampListView.as_view(), name="list-camps"),
	path('add/', add_camp, name='add-camp'),
	path('edit/<int:pk>/', edit_camp, name='edit-camp'),
	path('delte/<int:pk>/', CampDeleteView.as_view(), name='delete-camp'),
	#path('fee/<int:pk>/add/', FeeCreateView.as_view(), name='add-fee')
]