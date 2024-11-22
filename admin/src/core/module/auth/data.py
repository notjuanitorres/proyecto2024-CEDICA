from enum import Enum as pyEnum


class RoleEnum(pyEnum):
    """
    Enumeration for different user roles.

    Attributes:
        TECNICO (str): Technical role.
        ECUESTRE (str): Equestrian role.
        VOLUNTARIO (str): Volunteer role.
        ADMINISTRACION (str): Administration role.
    """
    TECNICO = "Técnico"
    ECUESTRE = "Ecuestre"
    VOLUNTARIO = "Voluntario"
    ADMINISTRACION = "Administración"


class PermissionEnum(pyEnum):
    """
    Enumeration for different user permissions.

    Attributes:
        EQUIPO_INDEX (str): Permission to index equipment.
        EQUIPO_NEW (str): Permission to create new equipment.
        EQUIPO_UPDATE (str): Permission to update equipment.
        EQUIPO_DESTROY (str): Permission to destroy equipment.
        EQUIPO_SHOW (str): Permission to show equipment details.
        PAGOS_INDEX (str): Permission to index payments.
        PAGOS_NEW (str): Permission to create new payments.
        PAGOS_UPDATE (str): Permission to update payments.
        PAGOS_DESTROY (str): Permission to destroy payments.
        PAGOS_SHOW (str): Permission to show payment details.
        JYA_INDEX (str): Permission to index jockeys and amazons.
        JYA_NEW (str): Permission to create new jockeys and amazons.
        JYA_UPDATE (str): Permission to update jockeys and amazons.
        JYA_DESTROY (str): Permission to destroy jockeys and amazons.
        JYA_SHOW (str): Permission to show jockey and amazon details.
        COBROS_INDEX (str): Permission to index charges.
        COBROS_NEW (str): Permission to create new charges.
        COBROS_UPDATE (str): Permission to update charges.
        COBROS_DESTROY (str): Permission to destroy charges.
        COBROS_SHOW (str): Permission to show charge details.
        ECUSTRE_INDEX (str): Permission to index equestrian activities.
        ECUSTRE_NEW (str): Permission to create new equestrian activities.
        ECUSTRE_UPDATE (str): Permission to update equestrian activities.
        ECUSTRE_DESTROY (str): Permission to destroy equestrian activities.
        ECUSTRE_SHOW (str): Permission to show equestrian activity details.
        REPORT_INDEX (str): Permission to index reports.
        REPORT_SHOW (str): Permission to show report details
    """
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
    REPORT_INDEX = "report_index"
    REPORT_SHOW = "report_show"