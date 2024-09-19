from dependency_injector import containers, providers
from core.database import db
from .module.accounts import AccountsServices, AccountsRepository


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    # Repositories
    accounts_repository = providers.Singleton(AccountsRepository, database=db)

    # Services
    accounts_services = providers.Singleton(
        AccountsServices, accounts_repository=accounts_repository
    )
