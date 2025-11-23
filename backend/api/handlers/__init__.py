from backend.api.handlers.users import api_router as users
from backend.api.handlers.auth import api_router as auth

list_of_routes = [
    users,
    auth,
]
