from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from product.models import Product, Review
from .serializers import ProductSerializer, ReviewsSerializer, ProductCreateSerializer, ProductUpdateSerializer, \
    ReviewSerializers
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


@api_view(["GET"])
def product_all(request):
    products = Product.objects.all()
    data = ProductSerializer(products, many=True).data
    return Response(data=data)


@api_view(["GET"])
def product_object(request, id):
    products = Product.objects.get(id=id)
    data = ProductSerializer(products, many=False).data
    return Response(data=data)


@api_view(["GET"])
def product_list_reviews(request):
    review = Product.objects.all()
    data = ReviewsSerializer(review, many=True).data

    return Response(data=data)


@api_view(["PUT", "DELETE"])
def products_view(request, id):
    product = Product.objects.get(id=id)

    if request.method == "PUT":
        serializer = ProductUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={"Massage": "ERROR",

                                  "errors": serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)
        print(request.data)
        product.title = request.data["title"]
        product.description = request.data["description"]
        product.price = request.data["price"]
        product.category_id = request.data["category_id"]
        product.tags.clear()
        for i in request.data["tags"]:
            product.tags.add(i)
        product.save()
        return Response(data={"massage": "product update"})
    elif request.method == "DELETE":
        product.delete()
        return Response(data={"massage": "destroyed"})


@api_view(["POST"])
def products_post_view(request):
    if request.method == "POST":
        serializer = ProductCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={"Massage": "ERROR",
                                  "errors": serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)
        print(request.data)
        product = Product.objects.create(
            title=request.data["title"],
            description=request.data["description"],
            price=request.data["price"],
            category_id=request.data["category_id"]
        )
        for i in request.data["tags"]:
            product.tags.add(i)
            product.save()
        return Response(data={"massage": "ok"})


@api_view(["POST", "GET"])
@permission_classes([IsAuthenticated])
def reviews_view(request):
    if request.method == "POST":
        Review.objects.create(
            text=request.data["text"],
            product_id=request.data["product_id"],
            author=request.user
        )
        return Response(data={"massage": "OK"})
    elif request.method == "GET":
        reviews = Review.objects.filter(author=request.user)
        return Response(data=ReviewSerializers(reviews, many=True).data)


@api_view(["POST"])
def login(request):
    username = request.data["username"]
    password = request.data["password"]
    user = authenticate(username=username, password=password)
    if user:
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
        return Response(data={"key": token.key})
    else:
        return Response(data={"ERROR": "ПОЛЬЗОВАТЕЛЬ НЕ НАЙДЕН"})
