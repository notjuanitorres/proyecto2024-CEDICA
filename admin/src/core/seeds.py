from src.core.module.charges.models import Charge, PaymentMethodEnum
from src.core.database import db
from src.core.module.user.models import User
from src.core.module.auth.models import Role, Permission, RolePermission
from src.core.module.auth.data import PermissionEnum, RoleEnum
from src.core.module.employee.models import Employee
from src.core.module.payment.models import Payment
from src.core.module.payment.data import PaymentTypeEnum
from src.core.module.employee.data import (
    JobPositionEnum as PositionEnum,
    JobConditionEnum as ConditionEnum,
    ProfessionsEnum,
)
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
    """
    Seeds all the necessary data into the database.

    This function runs the seeding process for accounts, employees, and the equestrian module,
    committing changes to the database at appropriate points.

    Args:
        app (Flask): The Flask application instance used to get the application context.
    """
    with app.app_context():
        seed_accounts()
        seed_employees()
        print("Commiting employees and accounts")
        db.session.commit()  # employees need to be commited before adding horse_trainers
        seed_equestrian_module()
        print("Commiting equestrian module")
        seed_payments()
        print("Commiting payments")
        db.session.commit()
        seed_jockey_amazons()
        print("Commiting jockey_amazons module")
        print("Seeding charges")
        seed_charges()
        print("Commiting charges")
        db.session.commit()


def seed_equestrian_module():
    """
    Seeds data related to the equestrian module.

    This includes horses and horse trainers.
    """
    print("Seeding horses")
    seed_horses()
    print("Seeding HorseTrainers")
    seed_horse_trainers()


def seed_accounts():
    """
    Seeds account-related data.

    This includes roles, permissions, role-permission mappings, and users.
    """
    print("Seeding roles")
    seed_roles()
    print("Seeding permissions")
    seed_permissions()
    print("Seeding role_permissions")
    seed_role_permissions()
    print("Seeding users")
    seed_users()


def seed_roles():
    """
    Seeds the roles in the database.

    Roles are added based on the `RoleEnum` enumeration.
    """
    roles = [
        Role(name=role.value) for role in RoleEnum
    ]

    db.session.add_all(roles)


def seed_permissions():
    """
    Seeds the permissions in the database.

    Permissions are added based on the `PermissionEnum` enumeration.
    """
    permissions = [
        Permission(name=permission.value) for permission in PermissionEnum
    ]

    db.session.add_all(permissions)


def seed_role_permissions():
    """
    Seeds the role-permission relationships in the database.

    This defines which permissions are granted to specific roles.
    """
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
    """
    Seeds the users in the database.

    This function creates several default users with different roles and system access.
    """

    def encrypt(password):
        """
        Encrypts a password using bcrypt.

        Args:
            password (str): The plaintext password to encrypt.

        Returns:
            str: The hashed password.
        """
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
    """
    Seeds employees in the database.

    This function creates several employees with different professions, positions, and conditions.
    """
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
    """
    Seeds horse data in the database.

    This function creates several horses with various attributes and assigned facilities.
    """
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
         date(2023, 1, 7), "Equestrian Center A", JAEnum.RIDING),

        ("Rocinante", date(2018, 1, 15), "M", "Andalusian", "Grey", False,
         date(2024, 3, 25), "Equestrian Center B", JAEnum.RECREATIONAL_ACTIVITIES),
    ]

    horses = [Horse(name=name, birth_date=birth_date, sex=sex, breed=breed, coat=coat, is_donation=is_donation,
                    admission_date=admission_date, assigned_facility=assigned_facility, ja_type=ja_type) for
              name, birth_date, sex, breed, coat, is_donation, admission_date, assigned_facility, ja_type in horse_data]

    db.session.add_all(horses)


def seed_horse_trainers():
    """
    Seeds horse trainer data in the database.

    This function assigns horse trainers to horses.
    """
    horse_trainers = [
        HorseTrainers(id_horse=1, id_employee=11),
        HorseTrainers(id_horse=2, id_employee=12),
        HorseTrainers(id_horse=3, id_employee=11),
        HorseTrainers(id_horse=4, id_employee=11),
        HorseTrainers(id_horse=4, id_employee=12),
    ]
    db.session.add_all(horse_trainers)

def seed_payments():
     payments = [
        Payment(amount=100.0, payment_date=date(2023, 1, 15), payment_type=PaymentTypeEnum.HONORARIOS, description='Payment for services', beneficiary_id=1, is_archived=False),
        Payment(amount=200.0, payment_date=date(2023, 2, 20), payment_type=PaymentTypeEnum.PROOVEDOR, description='Payment for goods', is_archived=False),
        Payment(amount=150.0, payment_date=date(2023, 3, 10), payment_type=PaymentTypeEnum.HONORARIOS, description='Refund', beneficiary_id=3, is_archived=True),
        Payment(amount=250.0, payment_date=date(2023, 4, 5), payment_type=PaymentTypeEnum.GASTOS, description='Payment for subscription', is_archived=False),
        Payment(amount=300.0, payment_date=date(2023, 5, 25), payment_type=PaymentTypeEnum.HONORARIOS, description='Payment for membership', beneficiary_id=5, is_archived=False),
        Payment(amount=400.0, payment_date=date(2023, 6, 15), payment_type=PaymentTypeEnum.PROOVEDOR, description='Payment for consultancy', is_archived=True),
        Payment(amount=500.0, payment_date=date(2023, 7, 20), payment_type=PaymentTypeEnum.GASTOS, description='Payment for equipment', is_archived=False),
        Payment(amount=600.0, payment_date=date(2023, 8, 10), payment_type=PaymentTypeEnum.HONORARIOS, description='Payment for training', beneficiary_id=3, is_archived=False),
        Payment(amount=700.0, payment_date=date(2023, 9, 5), payment_type=PaymentTypeEnum.PROOVEDOR, description='Payment for software', is_archived=True),
        Payment(amount=800.0, payment_date=date(2023, 10, 25), payment_type=PaymentTypeEnum.GASTOS, description='Payment for hardware', is_archived=False),
        Payment(amount=900.0, payment_date=date(2023, 11, 15), payment_type=PaymentTypeEnum.HONORARIOS, description='Payment for maintenance', beneficiary_id=1, is_archived=False),
        Payment(amount=1000.0, payment_date=date(2023, 12, 20), payment_type=PaymentTypeEnum.PROOVEDOR, description='Payment for license', is_archived=True),
        Payment(amount=1100.0, payment_date=date(2024, 1, 10), payment_type=PaymentTypeEnum.GASTOS, description='Payment for support', is_archived=False),
        Payment(amount=1200.0, payment_date=date(2024, 2, 5), payment_type=PaymentTypeEnum.HONORARIOS, description='Payment for hosting', beneficiary_id=4, is_archived=False),
        Payment(amount=1300.0, payment_date=date(2024, 3, 25), payment_type=PaymentTypeEnum.PROOVEDOR, description='Payment for domain', is_archived=True),
    ]

     db.session.add_all(payments)
     db.session.commit()
     print("Seeding payments completed")

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
    school2 = SchoolInstitution(
        name="Escuela Secundaria N°2",
        street="Otra Calle",
        number=456,
        department="Departamento 2",
        locality="Localidad 2",
        province="Provincia 2",
        phone_country_code="54",
        phone_area_code="11",
        phone_number="87654321"
    )
    school3 = SchoolInstitution(
        name="Escuela Secundaria N°3",
        street="Av. Siempreviva",
        number=742,
        department="Departamento Central",
        locality="Springfield",
        province="Provincia 3",
        phone_country_code="54",
        phone_area_code="351",
        phone_number="1231234"
    )
    db.session.add_all([school1, school2, school3])

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
    family_member2 = FamilyMember(
        relationship="Madre",
        first_name="Laura",
        last_name="Gómez",
        dni="23456789",
        street="Otra Calle",
        number=456,
        department="Departamento 2",
        locality="Localidad 2",
        province="Provincia 2",
        phone_country_code="54",
        phone_area_code="11",
        phone_number="87654321",
        email="laura.gomez@example.com",
        education_level=EducationLevelEnum.TERTIARY,
        occupation="Médico"
    )
    family_member3 = FamilyMember(
        relationship="Madre",
        first_name="Ana",
        last_name="Romero",
        dni="34567890",
        street="Calle Los Álamos",
        number=321,
        department="Departamento Norte",
        locality="Springfield",
        province="Provincia 3",
        phone_country_code="54",
        phone_area_code="351",
        phone_number="5675678",
        email="ana.romero@example.com",
        education_level=EducationLevelEnum.TERTIARY,
        occupation="Docente"
    )
    db.session.add_all([family_member1, family_member2, family_member3])

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
    work_assignment2 = WorkAssignment(
        proposal=WorkProposalEnum.ADAPTED_EQUESTRIAN_SPORTS,
        condition=WorkConditionEnum.REGULAR,
        sede=SedeEnum.HLP,
        days=[DayEnum.TUESDAY, DayEnum.THURSDAY],
        professor_or_therapist_id=4,
        conductor_id=4,
        track_assistant_id=4,
        horse_id=4
    )
    work_assignment3 = WorkAssignment(
        proposal=WorkProposalEnum.RECREATIONAL_ACTIVITIES,
        condition=WorkConditionEnum.REGULAR,
        sede=SedeEnum.OTHER,
        days=[DayEnum.TUESDAY, DayEnum.THURSDAY],
        professor_or_therapist_id=5,
        conductor_id=6,
        track_assistant_id=7,
        horse_id=6
    )
    db.session.add_all([work_assignment1, work_assignment2, work_assignment3])

    jockey1 = JockeyAmazon(
        first_name="María",
        last_name="González",
        dni="87654321",
        birth_date=date(1996, 5, 15),
        birthplace="Ciudad 1",
        has_scholarship=True,
        scholarship_observations="Observaciones de beca",
        has_disability=True,
        disability_diagnosis=DisabilityDiagnosisEnum.AUTISM_SPECTRUM_DISORDER,
        disability_other=None,
        disability_type=DisabilityTypeEnum.MENTAL,
        has_family_assignment=True,
        family_assignment_type=FamilyAssignmentEnum.UNIVERSAL_WITH_DISABLED_CHILD,
        has_pension=True,
        pension_type=PensionEnum.NATIONAL,
        pension_details="Detalles de la pensión",
        social_security="Obra Social 1",
        social_security_number="123456789",
        has_curatorship=False,
        curatorship_observations=None,
        school_institution=school1,
        current_grade_year="5to Año",
        school_observations="Observaciones escolares",
        professionals="Profesionales involucrados",
        family_members=[family_member1],
        work_assignment=work_assignment1
    )

    jockey2 = JockeyAmazon(
        first_name="José",
        last_name="López",
        dni="98765432",
        birth_date=date(1998, 8, 22),
        birthplace="Ciudad 2",
        has_scholarship=False,
        scholarship_observations=None,
        has_disability=True,
        disability_diagnosis=DisabilityDiagnosisEnum.INTELLECTUAL_DISABILITY,
        disability_other=None,
        disability_type=DisabilityTypeEnum.MENTAL,
        has_family_assignment=False,
        family_assignment_type=None,
        has_pension=False,
        pension_type=None,
        pension_details=None,
        social_security="Obra Social 2",
        social_security_number="987654321",
        has_curatorship=True,
        curatorship_observations="Curador: Juan Pérez",
        school_institution=school2,
        current_grade_year="2do Año",
        school_observations="Observaciones escolares de José",
        professionals="Profesional 1, Profesional 2",
        family_members=[family_member2],
        work_assignment=work_assignment2
    )

    jockey3 = JockeyAmazon(
        first_name="Emilia",
        last_name="Romero",
        dni="45678901",
        birth_date=date(2000, 12, 10),
        birthplace="Springfield",
        has_scholarship=True,
        scholarship_observations="Beca completa por excelencia académica",
        has_disability=False,
        disability_diagnosis=None,
        disability_other=None,
        disability_type=None,
        has_family_assignment=True,
        family_assignment_type=FamilyAssignmentEnum.UNIVERSAL_WITH_CHILD,
        has_pension=False,
        pension_type=None,
        pension_details=None,
        social_security="Obra Social 3",
        social_security_number="456789012",
        has_curatorship=False,
        curatorship_observations=None,
        school_institution=school3,
        current_grade_year="4to Año",
        school_observations="Alumno destacada en actividades extracurriculares",
        professionals="Psicopedagoga, Fonoaudióloga",
        family_members=[family_member3],
        work_assignment=work_assignment3
    )

    db.session.add_all([jockey1, jockey2, jockey3])


def seed_charges():
    charges = [
        Charge(
            id=1,
            date_of_charge=date(2023, 1, 1),
            amount=100.0,
            payment_method=PaymentMethodEnum.CREDIT_CARD,
            employee_id=1,
            jya_id=1,
            observations="First charge",
            inserted_at=date(2023, 1, 1),
            updated_at=date(2023, 1, 1)
        ),
        Charge(
            id=2,
            date_of_charge=date(2023, 2, 1),
            amount=200.0,
            payment_method=PaymentMethodEnum.CASH,
            employee_id=2,
            jya_id=1,
            observations="Second charge",
            inserted_at=date(2023, 2, 1),
            updated_at=date(2023, 2, 1)
        ),
        Charge(
            id=3,
            date_of_charge=date(2023, 3, 1),
            amount=150.0,
            payment_method=PaymentMethodEnum.DEBIT_CARD,
            employee_id=3,
            jya_id=2,
            observations="Third charge",
            inserted_at=date(2023, 3, 1),
            updated_at=date(2023, 3, 1)
        ),
    ]

    db.session.add_all(charges)
