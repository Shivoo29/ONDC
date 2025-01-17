from django.shortcuts import render
from . models import Catalogue, MasterCatalogue, Categories
from . serializers import CatalogueSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


# to get catalogue of logged in user
class GetCatalogues(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        all_catalogues = Catalogue.objects.filter(seller=request.user)
        data = []

        for catalogue in all_catalogues:
            if catalogue.mapped_to_master:
                category = catalogue.category
                corresponding_master_catalogue = MasterCatalogue.objects.filter(category=category).first()

                if corresponding_master_catalogue:
                    # Use master catalogue images
                    catalogue.product_image_1 = corresponding_master_catalogue.product_image_1
                    catalogue.product_image_2 = corresponding_master_catalogue.product_image_2
                    catalogue.product_image_3 = corresponding_master_catalogue.product_image_3
                    catalogue.product_image_4 = corresponding_master_catalogue.product_image_4
                    catalogue.product_image_5 = corresponding_master_catalogue.product_image_5

            serializer = CatalogueSerializer(catalogue)
            data.append(serializer.data)

        return Response(data, status=status.HTTP_200_OK)
    
class CreateCatalogue(APIView):
    
    permission_classes = (IsAuthenticated, )
    
    def post(self, request): 
        
        final_data = {
            'product_name' : request.data.get('product_name'),
            'mrp' : request.data.get('mrp'),
            'seller' : request.user.pk,
            'selling_prize' : request.data.get('selling_prize'),
            'buying_prize' : request.data.get('buying_prize'),
            'hsn_code' : request.data.get('hsn_code'),
            'gst_percentage' : request.data.get('gst_percentage'),
            'unit' : request.data.get('unit'),
            'quantity' : request.data.get('quantity'),
            'standardized' : request.data.get('standardized'),
            'category' : Categories.objects.get_or_create(category=request.data.get('category'))[0].pk,
            'mapped_to_master' : request.data.get('mapped_to_master'),
            'product_image_1' : request.data.get('product_image_1'),
            'product_image_2' : request.data.get('product_image_2'),
            'product_image_3' : request.data.get('product_image_3'),
            'product_image_4' : request.data.get('product_image_4'),
            'product_image_5' : request.data.get('product_image_5'),
        }

        catalogue_serializer = CatalogueSerializer(data=final_data)

        if catalogue_serializer.is_valid():
            catalogue_serializer.save()
            return Response({'message': 'Catalogue Saved Successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(catalogue_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# to get all catalogues even without loggin in    
class GetAllCatalogues(APIView):
    def get(self, request):
        all_catalogues = Catalogue.objects.all()
        data = []

        for catalogue in all_catalogues:
            if catalogue.mapped_to_master:
                category = catalogue.category
                corresponding_master_catalogue = MasterCatalogue.objects.filter(category=category).first()

                if corresponding_master_catalogue:
                    # Use master catalogue images
                    catalogue.product_image_1 = corresponding_master_catalogue.product_image_1
                    catalogue.product_image_2 = corresponding_master_catalogue.product_image_2
                    catalogue.product_image_3 = corresponding_master_catalogue.product_image_3
                    catalogue.product_image_4 = corresponding_master_catalogue.product_image_4
                    catalogue.product_image_5 = corresponding_master_catalogue.product_image_5

            serializer = CatalogueSerializer(catalogue)
            data.append(serializer.data)

        return Response(data, status=status.HTTP_200_OK)
        