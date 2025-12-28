from django.shortcuts import render
from products.models import Product
from .models import Cart, CartItem, RequestQuote
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from dashboard.serializers import RequestQuoteSerializer, CartSerializer
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_quotes(request):
    quotes = RequestQuote.objects.filter(user=request.user).order_by('-created_at')
    serializer = RequestQuoteSerializer(quotes, many=True)
    return Response({'quotes': serializer.data}, status=status.HTTP_200_OK)

# Cart endpoints

def _get_user_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart_detail(request):
    cart = _get_user_cart(request.user)
    return Response(CartSerializer(cart).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cart_add_item(request):
    product_ref = request.data.get('product_ref')
    quantity = int(request.data.get('quantity', 1) or 1)

    if not product_ref:
        return Response({'error': 'product_ref is required'}, status=400)
    if quantity < 1:
        return Response({'error': 'quantity must be >= 1'}, status=400)

    try:
        product = Product.objects.get(product_ref=product_ref)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)

    cart = _get_user_cart(request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': quantity})
    if not created:
        item.quantity += quantity
        item.save()

    return Response(CartSerializer(cart).data, status=201)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def cart_update_item(request, item_id: int):
    cart = _get_user_cart(request.user)
    try:
        item = cart.items.get(id=item_id)
    except CartItem.DoesNotExist:
        return Response({'error': 'Cart item not found'}, status=404)

    quantity = request.data.get('quantity')
    if quantity is None:
        return Response({'error': 'quantity is required'}, status=400)
    try:
        quantity = int(quantity)
    except ValueError:
        return Response({'error': 'quantity must be an integer'}, status=400)

    if quantity <= 0:
        item.delete()
    else:
        item.quantity = quantity
        item.save()

    return Response(CartSerializer(cart).data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cart_delete_item(request, item_id: int):
    cart = _get_user_cart(request.user)
    deleted = cart.items.filter(id=item_id).delete()[0]
    if deleted == 0:
        return Response({'error': 'Cart item not found'}, status=404)
    return Response(CartSerializer(cart).data)