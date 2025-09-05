from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from django.shortcuts import redirect

# def home_redirect(request):
#     return redirect("https://swasthgram.netlify.app")



from django.http import JsonResponse

def api_home(request):
    return JsonResponse({"message": "Welcome to SwasthGram API!"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),  
    path('api/', include('hygiene.urls')),
    path('', api_home),  # ⬅️ add this
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)