from rest_framework.views import APIView
from rest_framework.response import Response
from django.http.response import HttpResponse, JsonResponse
from rest_framework import status
from .models import Roles

# Create your views here.
class RolesAPI(APIView):
    def convert_to_model(self, productsJSON):
        discord = productsJSON['discord']
        tokenId = productsJSON['tokenId']
        
        return Roles(discord=discord, tokenId=tokenId)

    def handle_products(self, product_list):
        Roles.objects.bulk_create(product_list)
    
    def get(self, request, format=None):
        data = Roles.objects.values('id', 'discord', 'tokenId', 'assigned')
        return Response(data)

    def post(self, request, format=None):
        list_of_serialized_products = list(
                map(lambda productJSON: self.convert_to_model(productJSON), request.data.get('products', [])))

        self.handle_products(list_of_serialized_products)
        return Response({'success': True}, status=status.HTTP_201_CREATED)

    def patch(self, request, id):
        product = Roles.objects.get(id=id)
        data = request.data

        product.assigned = data.get('assigned', product.assigned)

        product.save()
        serializer = Roles(product)
        return HttpResponse(status=200)