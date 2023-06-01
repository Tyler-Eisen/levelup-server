from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Game, Gamer

class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for Event types"""
    time = serializers.TimeField(format="%I:%M %p")
    date = serializers.DateField(format="%B %d, %Y")
    class Meta:
        model = Event
        fields = ('id', 'game', 'description', 'date', 'time', 'organizer')

class EventView(ViewSet):
    """Level up Event types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single Event type
            
        Returns:
            Response -- JSON serialized Event type
        """
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all Event types
        
        Returns:
            Response -- JSON serialized list of Event types
        """
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    
    def create(self, request):
      game = Game.objects.get(pk=request.data["game"])
      gamer = Gamer.objects.get(uid=request.data["organizer"])

      event = Event(
          game=game,
          description=request.data["description"],
          date=request.data["date"],
          time=request.data["time"],
          organizer=gamer
      )
      event.save()
      serializer = EventSerializer(event)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
      """Handle PUT requests for an event

      Returns:
          Response -- Empty body with 204 status code
      """

      event = Event.objects.get(pk=pk)
      event.description = request.data["description"]
      event.date = request.data["date"]
      event.time = request.data["time"]

      game = Game.objects.get(pk=request.data["game"])
      event.game = game

      organizer = Gamer.objects.get(pk=request.data["organizer"])
      event.organizer = organizer

      event.save()
      serializer = EventSerializer(event)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk):
      event = Event.objects.get(pk=pk)
      event.delete()
      return Response(None, status=status.HTTP_204_NO_CONTENT)
    