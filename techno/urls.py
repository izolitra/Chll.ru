from django.contrib.auth.views import LoginView
from django.urls import path
from . import views


urlpatterns = [
    path("", views.ProductViewAll.as_view(),
         name='category_list_start'),
    path('form/', views.contact_form, name='contact_form'),
    path('search/', views.SearchResultsView.as_view(),
         name='search_results'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('contacts/', views.contacts),
    path('<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail_path'),
    path('brand/<slug:brand_n>/', views.BrandCategoryDetailView.as_view(), name='brand_category_list'),
    path('<slug:category_n>/<slug:brand_n>/<slug:slug>/', views.ProductBrandCategoryDetailView.as_view(), name='product_detail_brand'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

]
