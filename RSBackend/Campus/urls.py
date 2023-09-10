from django.urls.conf import path
from Campus import views

urlpatterns = [
    path('campus/', views.AllCampusList.as_view()),
    path('building/', views.BuildingsByCondition.as_view())
]