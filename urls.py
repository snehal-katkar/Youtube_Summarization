#from django.urls import path
#from .views import test_view

#urlpatterns = [
 #   path('test/', test_view),
#]


# summarizer/urls.py
#from django.urls import path
#from . import views

#urlpatterns = [
 #   path('summarize/', views.summarize_video),
#]
# summary_api/urls.py

from django.urls import path
from .views import summarize_view

urlpatterns = [
    path('summarize/', summarize_view),
]




