from backend.routes.auth import router as auth_router
from backend.routes.projects import router as projects_router
from backend.routes.tasks import router as tasks_router
from backend.routes.components import router as components_router
from backend.routes.portfolio import router as portfolio_router
from backend.routes.public import router as public_router

__all__ = [
    "auth_router",
    "projects_router",
    "tasks_router",
    "components_router",
    "portfolio_router",
    "public_router",
]
