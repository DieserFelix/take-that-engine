# enable automatic setup by importing routers here and collecting them in a list,
# main.py iterates the list and adds each router to the app.
from app.routers.rooms import rooms
from app.routers.games import games

# routers = [users, stores, categories, brands, articles, lists, list_items]
routers = [rooms, games]