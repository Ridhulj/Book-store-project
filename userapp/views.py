import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from bookapp.models import Book, Author
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q

from userapp.models import Cart, CartItem


# Create your views here.
def listUserBook(request):
    books=Book.objects.all().order_by('title')
    paginator= Paginator(books,4)
    page_number=request.GET.get('page')
    try:
        page=paginator.get_page(page_number)
    except EmptyPage:
        page=paginator.page(page_number.num_pages)

    return render(request,'user/userbook_list.html',{'books':books,'page':page})

def userdetailsView(request,book_id):
    book=Book.objects.get(id=book_id)
    return render(request,'user/userdetails_view.html',{'book':book})

def userSearch_Book(request):
    query = request.GET.get('q', None)  # Get the query parameter
    books = []

    if query:
        # Filter books based on the query, checking if the title contains the query
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__name__icontains=query)) # Case-insensitive search

    context = {
        'books': books,
        'query': query
    }

    return render(request, 'user/user_search.html', context)





def add_to_cart(request, book_id):
    book = Book.objects.get(id=book_id)

    if book.quantity > 0:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, book=book)

        if not item_created:
            cart_item.quantity += 1
            cart_item.save()

    return redirect('viewcart')


# View Cart
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    cart_item = CartItem.objects.all()
    total_price = sum(item.book.price * item.quantity for item in cart_items)
    total_items = cart_items.count()

    context = {
        'cart_items': cart_items,
        'cart_item' : cart_item,
        'total_price': total_price,
        'total_items': total_items
    }

    return render(request, 'user/cart.html', context)


# Increase Quantity
def increase_quantity(request, item_id):
    cart_item = CartItem.objects.get (id=item_id)

    if cart_item.quantity < cart_item.book.quantity:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('viewcart')


# Decrease Quantity
def decrease_quantity(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()

    return redirect('viewcart')


# Remove from Cart
def remove_from_cart(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id)
        cart_item.delete()
    except cart_item.DoesNotExist:
        pass

    return redirect('viewcart')

def create_checkout_session(request):
    cart_items=CartItem.objects.all()

    if cart_items:
        stripe.api_key=settings.STRIPE_SECRET_KEY

        if request.method=='POST':
            line_items=[]
            for cart_item in cart_items:
                if cart_item.book:
                    line_item={
                        'price_data':{
                            'currency':'INR',
                            'unit_amount':int(cart_item.book.price*100),
                            'product_data':{
                                'name':cart_item.book.title
                            },
                        },
                        'quantity':1
                    }
                    line_items.append(line_item)

            if line_items:
                checkout_session=stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=line_items,
                    mode='payment',
                    success_url=request.build_absolute_uri(reverse('success')),
                    cancel_url=request.build_absolute_uri(reverse('cancel'))
                )

                return redirect(checkout_session.url,code=303)

def success(request):
    cart_items=CartItem.objects.all()

    for cart_item in cart_items:
        product=cart_item.book
        if product.quantity >= cart_item.quantity:
            product.quantity -= cart_item.quantity
            product.save()

    cart_items.delete()

    return render(request,'user/success.html')

def cancel(request):
    return render(request,'user/cancel.html')