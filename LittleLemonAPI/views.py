from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import MenuItem
from .serializers import MenuItemSerializer
from rest_framework import status
from rest_framework import generics

# class MenuItemsView(generics.ListCreateAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer

from rest_framework.request import Request 
class SingleItemMenuView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    # The two methods below are added to make the single item view work with HyperlinkedRelatedField.  Instructions from Gemini

    def get_object(self):
         obj = super().get_object()
         return obj

    def retrieve(self, request: Request, *args, **kwargs):
         instance = self.get_object()
         serializer = self.get_serializer(instance, context={'request': request})
         return Response(serializer.data)
    
@api_view(['GET','POST'])
def MenuItems(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        serialized_item = MenuItemSerializer(items, many=True)
        return Response(serialized_item.data)
    if request.method == 'POST':
        serialized_item = MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_201_CREATED)
    
        
# @api_view()
# def single_item(request, id):
#      item = get_object_or_404(MenuItem, pk=id)
#      serializer = MenuItemSerializer(item, context={'request': request}) 
#      return Response(serializer.data) 

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
 
# @api_view(['GET', 'POST'])
# def menu_items(request):
#     if request.method == 'GET':
#         items = MenuItem.objects.all()
#         serialized_item = MenuItemSerializer(items, many=True)
#         return Response(serialized_item.data)  # Corrected to serialized_item.data
    
#     # elif request.method == 'POST':
#     #     serialized_item = MenuItemSerializer(data=request.data)
#     #     if serialized_item.is_valid(raise_exception=True):
#     #         serialized_item.save()
#     #         return Response(serialized_item.data, status=status.HTTP_201_CREATED)
#     if request.method == 'POST':
#         serialized_item = MenuItemSerializer(data=request.data)
#         serialized_item.is_valid(raise_exception=True)
#         serialized_item.save()
#         return Response(serialized_item.data, status=status.HTTP_201_CREATED)

# @api_view()
# def single_item(request, id):
#     item = get_object_or_404(MenuItem,pk=id)
#     serialize_item = MenuItemSerializer(item)
#     return Response(serialize_item.data)  

