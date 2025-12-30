from django.shortcuts import render
from django.core.paginator import Paginator
from .serializers import ProductSerializer, ProductCreateUpdateSerializer
from .models import Product
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from .schemas import (
    all_products_swagger,
    product_create_swagger,
    product_detail_swagger,
    update_product_swagger,
    delete_product_swagger,
)


@all_products_swagger
@api_view(["GET"])
@permission_classes([AllowAny])
def product_list(request):
    products = Product.objects.all()
    paginator = Paginator(products, 18)
    page_number = request.query_params.get("page", 1)
    try:
        page_obj = paginator.get_page(page_number)
    except Exception:
        page_obj = paginator.get_page(1)

    serializer = ProductSerializer(page_obj.object_list, many=True)
    filtered = [
        {
            "product_image": item.get("product_image"),
            "name": item.get("name"),
            "stock_quantity": item.get("stock_quantity"),
            "price": item.get("price"),
            "discounted_price": item.get("discounted_price"),
            "product_ref": item.get("product_ref"),
        }
        for item in serializer.data
    ]
    return Response(
        {
            "products": filtered,
            "pagination": {
                "page": page_obj.number,
                "per_page": 18,
                "total_pages": paginator.num_pages,
                "total_items": paginator.count,
                "has_next": page_obj.has_next(),
                "has_prev": page_obj.has_previous(),
                "next_page": (
                    page_obj.next_page_number() if page_obj.has_next() else None
                ),
                "prev_page": (
                    page_obj.previous_page_number() if page_obj.has_previous() else None
                ),
            },
        }
    )


@product_create_swagger
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def product_create(request):
    serializer = ProductCreateUpdateSerializer(data=request.data)
    if serializer.is_valid():
        product = serializer.save()
        return Response(ProductSerializer(product).data, status=201)
    return Response(serializer.errors, status=400)


@product_detail_swagger
@api_view(["GET"])
@permission_classes([AllowAny])
def product_detail(request, product_ref):
    try:
        product = Product.objects.get(product_ref=product_ref)
        related_products = Product.objects.filter(category=product.category).exclude(
            id=product.id
        )

    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)

    product_data = ProductSerializer(product, many=False).data
    related_products = ProductSerializer(related_products, many=True).data
    related_products_data = [
        {
            "product_image": item.get("product_image"),
            "name": item.get("name"),
            "stock_quantity": item.get("stock_quantity"),
            "price": item.get("price"),
            "discounted_price": item.get("discounted_price"),
            "product_ref": item.get("product_ref"),
        }
        for item in related_products
    ]
    return Response(
        {
            "product": product_data,
            "related_products": related_products_data,
        }
    )


@update_product_swagger
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def product_update(request, product_ref):
    try:
        product = Product.objects.get(product_ref=product_ref)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)

    serializer = ProductCreateUpdateSerializer(product, data=request.data, partial=True)
    if serializer.is_valid():
        product = serializer.save()
        return Response(ProductSerializer(product).data)
    return Response(serializer.errors, status=400)


@delete_product_swagger
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def product_delete(request, product_ref):
    try:
        product = Product.objects.get(product_ref=product_ref)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)

    product.delete()
    return Response(status=204)
