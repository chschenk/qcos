from django.contrib import admin
from django.urls import path, include

urlpatterns = [
	path('admin/', admin.site.urls),
	path('camps/', include('camps.urls')),
	path('registration/', include('camp_registration.urls')),
	path('base/', include('base.urls')),
	path('api/', include('api.urls')),
	path('accounts/', include('django.contrib.auth.urls')),
]
