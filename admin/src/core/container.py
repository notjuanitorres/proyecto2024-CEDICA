from dependency_injector import containers, providers
from .module.accounts import AccountsServices, AccountsRepository
from core.database import db


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["src.core.module.accounts", "src.web.controllers.auth"])
    config = providers.Configuration()

    # Repositories
    accounts_repository = providers.Factory(AccountsRepository, database=db)

    # Services
    accounts_services = providers.Singleton(AccountsServices,
                                        accounts_repository=accounts_repository)
