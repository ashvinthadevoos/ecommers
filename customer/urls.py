from django.urls import path
from customer import views
urlpatterns=[
    path('signup/',views.SignUpView.as_view(),name='signup'),
    path('',views.LoginView.as_view(),name='signin'),
    path('index/',views.IndexView.as_view(),name='index'),
    path('products/<int:id>',views.ProductDetailView.as_view(),name='product-detail'),
    path('products/<int:id>/cart/add',views.AddToCartView.as_view(),name='cart-add'),
    path('cart/',views.MyCartView.as_view(),name='cart-list'),
    path('cancel/<int:id>',views.CartRemoveView.as_view(),name='cart-remove'),
    path('placeorder/<int:id>',views.MakeOrderView.as_view(),name='placeorder'),
    path('orders/',views.MyOrdersView.as_view(),name='orders'),
    path('order/cancel/<int:id>',views.OrderCancelView.as_view(),name='order-cancel'),
    path('offers/',views.DiscountProductView.as_view(),name='offers'),
    path('review/add/<int:id>',views.ReviewAddView.as_view(),name='review-add'),
    path('signout/',views.signout_view,name='signout')
]