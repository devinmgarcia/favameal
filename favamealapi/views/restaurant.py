"""View module for handling requests about restaurants"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from favamealapi.models import Restaurant
from favamealapi.models.favoriterestaurant import FavoriteRestaurant
from django.contrib.auth.models import User
from rest_framework.decorators import action


class RestaurantView(ViewSet):
    """ViewSet for handling restuarant requests"""

    def create(self, request):
        """Handle POST operations for restaurants

        Returns:
            Response -- JSON serialized event instance
        """
        rest = Restaurant()
        rest.name = request.data["name"]
        rest.address = request.data["address"]

        try:
            rest.save()
            serializer = RestaurantSerializer(
                rest, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            restaurant = Restaurant.objects.get(pk=pk)

            # TODO: Add the correct value to the `favorite` property of the requested restaurant

            serializer = RestaurantSerializer(
                restaurant, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to restaurants resource

        Returns:
            Response -- JSON serialized list of restaurants
        """
        # user = User.objects.get(user=request.auth.user)
        restaurants = Restaurant.objects.all()

        # TODO: Add the correct value to the `favorite` property of each restaurant
        # for restaurant in restaurants:
        #     restaurant.starred = user in restaurant.starred.all()

        serializer = RestaurantSerializer(restaurants, many=True, context={'request': request})

        return Response(serializer.data)

    # TODO: Write a custom action named `star` that will allow a client to
    # send a POST and a DELETE request to /restaurant/2/star

    @action(methods=['post', 'delete'], detail=True)
    def star(self, request, pk=None):
        """Managing users favorite restaurants"""
        # Django uses the `Authorization` header to determine
        # which user is making the request to sign up

        user = User.objects.get(username=request.auth.user)
        
        try:
            # Handle the case if the client specifies a game
            # that doesn't exist
            restaurant = Restaurant.objects.get(pk=pk)
        except Restaurant.DoesNotExist:
            return Response(
                {'message': 'Restaurant does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # A gamer wants to sign up for an event
        if request.method == "POST":
            try:
                # Using the attendees field on the event makes it simple to add a gamer to the event
                # .add(gamer) will insert into the join table a new row the gamer_id and the event_id
                restaurant.favorite.add(user)
                return Response({}, status=status.HTTP_201_CREATED)
            except Exception as ex:
                return Response({'message': ex.args[0]})

        # User wants to leave a previously joined event
        elif request.method == "DELETE":
            try:
                # The many to many relationship has a .remove method that removes the gamer from the attendees list
                # The method deletes the row in the join table that has the gamer_id and event_id
                restaurant.favorite.remove(user)
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            except Exception as ex:
                return Response({'message': ex.args[0]})

class RestaurantSerializer(serializers.ModelSerializer):
    """JSON serializer for restaurants"""

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'address', 'favorite', 'starred')
        depth = 2

class FaveSerializer(serializers.ModelSerializer):
    """JSON serializer for favorites"""

    class Meta:
        model = FavoriteRestaurant
        fields = ('restaurant',)
        depth = 2

