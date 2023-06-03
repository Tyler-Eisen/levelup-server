from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Game, Gamer, EventGamer
from rest_framework.decorators import action

class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for Event types"""
    time = serializers.TimeField(format="%I:%M %p")
    date = serializers.DateField(format="%B %d, %Y")
    class Meta:
        model = Event
        fields = ('id', 'game', 'organizer',
          'description', 'date', 'time',
          'joined')

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
        
        uid = request.META['HTTP_AUTHORIZATION']
        gamer = Gamer.objects.get(uid=uid)

        for event in events:
    
          event.joined = len(EventGamer.objects.filter(
          gamer=gamer, event=event)) > 0

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
    
    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
      """Post request for a user to sign up for an event"""
      gamer = Gamer.objects.get(uid=request.data["userId"])
      event = Event.objects.get(pk=pk)
      attendee = EventGamer.objects.create(
        gamer=gamer,
        event=event
    )
      return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)
    
    @action(methods=['delete'], detail=True)
    def leave(self, request, pk=None):
      """Delete request for a user to leave an event"""

      # Get the gamer and event objects
      gamer = Gamer.objects.get(uid=request.data["userId"])
      event = Event.objects.get(pk=pk)

      # Find and remove the event_gamer object
      event_gamer = EventGamer.objects.get(gamer=gamer, event=event)
      event_gamer.delete()

      return Response({'message': 'Gamer removed'}, status=status.HTTP_204_NO_CONTENT)
