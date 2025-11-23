# from backend.server.handlers.auth import api_router as authentification
# from backend.server.handlers.projects import api_router as projects
# from backend.server.handlers.templates import api_router as templates
# from backend.server.handlers.messages import api_router as message
# from backend.api.handlers.ping import api_router as ping
from backend.api.handlers.users import api_router as users


list_of_routes = [
    users,

]
