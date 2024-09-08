from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404
from django.shortcuts import redirect
from django.urls import reverse

def custom_page_not_found_view(request, exception):
    return redirect(f"{reverse('user:login_view')}?next={request.path}")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.recipes.urls', namespace='recipes')),
    path('user/', include('apps.user.urls', namespace='user')),
]

handler404 = custom_page_not_found_view