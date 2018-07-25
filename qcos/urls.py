from django.contrib import admin
from django.urls import path, include

urlpatterns = [
	path('admin/', admin.site.urls),
	path('camps/', include('camps.urls', 'camps')),
	path('registration/', include('registration.urls', 'registration')),
	path('base/', include('base.urls', 'base')),
	path('api/', include('api.urls', 'api')),
]
