from rest_framework import serializers
from custmor.models import Category,Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category   
        fields = ['id', 'name', ]
        read_only_fields = ['user'] 


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','category','price','description','image'] 