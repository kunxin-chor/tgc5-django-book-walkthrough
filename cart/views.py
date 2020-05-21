from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponseForbidden
from books.models import Book
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

SHOPPING_CART = "shopping_cart"

def group_required(arg_name):
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            group_id = kwargs.get(arg_name)
            user = request.user
            if group_id in user.groups.values_list('id', flat=True):
                return view(request, *args, **kwargs)
            else:
                messages.error(request, "You are not a customer")
                return redirect(reverse('view_books_route'))
        return wrapper
    return decorator

# Create your views here.
@group_required('customer')
def add_to_cart(request, book_id):

    # if not request.user.groups.filter(name='customer').exists():
    #     messages.error(request, "You are not a customer")
    #     return redirect(reverse('view_books_route'))

    # open a file identified by the key 'shopping_cart' in the session (first argument)
    # if 'shopping_cart' is not found in the session, return an empty dictionary (second argument) 
    cart = request.session.get(SHOPPING_CART, {})

    book = get_object_or_404(Book, pk=book_id)

    # CASE ONE: The book that the user is adding is not in the shopping cart yet
    if book_id not in cart:

        cart[book_id] = {
            'id': book_id,
            'title': book.title,
            'cost': float(book.cost),
            'qty': 1
        }
        messages.success(request, f"Book: {book.title} has been added to your cart")

    # CASE TWO: the book that the user is adding is ALREADY in the shopping cart
    else:
        cart[book_id]['qty'] += 1
        messages.success(request, f"One more book: {book.title} has been added to your cart")

    # REMEMEBR to save back to the session
    request.session[SHOPPING_CART] = cart

    return redirect(reverse('view_books_route'))


def view_cart(request):
    # retrieve the cart from the session
    cart = request.session.get(SHOPPING_CART)
    return render(request, 'cart/view_cart.template.html', {
        'cart': cart
    })


def remove_from_cart(request, book_id):
    cart = request.session.get(SHOPPING_CART)
    if book_id in cart:
        del cart[book_id]
        request.session[SHOPPING_CART] = cart
        messages.success(request, "Item has been removed")

    return redirect(reverse('view_cart_route'))


def update_quantity(request, book_id):
    cart = request.session.get(SHOPPING_CART)
    if book_id in cart:
        cart[book_id]['qty'] = request.POST['qty']  # eqv to Flask: request.form.get
        request.session[SHOPPING_CART] = cart
        messages.success(request, f"Quantity for {cart[book_id]['title']} has been changed")
    
    return redirect(reverse('view_cart_route'))