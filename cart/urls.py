from django.urls import path
import cart.views

urlpatterns = [
    path('add_to_cart/<book_id>', cart.views.add_to_cart, name="add_to_cart_route"),
    path('view_cart', cart.views.view_cart, name="view_cart_route"),
    path('remove_from_cart/<book_id>', cart.views.remove_from_cart, name='remove_from_cart_route'),
    path('update_quantity/<book_id>', cart.views.update_quantity, name='update_cart_quantity_route')
]
