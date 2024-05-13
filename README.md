AltiMetrikViewSet Class:

This is a custom viewset class that extends GenericViewSet and includes mixins for performing CRUD operations (ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin).
It defines several methods:
initialise_model_name: This method sets the model name and serializer class attributes.
get_serializer_class: Returns the serializer class based on the columns received in the request data.
filter_queryset: Filters the queryset based on the filters received in the request data.
get_queryset: Retrieves the queryset and performs operations like filtering, ordering, and annotations based on request data.
create: Handles HTTP POST requests to create new instances of the model.
update: Handles HTTP PATCH requests to update existing instances of the model.
destroy: Handles HTTP DELETE requests to delete instances of the model.
ProductViewSet Class:

This class extends AltiMetrikViewSet and provides specific functionality for handling product-related requests.
It defines the initialise_model_name method, which overrides the method from the parent class.
The dispatch method is overridden to check for the presence of the 'Authorization' header in the request. If the header is missing, it returns a 401 Unauthorized response; otherwise, it proceeds with the request.

// generic get Api requests for viewsets

{
  "columns": ["name", "price", "category"],

  "filters": [
    {"field": "price", "value": "10.99"},
    {"field": "category", "value": "Electronics"}
  ],

  "order_by": {"field": "price", "order": "desc"},

  "select_related": ["manufacturer", "reviews"],

  "prefetch_related": ["comments"],

  "annotate": {
    "total_sales": "Sum('sales__quantity')",
    "average_rating": "Avg('reviews__rating')"
  }
}
