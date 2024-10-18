
from enum import Enum as pyEnum


class RoleEnum(pyEnum):
    TECNICO = "Técnico"
    ECUESTRE = "Ecuestre"
    VOLUNTARIO = "Voluntario"
    ADMINISTRACION = "Administración"


class PermissionEnum(pyEnum):
    EQUIPO_INDEX = "equipo_index"
    EQUIPO_NEW = "equipo_new"
    EQUIPO_UPDATE = "equipo_update"
    EQUIPO_DESTROY = "equipo_destroy"
    EQUIPO_SHOW = "equipo_show"
    PAGOS_INDEX = "pagos_index"
    PAGOS_NEW = "pagos_new"
    PAGOS_UPDATE = "pagos_update"
    PAGOS_DESTROY = "pagos_destroy"
    PAGOS_SHOW = "pagos_show"
    JYA_INDEX = "jya_index"
    JYA_NEW = "jya_new"
    JYA_UPDATE = "jya_update"
    JYA_DESTROY = "jya_destroy"
    JYA_SHOW = "jya_show"
    COBROS_INDEX = "cobros_index"
    COBROS_NEW = "cobros_new"
    COBROS_UPDATE = "cobros_update"
    COBROS_DESTROY = "cobros_destroy"
    COBROS_SHOW = "cobros_show"
    ECUSTRE_INDEX = "ecuestre_index"
    ECUSTRE_NEW = "ecuestre_new"
    ECUSTRE_UPDATE = "ecuestre_update"
    ECUSTRE_DESTROY = "ecuestre_destroy"
    ECUSTRE_SHOW = "ecuestre_show"

