# pylint: disable=I1101
from dependency_injector import containers, providers
from .module.auth import AuthRepository, AuthServices
from .module.user import UserRepository
from .module.employee import EmployeeRepository
from .module.equestrian import EquestrianServices, EquestrianRepository
from .module.common import StorageServices


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    # TODO: Initialize the db in the container so it can be injected into the repository
    user_repository = providers.Factory(UserRepository)
    auth_repository = providers.Factory(AuthRepository)
    employee_repository = providers.Factory(EmployeeRepository)
    equestrian_repository = providers.Factory(EquestrianRepository)

    # Services
    storage_services = providers.Factory(StorageServices)

    auth_services = providers.Factory(
        AuthServices, auth_repository=auth_repository, user_repository=user_repository
    )

    equestrian_services = providers.Factory(
        EquestrianServices, equestrian_repository=equestrian_repository
    )
