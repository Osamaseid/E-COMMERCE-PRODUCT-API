from django.urls import path
from . import views

urlpatterns = [
    # Category URLs
    path('categories/', views.getCategories, name='get_categories'),
    path('categories/<int:pk>/', views.categoryDetail, name='category_detail'),
    path('categories/create/', views.createCategory, name='create_category'),

    # Product URLs
    path('products/', views.getProducts, name='get_products'),
    path('products/<int:pk>/', views.productDetail, name='product_detail'),
    path('products/create/', views.createProduct, name='create_product'),

    # Review URLs
    path('reviews/', views.getReviews, name='get_reviews'),
    path('reviews/<int:pk>/', views.reviewDetail, name='review_detail'),
    path('reviews/create/', views.createReview, name='create_review'),

    # Order URLs
    path('orders/', views.getOrders, name='get_orders'),
    path('orders/<int:pk>/', views.orderDetail, name='order_detail'),
    path('orders/create/', views.createOrder, name='create_order'),

    # User URLs
    path('users/', views.getUsers, name='get_users'),
    path('users/<int:pk>/', views.userDetail, name='user_detail'),
    path('users/create/', views.createUser, name='create_user'),
]
