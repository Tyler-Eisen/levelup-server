from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from levelupapi.views import GameTypeView, EventView, GameView
from django.urls import path
from levelupapi.views import register_user, check_user

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'gametypes', GameTypeView, 'gametype')
router.register(r'events', EventView, 'event')
router.register(r'games', GameView, 'game')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('register', register_user),
    path('checkuser', check_user),
]
