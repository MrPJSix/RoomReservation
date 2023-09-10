from django.urls.conf import path
from Student import views

urlpatterns = [
    path('studyroom/', views.RoomsByCondition.as_view()),
    path('studyroom/seatstatus/', views.SeatsStatusList.as_view()),
    path('studyroom/booking', views.ReservationBook.as_view()),
    path('reservations/cancel', views.ReservationCancel.as_view()),
    path('reservations/info', views.ReservationAll.as_view()),
    path('reservations/invalid', views.ReservationInvalid.as_view()),
    path('reservations/sign', views.SignIn.as_view())
]