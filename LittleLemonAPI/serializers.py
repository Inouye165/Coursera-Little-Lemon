from rest_framework import serializers
from decimal import Decimal
from .models import MenuItem
from .models import Category
from rest_framework.validators import UniqueValidator


        
# class MenuItemSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     price = serializers.DecimalField(max_digits=6 , decimal_places=2)
#     inventory = serializers.IntegerField()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','slug','title']

class MenuItemSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name = 'calculate_tax')
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, min_value=2)
    # def validate_price(self, value):
    #     if (value < 2):
    #         raise serializers.ValidationError('Price should not be less than 2.0')

    # def validate_stock(self, value):
    #     if (value < 0):
    #         raise serializers.ValidationError('Stock cannot be negative')
    def validate(self, attrs):
        if(attrs['price']<2):
            raise serializers.ValidationError('Price should not be less than 2.0')
        if(attrs['inventory']<0):
            raise serializers.ValidationError('Stock cannot be negative')
        return super().validate(attrs)
    title = serializers.CharField(max_length=255,validators=[UniqueValidator(queryset=MenuItem.objects.all())])
    class Meta:
        model = MenuItem
        fields = ['id','title','price','stock', 'price_after_tax','category','category_id']
        extra_kwargs = {'price': {'min_value': 2},'stock':{'source':'inventory', 'min_value': 0}}
        
    def calculate_tax(self,product:MenuItem):
        tax_calculated =  product.price * Decimal(1.1)
        return round(tax_calculated, 2)
 
    # def calculate_tax(self, product:MenuItem):
    #     return product.price * Decimal(1.1)
    
#  Second method   as instructed in 'Week 2: Other types of serializers in DRF'
# from .models import Category
# class MenuItemSerializer(serializers.ModelSerializer):
#     stock = serializers.IntegerField(source='inventory')
#     price_after_tax = serializers.SerializerMethodField(method_name = 'calculate_tax')
#     category = serializers.HyperlinkedRelatedField(
#         queryset = Category.objects.all(),
#         view_name='category-detail'
#     )
#     class Meta:
#         model = MenuItem
#         fields = ['id','title','price','stock', 'price_after_tax','category']
#     def calculate_tax(self, product:MenuItem):
#         return product.price * Decimal(1.1)
#First method
# class MenuItemSerializer(serializers.ModelSerializer):
#     stock = serializers.IntegerField(source='inventory')
#     price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
#     #category = CategorySerializer()
#     class Meta:
#         model = MenuItem
#         fields = ['id','title','price','stock','price_after_tax','category']
#         depth = 1
#     def calculate_tax(self,product:MenuItem):
#         return product.price*Decimal(1.1)