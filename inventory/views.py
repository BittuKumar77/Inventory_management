# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated
# from django.core.cache import cache
# from .models import Item
# from .serializers import ItemSerializer

# class ItemViewSet(viewsets.ModelViewSet):
#     queryset = Item.objects.all()
#     serializer_class = ItemSerializer
#     permission_classes = [IsAuthenticated]

#     def retrieve(self, request, *args, **kwargs):
#         item_id = kwargs.get('pk')
#         cached_item = cache.get(f'item_{item_id}')
#         if cached_item:
#             return Response(cached_item)
        
#         response = super().retrieve(request, *args, **kwargs)
#         cache.set(f'item_{item_id}', response.data)
#         return response



from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Item
from .serializers import ItemSerializer
from django.db import IntegrityError
from rest_framework import viewsets
from django.core.cache import cache
from rest_framework import generics


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()  # Retrieve all items
    serializer_class = ItemSerializer  # Use the ItemSerializer for data
    permission_classes = [IsAuthenticated]  

class CreateItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            try:
                item = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"error": "Item already exists"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReadItemView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, item_id):
        try:
            item = Item.objects.get(pk=item_id)
            serializer = ItemSerializer(item)
            return Response(serializer.data)
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

class UpdateItemView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, item_id):
        try:
            item = Item.objects.get(pk=item_id)
            serializer = ItemSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        
class DeleteItemView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        try:
            item = Item.objects.get(pk=item_id)
            item.delete()
            return Response({"message": "Item deleted successfully"}, status=status.HTTP_200_OK)
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    lookup_field = 'id'  # Assuming you use 'id' as the lookup field

    def retrieve(self, request, *args, **kwargs):
        item_id = self.kwargs.get('id')
        cache_key = f'item_{item_id}'
        item = cache.get(cache_key)

        if item is None:
            try:
                item_instance = self.get_object()  # Fetch item from DB
                serializer = self.get_serializer(item_instance)
                item = serializer.data
                cache.set(cache_key, item, timeout=60 * 15)  # Cache for 15 minutes
            except Item.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(item)
