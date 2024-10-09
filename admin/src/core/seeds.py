from datetime import datetime
from datetime import datetime
from src.core.database import db
from src.core.module.accounts.models import User, Role, Permission, RolePermission
from src.core.module.employee.models import Employee
from src.core.module.employee.data import PositionEnum, ConditionEnum, ProfessionsEnum
from src.core.module.employee.models import Employee
from src.core.module.employee.data import PositionEnum, ConditionEnum, ProfessionsEnum
from src.core.bcrypt import bcrypt
from src.core.module.equestrian.models import Horse, JAEnum, HorseTrainers
from datetime import date


def seed_all():
    seed_accounts()
    seed_employees()
    print("Commiting employees and accounts")
    db.session.commit()  # employees need to be commited before adding horse_trainers
    seed_equestrian_module()
    print("Commiting equestrian module")
    db.session.commit()


def seed_equestrian_module():
    print("Seeding horses")
    seed_horses()
    print("Seeding HorseTrainers")
    seed_horse_trainers()


def seed_accounts():
    print("Seeding roles")
    seed_roles()
    print("Seeding permissions")
    seed_permissions()
    print("Seeding role_permissions")
    seed_role_permissions()
    print("Seeding users")
    seed_users()


def seed_roles():
    roles = [
        Role(name="Técnico"),
        Role(name="Ecuestre"),
        Role(name="Voluntario"),
        Role(name="Administración")
    ]

    db.session.add_all(roles)


def seed_permissions():
    permissions = [
        Permission(name="equipo_index"),
        Permission(name="equipo_new"),
        Permission(name="equipo_update"),
        Permission(name="equipo_destroy"),
        Permission(name="equipo_show"),
        Permission(name="pagos_index"),
        Permission(name="pagos_new"),
        Permission(name="pagos_update"),
        Permission(name="pagos_destroy"),
        Permission(name="pagos_show"),
        Permission(name="jya_index"),
        Permission(name="jya_new"),
        Permission(name="jya_update"),
        Permission(name="jya_destroy"),
        Permission(name="jya_show"),
        Permission(name="cobros_index"),
        Permission(name="cobros_new"),
        Permission(name="cobros_update"),
        Permission(name="cobros_destroy"),
        Permission(name="cobros_show"),
        Permission(name="ecuestre_index"),
        Permission(name="ecuestre_new"),
        Permission(name="ecuestre_update"),
        Permission(name="ecuestre_destroy"),
        Permission(name="ecuestre_show"),
    ]

    db.session.add_all(permissions)


def seed_role_permissions():
    role_permissions = [
        # Administración - Equipo
        RolePermission(role_id=4, permission_id=1),  # equipo_index
        RolePermission(role_id=4, permission_id=2),  # equipo_new
        RolePermission(role_id=4, permission_id=3),  # equipo_update
        RolePermission(role_id=4, permission_id=4),  # equipo_destroy
        RolePermission(role_id=4, permission_id=5),  # equipo_show
        # Administración - Pagos
        RolePermission(role_id=4, permission_id=6),  # pagos_index
        RolePermission(role_id=4, permission_id=7),  # pagos_new
        RolePermission(role_id=4, permission_id=8),  # pagos_update
        RolePermission(role_id=4, permission_id=9),  # pagos_destroy
        RolePermission(role_id=4, permission_id=10),  # pagos_show
        # Técnica - JYA
        RolePermission(role_id=1, permission_id=11),  # jya_index
        RolePermission(role_id=1, permission_id=12),  # jya_new
        RolePermission(role_id=1, permission_id=13),  # jya_update
        RolePermission(role_id=1, permission_id=14),  # jya_destroy
        RolePermission(role_id=1, permission_id=15),  # jya_show
        # Administración - JYA
        RolePermission(role_id=4, permission_id=11),  # jya_index
        RolePermission(role_id=4, permission_id=12),  # jya_new
        RolePermission(role_id=4, permission_id=13),  # jya_update
        RolePermission(role_id=4, permission_id=14),  # jya_destroy
        RolePermission(role_id=4, permission_id=15),  # jya_show
        # Ecuestre - JYA
        RolePermission(role_id=2, permission_id=11),  # jya_index
        RolePermission(role_id=2, permission_id=15),  # jya_show
        # Administración - Cobros
        RolePermission(role_id=4, permission_id=16),  # cobros_index
        RolePermission(role_id=4, permission_id=17),  # cobros_new
        RolePermission(role_id=4, permission_id=18),  # cobros_update
        RolePermission(role_id=4, permission_id=19),  # cobros_destroy
        RolePermission(role_id=4, permission_id=20),  # cobros_show
        # Técnica - Cobros
        RolePermission(role_id=1, permission_id=16),  # cobros_index
        RolePermission(role_id=1, permission_id=20),  # cobros_show
        # Ecuestre - Ecuestre
        RolePermission(role_id=2, permission_id=21),  # ecuestre_index
        RolePermission(role_id=2, permission_id=22),  # ecuestre_new
        RolePermission(role_id=2, permission_id=23),  # ecuestre_update
        RolePermission(role_id=2, permission_id=24),  # ecuestre_destroy
        RolePermission(role_id=2, permission_id=25),  # ecuestre_show
        # Administración - Ecuestre
        RolePermission(role_id=4, permission_id=21),  # ecuestre_index
        RolePermission(role_id=4, permission_id=25),  # ecuestre_show
        # Técnica - Ecuestre
        RolePermission(role_id=1, permission_id=21),  # ecuestre_index
        RolePermission(role_id=1, permission_id=25),  # ecuestre_show
    ]

    db.session.add_all(role_permissions)


def seed_users():
    def encrypt(password):
        return bcrypt.generate_password_hash(password).decode("utf-8")

    users = [
        User(
            email="tecnica@gmail.com",
            alias="falso1",
            password=encrypt("Tecnica123"),
            role_id=1,
        ),
        User(
            email="ecuestre@gmail.com",
            alias="falso2",
            password=encrypt("Ecuestre123"),
            role_id=2,
        ),
        User(
            email="voluntariado@gmail.com",
            alias="falso3",
            password=encrypt("Voluntariado123"),
            role_id=3,
        ),
        User(
            email="administracion@gmail.com",
            alias="falso3",
            password=encrypt("Administracion123"),
            role_id=4,
        ),
        User(
            email="sysadmin@gmail.com",
            alias="sysadmin",
            password=encrypt("Sysadmin123"),
            system_admin=True,
        ),
        User(
            email="tecnica@gmail.com",
            alias="falso1",
            password=encrypt("Tecnica123"),
            role_id=1,
        ),
        User(
            email="ecuestre@gmail.com",
            alias="falso2",
            password=encrypt("Ecuestre123"),
            role_id=2,
        ),
        User(
            email="voluntariado@gmail.com",
            alias="falso3",
            password=encrypt("Voluntariado123"),
            role_id=3,
        ),
        User(
            email="administracion@gmail.com",
            alias="falso3",
            password=encrypt("Administracion123"),
            role_id=4,
        ),
        User(
            email="sysadmin@gmail.com",
            alias="sysadmin",
            password=encrypt("Sysadmin123"),
            system_admin=True,
        ),
    ]

    db.session.add_all(users)


def seed_employees():
    print("Seeding employees")
    employees = [
        Employee(
            email="juan.perez@gmail.com",
            phone="123456789",
            name="Juan",
            lastname="Pérez",
            dni=12345678,
            profession=ProfessionsEnum.PSICOLOGO,
            position=PositionEnum.TERAPEUTA,
            health_insurance="Seguro Salud S.A.",
            affiliate_number=9876543,
            job_condition=ConditionEnum.VOLUNTARIO,
            user_id=1,
        ),
        Employee(
            email="maria.garcia@gmail.com",
            phone="987654321",
            name="María",
            lastname="García",
            dni=23456789,
            profession=ProfessionsEnum.MEDICO,
            position=PositionEnum.ADMINISTRATIVO,
            health_insurance="Salud y Vida",
            affiliate_number=8765432,
            job_condition=ConditionEnum.VOLUNTARIO,
            user_id=2,
        ),
        Employee(
            email="luis.martinez@gmail.com",
            phone="456789123",
            name="Luis",
            lastname="Martínez",
            dni=34567890,
            profession=ProfessionsEnum.KINESIOLOGO,
            position=PositionEnum.TERAPEUTA,
            health_insurance="Vida y Salud",
            affiliate_number=7654321,
            job_condition=ConditionEnum.PERSONAL_RENTADO,
        ),
        Employee(
            email="carla.lopez@gmail.com",
            phone="321654987",
            name="Carla",
            lastname="López",
            dni=45678901,
            profession=ProfessionsEnum.DOCENTE,
            position=PositionEnum.DOCENTE_CAPACITACION,
            health_insurance="Seguro Médico",
            affiliate_number=6543210,
            job_condition=ConditionEnum.VOLUNTARIO,
        ),
        Employee(
            email="jose.fernandez@gmail.com",
            phone="654987321",
            name="José",
            lastname="Fernández",
            dni=56789012,
            profession=ProfessionsEnum.PSICOPEDAGOGO,
            position=PositionEnum.TERAPEUTA,
            health_insurance="Salud Integral",
            affiliate_number=5432109,
            job_condition=ConditionEnum.VOLUNTARIO,
         ),
        Employee(
            email="sofia.gonzalez@gmail.com",
            phone="789321654",
            name="Sofía",
            lastname="González",
            dni=67890123,
            profession=ProfessionsEnum.FONOAUDIOLOGO,
            position=PositionEnum.ADMINISTRATIVO,
            health_insurance="Medicina Prepagada",
            affiliate_number=4321098,
            job_condition=ConditionEnum.VOLUNTARIO,
        ),
        Employee(
            email="pedro.sanchez@gmail.com",
            phone="159753468",
            name="Pedro",
            lastname="Sánchez",
            dni=78901234,
            profession=ProfessionsEnum.TERAPISTA_OCUPACIONAL,
            position=PositionEnum.TERAPEUTA,
            health_insurance="Plan de Salud",
            affiliate_number=3210987,
            job_condition=ConditionEnum.VOLUNTARIO,
        ),
        Employee(
            email="laura.morales@gmail.com",
            phone="753159486",
            name="Laura",
            lastname="Morales",
            dni=89012345,
            profession=ProfessionsEnum.VETERINARIO,
            position=PositionEnum.VETERINARIO,
            health_insurance="Seguro Veterinario",
            affiliate_number=2109876,
            job_condition=ConditionEnum.VOLUNTARIO,
        ),
        Employee(
            email="francisco.castro@gmail.com",
            phone="159258753",
            name="Francisco",
            lastname="Castro",
            dni=90123456,
            profession=ProfessionsEnum.PSICOLOGO,
            position=PositionEnum.TERAPEUTA,
            health_insurance="Salud y Bienestar",
            affiliate_number=1098765,
            job_condition=ConditionEnum.VOLUNTARIO,
        ),
        Employee(
            email="valentina.ramirez@gmail.com",
            phone="951753864",
            name="Valentina",
            lastname="Ramírez",
            dni=12345679,
            profession=ProfessionsEnum.MEDICO,
            position=PositionEnum.ADMINISTRATIVO,
            health_insurance="Seguros Médicos",
            affiliate_number=987650,
            job_condition=ConditionEnum.PERSONAL_RENTADO,
        ),
    ]

    # Add employees to the session and commit
    db.session.add_all(employees)


def seed_horses():
    horses = [
        Horse(
            name="Caballito blanco",
            birth_date=date(2015, 5, 14),
            sex="M",
            breed="Thoroughbred",
            coat="Bay",
            is_donation=False,
            admission_date=date(2020, 8, 20),
            assigned_facility="Equestrian Center A",
            ja_type=JAEnum.RECREATIONAL_ACTIVITIES
        ),
        Horse(
            name="Bella",
            birth_date=date(2013, 7, 2),
            sex="F",
            breed="Arabian",
            coat="Grey",
            is_donation=True,
            admission_date=date(2021, 4, 10),
            assigned_facility="Equestrian Center B",
            ja_type=JAEnum.HIPOTHERAPY
        ),
        Horse(
            name="Spirit",
            birth_date=date(2017, 3, 11),
            sex="M",
            breed="Morgan",
            coat="Chestnut",
            is_donation=False,
            admission_date=date(2022, 2, 5),
            assigned_facility="Therapeutic Riding School",
            ja_type=JAEnum.THERAPEUTIC_RIDING
        ),
        Horse(
            name="Star",
            birth_date=date(2014, 11, 30),
            sex="F",
            breed="Quarter Horse",
            coat="Palomino",
            is_donation=False,
            admission_date=date(2019, 9, 15),
            assigned_facility="Equestrian Center C",
            ja_type=JAEnum.ADAPTED_SPORTS
        ),
        Horse(
            name="Shadow",
            birth_date=date(2016, 10, 18),
            sex="M",
            breed="Appaloosa",
            coat="Leopard",
            is_donation=True,
            admission_date=date(2023, 1, 7),
            assigned_facility="Equestrian Center A",
            ja_type=JAEnum.RIDING
        )
    ]
    print("Horses added")
    db.session.add_all(horses)


def seed_horse_trainers():
    horse_trainers = [
        HorseTrainers(id_horse=1, id_employee=1),
        HorseTrainers(id_horse=2, id_employee=2),
        HorseTrainers(id_horse=3, id_employee=3),
        HorseTrainers(id_horse=4, id_employee=4),
        HorseTrainers(id_horse=5, id_employee=5),
    ]
    db.session.add_all(horse_trainers)
