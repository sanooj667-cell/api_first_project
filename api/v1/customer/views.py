from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from custmor.models import Product, Category
from user.models import CustomUser
from .serializers import *



@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    user = authenticate(request, email=email, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        response_data ={
            "status_code" : 200,
            "status" : "success",
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            "message" : "login sucsessfully."
        }
        return Response(response_data)
    else:
        response_data = {
            "status_code" : 400,
            "status" : "error",
            "message" : "user is not found"
        }
        return Response(response_data)






@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    first_name = request.data.get('first_name')
    last_name = request.data.get("last_name")
    email = request.data.get("email")
    password = request.data.get("password")

    if CustomUser.objects.filter(email=email).exists():
        response_data = {
            "status_code": 400,
            "status": "error",
            "message": "User with this email already exists."
        }
        return Response(response_data)
    else:
        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name 
        )
        user.save()
        response_data ={
            "status_code": 201,
            "status": "success",
            "message": "User registered successfully."
        }
        return Response(response_data)



    




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def categories(request):
    categories = Category.objects.all()
    context = {
            "request" :request
        }

    serializer = CategorySerializer(categories, many=True,context=context)

    response_data = {
        "status_code": 200,
        "data": serializer.data,
        "message": "categories"
    }

    return Response(response_data)


    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_category(request):
    user=request.user
    name = request.data.get("name")
    categorie = Category.objects.create(
        name = name,
        user=user
        
    
    )


    serializer=CategorySerializer(
        categorie,
        context={"request":request}
        )



   

    response_data = {
        "status_code" : 200,
        "data":serializer.data,
        "message" : "created succsesfully"
    }
    return Response(response_data)




# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def add_category(request):
#     user=request.user
#     serializer = CategorySerializer(data=request.data)

#     if serializer.is_valid():
#         serializer.save(user=user) 

#         return Response({
#             "status_code": 201,
#             "data": serializer.data,
#             "message": "Created successfully"
#         })

#     return Response(serializer.errors, status=400)
    

@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def edit_category(request, id):
    user=request.user
    category=Category.objects.get(id=id,user=user)
    name = request.data.get("name")
    category.name = name
    category.save()

    serializer = CategorySerializer(
        category,
        context={"request": request}
    )

    return Response({
        "status_code": 200,
        "status": "success",
        "data": serializer.data,
        "message": "edited successfully"
    })






@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_category(request, id):
    user=request.user
    category=Category.objects.get(id=id,user=user)

    category.delete()

    return Response({
        "status_code": 200,
        "status": "success",
        "data": {},
        "message": "deleted successfully"
    })



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def products(request):
    products = Product.objects.all()
    context = {
        "request"  : request
    }

    serializers = ProductSerializer(products, many=True,context=context)

    Response_data = {
        "status_code" : 200,
        "status" : "sucssus",
        "data" : serializers.data,
    }

    return Response(Response_data)
    

    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_product(request,id):
    user = request.user
    category=Category.objects.get(id=id)
    serializers = ProductSerializer(data=request.data)

    if serializers.is_valid():
        serializers.save(user = user,category=category)
        return Response({
            "status_code" : 200,
            "data" : serializers.data,
            "message" : "add product sucsessfully"
        })
    return Response(serializers.errors,status=400)     


    

@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def edit_product(request, id):
    user =  request.user 
    product = Product.objects.get(id=id, user = user)
    serializer =  ProductSerializer(product,data = request.data, partial = True)

    if serializer.is_valid():
        serializer.save() 
        return Response({
            "status_code":"200",
            "data":serializer.data,
            "message": "product edited sucsessfully"
        })
    return Response(serializer.errors,status=400 )

    
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_product(request, id):
    product = Product.objects.get(id=id, user=request.user)
    product.delete()
    response_data ={
        "status_code" :200,
        "status" : "sucssus",
        "message" : "deleted sucssusfully"

    }
    return Response(response_data)




