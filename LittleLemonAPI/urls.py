from django.urls import path
from . import views

urlpatterns = [
    # path('menu-items/',views.MenuItemsView.as_view()),
    path('menu-items/',views.MenuItems),
    path('menu-items/<int:id>', views.single_item),
    path('category/<int:pk>',views.category_detail, name='category-detail'),
    # path('menu-items/<int:id>',views.single_item),
    
]