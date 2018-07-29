from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('admin/', admin.site.urls),
	path('camps/', include('camps.urls')),
	path('', RedirectView.as_view(pattern_name='camp_registration:list-camps')),
	path('registration/', include('camp_registration.urls')),
	path('base/', include('base.urls')),
	path('api/', include('api.urls')),
	path('accounts/', include('django.contrib.auth.urls')),
	path('login/', auth_views.login, name='login'),
	path('logout/', auth_views.logout, name='logout'),
]
