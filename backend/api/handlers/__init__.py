from backend.api.handlers.auth import api_router as auth
from backend.api.handlers.users import api_router as users

list_of_routes = [
    users,
    auth,
]
