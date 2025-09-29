from django.urls import path
from .views import (
    EmployeeCreateView, RestaurantCreateView, UploadMenuView,
    TodayMenuView, VoteView, ResultsTodayView, RestaurantListView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('employees/', EmployeeCreateView.as_view(), name='employee_create'),
    path('restaurants/', RestaurantCreateView.as_view(), name='restaurant_create'),
    path('restaurants/<int:pk>/menus/', UploadMenuView.as_view(), name='upload_menu'),
    path('restaurants/list/', RestaurantListView.as_view(), name='restaurant_list'),
    path('menus/today/', TodayMenuView.as_view(), name='today_menus'),
    path('menus/<int:menu_id>/vote/', VoteView.as_view(), name='vote'),
    path('results/today/', ResultsTodayView.as_view(), name='results_today'),
]
