from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, throttle_classes
from .models import MenuItem
from .serializers import MenuItemSerializer
from rest_framework import status
#from rest_framework import generics

from rest_framework.request import Request 
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.throttling  import AnonRateThrottle, UserRateThrottle
from .throttles import TenCallsPerMinute



# class SingleItemMenuView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer
    
#     # The two methods below are added to make the single item view work with HyperlinkedRelatedField.  Instructions from Gemini

#     def get_object(self):
#          obj = super().get_object()
#          return obj

#     def retrieve(self, request: Request, *args, **kwargs):
#          instance = self.get_object()
#          serializer = self.get_serializer(instance, context={'request': request})
#          return Response(serializer.data)
    
@api_view(['GET','POST'])
def MenuItems(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        if category_name:
            items = items.filter(category__title__exact=category_name)
        if to_price:
            items = items.filter(price=to_price)
        if search:
            items = items.filter(title__startswith=search)
        if ordering:
            odering_fields = ordering.split(',')
            items = items.order_by(*odering_fields)
        serialized_item = MenuItemSerializer(items, many=True)
        

        return Response(serialized_item.data)
    if request.method == 'POST':
        serialized_item = MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_201_CREATED)
    
        

@api_view()
def single_item(request, id):
    item = get_object_or_404(MenuItem,pk=id)
    serialized_item = MenuItemSerializer(item, context={'request': request})
    return Response(serialized_item.data)
    
from .models import Category 
from .serializers import CategorySerializer
@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category,pk=pk)
    serialized_category = CategorySerializer(category)
    return Response(serialized_category.data)    
 
 # Lesson on tokens 2-26-2024 1203
 
@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message":"Some secret message"})
 
@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({"message":"Only a manager should see this"})
    else:
        return Response({"message":"You are not authorized"}, 403)

@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({'message':'Successful'})


@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMinute])
def throttle_check_auth(request):
    return Response({'message':'Message for logged in users only'})

from rest_framework.response import Response 
from rest_framework import viewsets 
from .models import MenuItem 
from .serializers import MenuItemSerializer
class MenuItemsViewSet(viewsets.ModelViewSet):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    def get_throttles(self):
        if self.action == 'create':
            throttle_classes = [UserRateThrottle]
        else:
            throttle_classes = [AnonRateThrottle]
        return [throttle() for throttle in throttle_classes]