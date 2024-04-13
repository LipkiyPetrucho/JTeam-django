from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .cart import Cart
from .forms import CartAddProductForm
from location.models import Place


@require_POST
def cart_add(request, place_id):
    cart = Cart(request)
    place = get_object_or_404(Place, id=place_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(place=place,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, place_id):
    cart = Cart(request)
    place = get_object_or_404(Place, id=place_id)
    cart.remove(place)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})
