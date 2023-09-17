from django.urls import path
from .views import RestaurantCreateView, RestaurantUpdateDeleteView, BranchCreateView, BranchUpdateDeleteView, \
    MenuCategoryCreateView, MenuCategoryUpdateDeleteView, ProductCreateView, ProductUpdateDeleteView, test_view, get_progress


urlpatterns = [
    path('', RestaurantCreateView.as_view(), name='restaurant_create'),
    path('<int:restaurant_id>/', RestaurantUpdateDeleteView.as_view(), name='restaurant_update_delete'),
    path('<int:restaurant_id>/branch', BranchCreateView.as_view(), name='branch_create'),
    path('branch/<int:branch_id>', BranchUpdateDeleteView.as_view(), name='branch_update_delete'),
    path('<int:restaurant_id>/menu_category', MenuCategoryCreateView.as_view(), name='menu_category_create'),
    path('menu_category/<int:menu_category_id>', MenuCategoryUpdateDeleteView.as_view(), name='menu_category_update_delete'),
    path('menu_category/<int:menu_category_id>/product', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:product_id>', ProductUpdateDeleteView.as_view(), name='product_update_delete'),
    path('test_url', test_view, name='test_view'),
    path('get_progress', get_progress, name='get_progress'),
]
