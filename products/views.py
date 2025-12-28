from django.shortcuts import render
from .serializers import ProductSerializer, ProductCreateUpdateSerializer
from .models import Product
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes


@api_view(['GET'])
@permission_classes([AllowAny])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    filtered = [
        {
            'product_image': item.get('product_image'),
            'name': item.get('name'),
            'stock_quantity': item.get('stock_quantity'),
            'price': item.get('price'),
            'discounted_price': item.get('discounted_price'),
            'product_ref': item.get('product_ref'),
        }
        for item in serializer.data
    ]
    return Response({'products': filtered})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def product_create(request):
    serializer = ProductCreateUpdateSerializer(data=request.data)
    if serializer.is_valid():
        product = serializer.save()
        return Response(ProductSerializer(product).data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([AllowAny])
def product_detail(request, product_ref):
    try:
        product = Product.objects.get(product_ref=product_ref)
        related_products = Product.objects.filter(category=product.category).exclude(id=product.id)

    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)

    serializer = ProductSerializer(product)
    product_data = ProductSerializer(product).data
    return Response({
        'product': product_data,
        'related_products': ProductSerializer(related_products, many=True).data
    })


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def product_update(request, product_ref):
    try:
        product = Product.objects.get(product_ref=product_ref)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)

    serializer = ProductCreateUpdateSerializer(product, data=request.data, partial=True)
    if serializer.is_valid():
        product = serializer.save()
        return Response(ProductSerializer(product).data)
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def product_delete(request, product_ref):
    try:
        product = Product.objects.get(product_ref=product_ref)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)

    product.delete()
    return Response(status=204)

