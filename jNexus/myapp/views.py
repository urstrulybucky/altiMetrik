from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.mixins import ListModelMixin,CreateModelMixin ,RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework import serializers
from .models import Product
from .serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated


class AltiMetrikViewSet(GenericViewSet, ListModelMixin , CreateModelMixin ,RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):

    def initialise_model_name(self):
        # Access the model name from the derived class
        self.model_name = self.model_name
        self.serializer_class = self.serializer_class

    
    def get_serializer_class(self):
        columns = self.request.data.get('columns')
        
        if columns:
            # Dynamic creation of serializer class based on columns
            serializer_class = type('DynamicAddressSerializer', (serializers.ModelSerializer,), {
                'Meta': type('Meta', (), {'model': self.model_name, 'fields': columns})
            })
        else:
            # Use default serializer class if columns are not specified
            serializer_class = self.serializer_class
        
        return serializer_class
    
      
    def filter_queryset(self, queryset):
        # Retrieve filters from request payload
        filters = self.request.data.get('filters', {})
        filter_args = {}

        # Apply type-based validation for filter values
        for filter_item in filters:
            field = filter_item.get('field')
            value = filter_item.get('value')
            field_type = self.model_name._meta.get_field(field).get_internal_type()

            if field_type == 'IntegerField':
                try:
                    value = int(value)
                except ValueError:
                    continue
            elif field_type == 'CharField':
                if not isinstance(value, str):
                    continue
            elif field_type == 'DateField':
                # Add date validation logic if needed
                pass
            elif field_type == 'FloatField':
                try:
                    value = float(value)
                except ValueError:
                    continue
            
            filter_args[f'{field}__exact'] = value

        return queryset.filter(**filter_args)

  
    def get_queryset(self):

        queryset = super().get_queryset()
        # Retrieve columns from request payload
        columns = self.request.data.get('columns', [])
        if columns:
            queryset = queryset.values(*columns)
        
        # Retrieve order_by from request payload
        order_by = self.request.data.get('order_by', {})
        if order_by:
            field = order_by.get('field')
            direction = order_by.get('order', 'asc')
            if direction=='asc':
                queryset = queryset.order_by(f'{field}')
            else:
                queryset = queryset.order_by(f'{"-"+field}')

        # Retrieve select_related and prefetch_related from request payload
        select_related = self.request.data.get('select_related', [])

        prefetch_related = self.request.data.get('prefetch_related', [])

        for related in select_related:
            queryset = queryset.select_related(related)
        for related in prefetch_related:
            queryset = queryset.prefetch_related(related)

        # Dynamic validation for filter fields (if needed)
        # Implement additional validation logic here if necessary


        # Retrieve annotations from request payload (example)
        annotations = self.request.data.get('annotate', {})
        print(annotations)
        
        # Apply annotations to the queryset
        for annotation_name, annotation_value in annotations.items():
            
            queryset = queryset.annotate(result=annotation_name(annotation_value))
            print(queryset)

            # if annotation_name == 'count':
            #     queryset = queryset.annotate(
            #         total_count=Count(annotation_value)
            #     )
            # elif annotation_name == 'average':
            #     queryset = queryset.annotate(
            #         avg_value=Avg(annotation_value)
            #     )
            # Add more annotations as needed

        return queryset   

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
        

    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)   

class ProductViewSet(AltiMetrikViewSet):
    queryset = Product.objects.all()
    model_name=Product
    serializer_class = ProductSerializer
    
    def initialise_model_name(self):
        # Call the inherited method
        self.initialise_model_name()

    def dispatch(self, request, *args, **kwargs):

        try:
            if 'Authorization' not in request.headers:
                return Response({'error': 'Authorization header is missing'}, status=status.HTTP_401_UNAUTHORIZED)
        
        except AssertionError as e:
            # Return a response indicating the error
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        # Check if Authorization header is present
        
        
        # If Authorization header is present, proceed with the request
        return super().dispatch(request, *args, **kwargs)