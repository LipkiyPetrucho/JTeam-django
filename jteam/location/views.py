from django.shortcuts import get_object_or_404, render

from .models import City, Place
from cart.forms import CartAddProductForm


def place_list(request, city_slug=None):
    city = None
    cities = City.objects.all()
    places = Place.objects.filter(available=True)
    if city_slug:
        city = get_object_or_404(City,
                                 slug=city_slug)
        places = places.filter(city=city)
    return render(request,
                  'place/list.html',
                  {'city': city,
                   'cities': cities,
                   'places': places})

def place_detail(request, id, slug):
    place = get_object_or_404(Place,
                              id=id,
                              slug=slug,
                              available=True)
    cart_place_form = CartAddProductForm()
    return render(request,
                  'place/detail.html',
                  {'place': place,
                   'cart_place_form': cart_place_form})
