from src.core.database import db
from src.core.module.accounts.models import User, Role, Permission, RolePermission, PermissionEnum, RoleEnum
from src.core.module.employee.models import Employee
from src.core.module.employee.data import JobPositionEnum, JobConditionEnum, ProfessionsEnum
from src.core.bcrypt import bcrypt
from src.core.module.equestrian.models import Horse, JAEnum, HorseTrainers
from src.core.module.jockey_amazon.models import (
    JockeyAmazon, SchoolInstitution, FamilyMember, WorkAssignment,
    DisabilityDiagnosisEnum, DisabilityTypeEnum, FamilyAssignmentEnum, PensionEnum,
    WorkProposalEnum, WorkConditionEnum, SedeEnum, DayEnum, EducationLevelEnum
)
from datetime import date


def seed_all(app):
    with app.app_context():
        seed_accounts()
        seed_employees()
        print("Commiting employees and accounts")
        db.session.commit()  # employees need to be commited before adding horse_trainers
        seed_equestrian_module()
        print("Commiting equestrian module")
        db.session.commit()
        seed_jockey_amazons()
        print("Commiting jockey_amazons module")
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
        Role(name=role.value) for role in RoleEnum
    ]

    db.session.add_all(roles)


def seed_permissions():
    permissions = [
        Permission(name=permission.value) for permission in PermissionEnum
    ]

    db.session.add_all(permissions)


def seed_role_permissions():
    role_permissions = [
        # Administración - Equipo
        *[RolePermission(role_id=4, permission_id=i) for i in range(1, 6)],
        # Administración - Pagos
        *[RolePermission(role_id=4, permission_id=i) for i in range(6, 11)],
        # Técnica - JYA
        *[RolePermission(role_id=1, permission_id=i) for i in range(11, 16)],
        # Administración - JYA
        *[RolePermission(role_id=4, permission_id=i) for i in range(11, 16)],
        # Ecuestre - JYA
        RolePermission(role_id=2, permission_id=11),  # JYA_INDEX
        RolePermission(role_id=2, permission_id=15),  # JYA_SHOW
        # Administración - Cobros
        *[RolePermission(role_id=4, permission_id=i) for i in range(16, 21)],
        # Técnica - Cobros
        RolePermission(role_id=1, permission_id=16),  # COBROS_INDEX
        RolePermission(role_id=1, permission_id=20),  # COBROS_SHOW
        # Ecuestre - Ecuestre
        *[RolePermission(role_id=2, permission_id=i) for i in range(21, 26)],
        # Administración - Ecuestre
        RolePermission(role_id=4, permission_id=21),  # ECUSTRE_INDEX
        RolePermission(role_id=4, permission_id=25),  # ECUSTRE_SHOW
        # Técnica - Ecuestre
        RolePermission(role_id=1, permission_id=21),  # ECUSTRE_INDEX
        RolePermission(role_id=1, permission_id=25),  # ECUSTRE_SHOW
    ]

    db.session.add_all(role_permissions)


def seed_users():
    def encrypt(password):
        return bcrypt.generate_password_hash(password).decode("utf-8")

    users = [
        User(email=email, alias=alias, password=encrypt(password), role_id=role_id, system_admin=system_admin)
        for email, alias, password, role_id, system_admin in [
            ("tecnica@gmail.com", "falso1", "Tecnica123", 1, False),
            ("ecuestre@gmail.com", "falso2", "Ecuestre123", 2, False),
            ("voluntariado@gmail.com", "falso3", "Voluntariado123", 3, False),
            ("administracion@gmail.com", "falso3", "Administracion123", 4, False),
            ("sysadmin@gmail.com", "sysadmin", "Sysadmin123", None, True),
        ]
    ]

    db.session.add_all(users)


def seed_employees():
    print("Seeding employees")
    employees = [
        Employee(
            email=email,
            phone=phone,
            name=name,
            lastname=lastname,
            dni=dni,
            profession=profession,
            position=position,
            health_insurance=health_insurance,
            affiliate_number=affiliate_number,
            job_condition=job_condition,
            user_id=user_id
        )
        for
        email, phone, name, lastname, dni, profession, position,
        health_insurance, affiliate_number, job_condition, user_id
        in [
            ("juan.perez@gmail.com", "123456789", "Juan", "Pérez", 12345678, ProfessionsEnum.PSICOLOGO,
             JobPositionEnum.TERAPEUTA, "Seguro Salud S.A.", 9876543, JobConditionEnum.VOLUNTARIO, 1),

            ("maria.garcia@gmail.com", "987654321", "María", "García", 23456789, ProfessionsEnum.MEDICO,
             JobPositionEnum.ADMINISTRATIVO, "Salud y Vida", 8765432, JobConditionEnum.VOLUNTARIO, 2),

            ("luis.martinez@gmail.com", "456789123", "Luis", "Martínez", 34567890, ProfessionsEnum.KINESIOLOGO,
             JobPositionEnum.TERAPEUTA, "Vida y Salud", 7654321, JobConditionEnum.PERSONAL_RENTADO, None),

            ("carla.lopez@gmail.com", "321654987", "Carla", "López", 45678901, ProfessionsEnum.DOCENTE,
             JobPositionEnum.DOCENTE_CAPACITACION, "Seguro Médico", 6543210, JobConditionEnum.VOLUNTARIO, None),

            ("jose.fernandez@gmail.com", "654987321", "José", "Fernández", 56789012, ProfessionsEnum.PSICOPEDAGOGO,
             JobPositionEnum.TERAPEUTA, "Salud Integral", 5432109, JobConditionEnum.VOLUNTARIO, None),

            ("sofia.gonzalez@gmail.com", "789321654", "Sofía", "González", 67890123, ProfessionsEnum.FONOAUDIOLOGO,
             JobPositionEnum.ADMINISTRATIVO, "Medicina Prepagada", 4321098, JobConditionEnum.VOLUNTARIO, None),

            ("pedro.sanchez@gmail.com", "159753468", "Pedro", "Sánchez", 78901234,
             ProfessionsEnum.TERAPISTA_OCUPACIONAL,
                JobPositionEnum.TERAPEUTA, "Plan de Salud", 3210987, JobConditionEnum.VOLUNTARIO, None),

            ("laura.morales@gmail.com", "753159486", "Laura", "Morales", 89012345, ProfessionsEnum.VETERINARIO,
             JobPositionEnum.VETERINARIO, "Seguro Veterinario", 2109876, JobConditionEnum.VOLUNTARIO, None),

            ("francisco.castro@gmail.com", "159258753", "Francisco", "Castro", 90123456, ProfessionsEnum.PSICOLOGO,
             JobPositionEnum.TERAPEUTA, "Salud y Bienestar", 1098765, JobConditionEnum.VOLUNTARIO, None),

            ("valentina.ramirez@gmail.com", "951753864", "Valentina", "Ramírez", 12345679, ProfessionsEnum.MEDICO,
             JobPositionEnum.ADMINISTRATIVO, "Seguros Médicos", 987650, JobConditionEnum.PERSONAL_RENTADO, None),

            ("mateo.gonzalez@gmail.com", "761753864", "Mateo", "Gonzalez", 987654, ProfessionsEnum.VETERINARIO,
             JobPositionEnum.ENTRENADOR_CABALLOS, "Seguros Médicos", 987650, JobConditionEnum.PERSONAL_RENTADO, None),

            ("ivan.pineda@gmail.com", "481753864", "Ivan", "Pineda", 987654321, ProfessionsEnum.VETERINARIO,
             JobPositionEnum.CONDUCTOR, "Seguros Médicos", 987650, JobConditionEnum.PERSONAL_RENTADO, None),
        ]
    ]

    # Add employees to the session and commit
    db.session.add_all(employees)


def seed_horses():
    horse_data = [
        ("Caballito blanco", date(2015, 5, 14), "M", "Thoroughbred", "Bay", False,
         date(2020, 8, 20), "Equestrian Center A", JAEnum.RECREATIONAL_ACTIVITIES),

        ("Bella", date(2013, 7, 2), "F", "Arabian", "Grey", True,
         date(2021, 4, 10), "Equestrian Center B", JAEnum.HIPOTHERAPY),

        ("Spirit", date(2017, 3, 11), "M", "Morgan", "Chestnut", False,
         date(2022, 2, 5), "Therapeutic Riding School", JAEnum.THERAPEUTIC_RIDING),

        ("Star", date(2014, 11, 30), "F", "Quarter Horse", "Palomino", False,
         date(2019, 9, 15), "Equestrian Center C", JAEnum.ADAPTED_SPORTS),

        ("Shadow", date(2016, 10, 18), "M", "Appaloosa", "Leopard", True,
         date(2023, 1, 7), "Equestrian Center A", JAEnum.RIDING)
    ]

    horses = [Horse(name=name, birth_date=birth_date, sex=sex, breed=breed, coat=coat, is_donation=is_donation,
                    admission_date=admission_date, assigned_facility=assigned_facility, ja_type=ja_type) for
              name, birth_date, sex, breed, coat, is_donation, admission_date, assigned_facility, ja_type in horse_data]

    db.session.add_all(horses)


def seed_horse_trainers():
    horse_trainers = [
        HorseTrainers(id_horse=1, id_employee=11),
        HorseTrainers(id_horse=2, id_employee=12),
        HorseTrainers(id_horse=3, id_employee=11),
        HorseTrainers(id_horse=4, id_employee=11),
        HorseTrainers(id_horse=4, id_employee=12),
    ]
    db.session.add_all(horse_trainers)

def seed_jockey_amazons():
    print("Seeding jockey_amazons")
    school1 = SchoolInstitution(
        name="Escuela Primaria N°1",
        street="Calle Falsa",
        number=123,
        department="Departamento 1",
        locality="Localidad 1",
        province="Provincia 1",
        phone_country_code="54",
        phone_area_code="11",
        phone_number="12345678"
    )
    db.session.add(school1)

    family_member1 = FamilyMember(
        relationship="Padre",
        first_name="Juan",
        last_name="Pérez",
        dni="12345678",
        street="Calle Falsa",
        number=123,
        department="Departamento 1",
        locality="Localidad 1",
        province="Provincia 1",
        phone_country_code="54",
        phone_area_code="11",
        phone_number="12345678",
        email="juan.perez@example.com",
        education_level=EducationLevelEnum.SECONDARY,
        occupation="Empleado"
    )
    db.session.add(family_member1)

    jockey1 = JockeyAmazon(
        first_name="María",
        last_name="González",
        dni="87654321",
        age=25,
        birth_date=date(1996, 5, 15),
        birthplace="Ciudad 1",
        is_scholarship=True,
        scholarship_observations="Observaciones de beca",
        has_disability=True,
        disability_diagnosis=DisabilityDiagnosisEnum.AUTISM_SPECTRUM_DISORDER,
        disability_other=None,
        disability_type=DisabilityTypeEnum.MENTAL,
        has_family_assignment=True,
        family_assignment_type=FamilyAssignmentEnum.UNIVERSAL_WITH_DISABLED_CHILD,
        has_pension=PensionEnum.NATIONAL,
        pension_details="Detalles de la pensión",
        social_security="Obra Social 1",
        social_security_number="123456789",
        has_curatorship=False,
        curatorship_observations=None,
        school_institution=school1,
        current_grade_year="5to Año",
        school_observations="Observaciones escolares",
        professionals="Profesionales involucrados",
        family_members=[family_member1]
    )
    db.session.add(jockey1)
    db.session.commit() # jockey1 needs to be commited before adding work_assignments
    work_assignment1 = WorkAssignment(
        proposal=WorkProposalEnum.HIPOTHERAPY,
        condition=WorkConditionEnum.REGULAR,
        sede=SedeEnum.CASJ,
        days=[DayEnum.MONDAY, DayEnum.WEDNESDAY, DayEnum.FRIDAY],
        professor_or_therapist_id=3,
        conductor_id=3,
        track_assistant_id=3,
        horse_id=3
    )
    db.session.add(work_assignment1)