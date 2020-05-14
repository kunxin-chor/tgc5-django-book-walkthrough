from django.shortcuts import render, get_object_or_404, reverse, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.models import Site
import stripe
from books.models import Book


# Create your views here.
def checkout(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # generate the session
    # we need:
    # 1. the line items
    # 2. payment meethod
    # 3. which url to go if the payment is successful
    # 4. which url to go if the user cancels the payment

    # generate the line items
    line_items = []

    cart = request.session.get('shopping_cart', {})

    for id, book in cart.items():
        book_from_db = get_object_or_404(Book, pk=id)
        line_item = {
            "name": book_from_db.title,
            "amount": int(book_from_db.cost*100),
            "currency": "sgd",
            "quantity": book['qty']
        }
        line_items.append(line_item)

    # get our current domain
    current_site = Site.objects.get_current()
    domain = current_site.domain

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        success_url=domain + reverse(checkout_success),
        cancel_url=domain + reverse(checkout_cancelled)
    )

    return render(request, 'checkout/checkout.template.html', {
        "session_id": session.id,
        "public_key": settings.STRIPE_PUBLISHABLE_KEY
    })


def checkout_success(request):
    # reset the shopping cart
    request.session['shopping_cart'] = {}
    return HttpResponse("Checkout successful")


def checkout_cancelled(request):
    return HttpResponse("Checkout cancelled")


@csrf_exempt
def handle_payment_completed(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.SIGNING_SECRET
        )
    except ValueError as e:
        # Invalid payload
        print(e)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print(e)
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

    # Fulfill the purchase...
    handle_checkout_session(session)



    return HttpResponse(status=200)


def handle_checkout_session(session):
    print(session)



