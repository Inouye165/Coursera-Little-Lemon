from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    # path('menu-items/',views.MenuItemsView.as_view()),
    # path('menu-items/',views.MenuItems),
    # path('menu-items/<int:id>', views.single_item),
    path('category/<int:pk>',views.category_detail, name='category-detail'),
    # path('menu-items/<int:id>',views.single_item),
    path('secret/',views.secret),
    path('manager-view/',views.manager_view),
    path('api-token-auth',obtain_auth_token),
    path('throttle-check',views.throttle_check),
    path('throttle-check-auth',views.throttle_check_auth),
    
    # these are the endpoints from Week 3 API throttling for class-based views. 
    # menu-items endpoints above are commented out to avoid conflicts
    path('menu-items',views.MenuItemsViewSet.as_view({'get':'list', 'post':'create'})),
    path('menu-items/<int:pk>',views.MenuItemsViewSet.as_view({'get':'retrieve'})),   
    path('groups/manager/users/',views.managers),
    
]