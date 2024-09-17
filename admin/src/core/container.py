from dependency_injector import containers, providers
from core.module.user.repositories import UserRepository
from core.module.user.services import UserServices


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    # Repositories
    user_repository = providers.Factory(UserRepository)

    # Services
    user_services = providers.Factory(UserServices, user_repository=user_repository)
