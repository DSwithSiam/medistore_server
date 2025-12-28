from django.shortcuts import render
from products.models import Product
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from dashboard.serializers import RequestQuoteSerializer
from products.serializers import ProductSerializer
# Create your views here.


from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_home(request):
    def project(items):
        return [
            {
                'product_image': item['product_image'],
                'name': item['name'],
                'stock_quantity': item['stock_quantity'],
                'price': item['price'],
                'discounted_price': item['discounted_price'],
                'discount': item.get('discount', 0),
                'product_ref': item['product_ref'],
            }
            for item in items
        ]

    discounted_qs = Product.objects.filter(discount__gt=0).order_by('-discount')[:8]
    latest_qs = Product.objects.order_by('-created_at')[:8]

    discounted_data = ProductSerializer(discounted_qs, many=True).data
    latest_data = ProductSerializer(latest_qs, many=True).data

    return Response({
        "discounted_products": project(discounted_data),
        "latest_products": project(latest_data),
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def filter_products(request, category):
    products = Product.objects.filter(category=category)
    serializer = ProductSerializer(products, many=True)
    filtered = [
        {
            'product_image': item.get('product_image'),
            'name': item.get('name'),
            'stock_quantity': item.get('stock_quantity'),
            'price': item.get('price'),
            'discounted_price': item.get('discounted_price'),
            'discount': item.get('discount', 0),
            'product_ref': item.get('product_ref'),
        }
        for item in serializer.data
    ]
    return Response({'products': filtered})


@api_view(['POST'])
@permission_classes([AllowAny])
def search_products(request):
    query = request.data.get('query', '')
    category=request.data.get('category', None)
    if category:
        products = Product.objects.filter(name__icontains=query, category=category)
    else:
        products = Product.objects.filter(name__icontains=query)
    serializer = ProductSerializer(products, many=True)
    filtered = [
        {
            'product_image': item.get('product_image'),
            'name': item.get('name'),
            'stock_quantity': item.get('stock_quantity'),
            'price': item.get('price'),
            'discounted_price': item.get('discounted_price'),
            'discount': item.get('discount', 0),
            'product_ref': item.get('product_ref'),
        }
        for item in serializer.data
    ]
    return Response({'products': filtered})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_quote(request):
    serializer = RequestQuoteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Quote request submitted successfully',
            'request_quote': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)