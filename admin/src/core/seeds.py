import random
from enum import Enum
from faker import Faker
from src.core.module.charges.models import Charge, PaymentMethodEnum
from src.core.database import db
from src.core.module.user.models import User
from src.core.module.auth.models import Role, Permission, RolePermission
from src.core.module.auth.data import PermissionEnum, RoleEnum
from src.core.module.employee.models import Employee
from src.core.module.payment.models import Payment
from src.core.module.payment.data import PaymentTypeEnum
from src.core.module.employee.data import (
    JobPositionEnum,
    JobConditionEnum,
    ProfessionsEnum,
)
from src.core.bcrypt import bcrypt
from src.core.module.equestrian.models import Horse, JAEnum
from src.core.module.jockey_amazon.models import (
    JockeyAmazon,
    SchoolInstitution,
    FamilyMember,
    WorkAssignment,
)
from src.core.module.jockey_amazon.data import (
    DisabilityDiagnosisEnum,
    DisabilityTypeEnum,
    FamilyAssignmentEnum,
    PensionEnum,
    WorkProposalEnum,
    WorkConditionEnum,
    SedeEnum,
    DayEnum,
    EducationLevelEnum,
)

class SeedEntity(Enum):
    """Represents the standarized entities names to be seeded
    """
    HORSES = "horses"
    JOCKEYS = "jockeys"
    EMPLOYEES = "employees"
    PAYMENTS = "payments"
    CHARGES = "charges"

seeding_config = {
    "counts": {
        SeedEntity.HORSES: 31,
        SeedEntity.JOCKEYS: 31,
        SeedEntity.EMPLOYEES: 31,
        SeedEntity.PAYMENTS: 15,
        SeedEntity.CHARGES: 15,
    },
    "chances": {
        # 0, 25, 50, 75, 100
        "creating_archived": 25,
    }
}


fake: Faker = Faker("es-AR")
generated_dnis = set()


def generate_unique_dni():
    while True:
        dni = str(random.randint(10000000, 99999999))
        if dni not in generated_dnis:
            generated_dnis.add(dni)
            return dni


def seed_all(app):
    """
    Seeds all the necessary data into the database.

    This function runs the seeding process for accounts, employees, the equestrian module,
    payments, jockey amazons, and charges, committing changes to the database at appropriate points.

    Args:
        app (Flask): The Flask application instance used to get the application context.
    """

    with app.app_context():
        seed_accounts()
        seed_employees(seeding_config["counts"][SeedEntity.EMPLOYEES])
        seed_horses(seeding_config["counts"][SeedEntity.HORSES])
        seed_jockeys_amazons(seeding_config["counts"][SeedEntity.JOCKEYS])
        seed_payments(seeding_config["counts"][SeedEntity.PAYMENTS])
        seed_charges(seeding_config["counts"][SeedEntity.CHARGES])
        db.session.commit()


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
    roles = [Role(name=role.value) for role in RoleEnum]

    db.session.add_all(roles)


def seed_permissions():
    """
    Seeds the permissions in the database.

    Permissions are added based on the `PermissionEnum` enumeration.
    """
    permissions = [Permission(name=permission.value) for permission in PermissionEnum]

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
        # Administración - Reportes
        RolePermission(role_id=4, permission_id=26),
        RolePermission(role_id=4, permission_id=27),
        # Técnica - Reportes
        RolePermission(role_id=1, permission_id=26),
        RolePermission(role_id=1, permission_id=27),
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
        User(
            email=email,
            alias=alias,
            password=encrypt(password),
            role_id=role_id,
            system_admin=system_admin,
        )
        for email, alias, password, role_id, system_admin in [
            ("tecnica@gmail.com", "Tecnica", "Tecnica123", 1, False),
            ("ecuestre@gmail.com", "Ecuestre", "Ecuestre123", 2, False),
            ("voluntariado@gmail.com", "Voluntario/a", "Voluntariado123", 3, False),
            (
                "administracion@gmail.com",
                "Administrador",
                "Administracion123",
                4,
                False,
            ),
            (
                "sysadmin@gmail.com",
                "Administrador del Sistema",
                "Sysadmin123",
                None,
                True,
            ),
        ]
    ]

    db.session.add_all(users)


def seed_employees(n: int):
    """
    Seeds employees in the database.

    This function creates several employees with different professions, positions, and conditions.
    """
    print("Seeding employees")
    employees = []
    creating_archived_chances = seeding_config.get("chances").get("creating_archived")
    for _ in range(n):
        employee = Employee(
            email=fake.email(),
            name=fake.first_name(),
            lastname=fake.last_name(),
            dni=generate_unique_dni(),
            profession=fake.random_element(elements=[e.name for e in ProfessionsEnum]),
            position=fake.random_element(elements=[e.name for e in JobPositionEnum]),
            job_condition=fake.random_element(
                elements=[e.name for e in JobConditionEnum]
            ),
            start_date=fake.date_between(start_date="-5y", end_date="today"),
            end_date=(
                fake.date_between(start_date="today", end_date="+5y")
                if fake.random.choice([True, False])
                else None
            ),
            health_insurance=fake.company(),
            affiliate_number=fake.unique.random_number(digits=8),
            is_active=fake.random.choice([True, False]),
            is_deleted=fake.boolean(chance_of_getting_true=creating_archived_chances),
            street=fake.street_name(),
            number=fake.building_number(),
            department=fake.random_element(
                elements=[None, fake.word()]
            ),  # Optional field
            locality=fake.city(),
            province=fake.province(),
            country_code=fake.country_code(),
            area_code=fake.random_int(min=1, max=300),
            phone=fake.msisdn()[:10],
            emergency_contact_name=fake.name(),
            emergency_contact_phone=fake.phone_number(),
        )
        employees.append(employee)

    print("Commiting employees")
    db.session.bulk_save_objects(employees)
    db.session.commit()


def seed_horses(n: int):
    """
    Seeds horse data in the database.

    This function creates several horses with various attributes and assigned facilities.
    """
    horses = []
    creating_archived_chances = seeding_config.get("chances").get("creating_archived")
    print("Seeding horses")
    for _ in range(n):
        horse = Horse(
            name=fake.language_name(),
            birth_date=fake.date_of_birth(minimum_age=1, maximum_age=30),
            sex=fake.random_element(elements=["M", "F"]),
            breed=fake.random_element(
                elements=["Arabian", "Thoroughbred", "Quarter Horse", "Appaloosa"]
            ),
            coat=fake.random_element(elements=["Bay", "Chestnut", "Black", "Gray", "White"]),
            is_donation=fake.random.choice([True, False]),
            admission_date=fake.date_between(start_date="-5y", end_date="today"),
            assigned_facility=fake.company(),
            ja_type=fake.random_element(elements=[e.name for e in JAEnum]),
            is_archived=fake.boolean(chance_of_getting_true=creating_archived_chances),
        )
        horses.append(horse)

    print("Commiting horses")
    db.session.bulk_save_objects(horses)
    db.session.commit()


def seed_school_institutions(jockey):
    """Create fake school institutions for a given jockey."""
    school = SchoolInstitution(
        name=fake.company(),
        street=fake.street_name(),
        number=fake.building_number(),
        locality=fake.city(),
        province=fake.province(),
        phone_country_code=fake.random_int(min=1, max=300),
        phone_area_code=fake.random_int(min=1, max=300),
        phone_number=fake.phone_number()[:15],
        jockey_amazon_id=jockey.id,
    )
    db.session.add(school)


def seed_work_assignment(jockey: JockeyAmazon):
    """
    Seeds work assignments in the database.

    This function creates several work assignments with various attributes.
    """

    work_assignment = WorkAssignment(
        proposal=fake.random_element(elements=[e.name for e in WorkProposalEnum]),
        condition=fake.random_element(elements=[e.name for e in WorkConditionEnum]),
        sede=fake.random_element(elements=[e.name for e in SedeEnum]),
        days=fake.random_elements(
            elements=[e.name for e in DayEnum],
            unique=True,
            length=fake.random_int(min=1, max=7),
        ),
        jockey_amazon=jockey,
    )
    # Add work assignments to the session and commit
    db.session.add(work_assignment)
    db.session.commit()


def seed_family_members(jockey: JockeyAmazon):
    """
    Seeds family members in the database.

    This function creates several family members with various attributes.
    """
    family_members = []
    family_members_number = random.randint(1, 2)
    for _ in range(family_members_number):
        family_member = FamilyMember(
            relationship=fake.random_element(
                elements=["Madre", "Padre", "Madre", "Hermano/a", "Esposa/o", "Tutor"]
            ),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            dni=fake.unique.random_number(digits=8),
            street=fake.street_name(),
            number=fake.building_number(),
            department=fake.random_element(
                elements=[None, fake.word()]
            ),  # Optional field
            locality=fake.municipality(),
            province=fake.province(),
            phone_country_code=fake.random_int(min=1, max=99),
            phone_area_code=fake.random_int(min=1, max=300),
            phone_number=fake.msisdn()[:10],
            email=fake.email(),
            education_level=fake.random_element(
                elements=[e.name for e in EducationLevelEnum]
            ),
            occupation=fake.random_element(
                elements=["Profesor", "Ingeniero", "Desempleado", "Artista", "Abogado"]
            ),
            jockey_amazon_id=jockey.id,
        )
        family_members.append(family_member)

    # Add family members to the session and commit
    db.session.bulk_save_objects(family_members)
    db.session.commit()


def seed_jockeys_amazons(num_jockeys=10):
    """Seed a specified number of JockeyAmazon instances."""
    print("Seeding jockeys and amazons")
    for _ in range(num_jockeys):
        has_scholarship = fake.boolean()
        has_disability = fake.boolean()
        has_curatorship = fake.boolean()
        creating_archived_chances = seeding_config.get("chances").get("creating_archived")
        jockey = JockeyAmazon(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            dni=generate_unique_dni(),
            birth_date=fake.date_of_birth(),
            birthplace=fake.city(),
            has_debts=fake.boolean(chance_of_getting_true=0),
            has_scholarship=has_scholarship,
            scholarship_percentage=fake.random.uniform(0, 100) if has_scholarship else None,
            scholarship_observations=fake.text(max_nb_chars=200) if has_scholarship else None,
            has_disability=has_disability,
            disability_diagnosis=fake.random_element(elements=[e.name for e in DisabilityDiagnosisEnum]) if has_disability else None,
            disability_other=fake.sentence() if has_disability and fake.boolean() else None,
            disability_type=fake.random_element(elements=[e.name for e in DisabilityTypeEnum]) if has_disability else None,
            has_curatorship=has_curatorship,
            curatorship_observations=fake.text(max_nb_chars=200) if has_curatorship else None, 
            school_institution=None,
            current_grade_year=fake.word(),
            school_observations=fake.text(max_nb_chars=50),
            has_family_assignment=fake.boolean(),
            family_assignment_type=fake.random_element(elements=[e.name for e in FamilyAssignmentEnum]),
            has_pension=fake.boolean(),
            pension_type=fake.random_element(elements=[e.name for e in PensionEnum]),
            pension_details=fake.sentence() if fake.boolean() else None,
            social_security=fake.company_suffix(),
            social_security_number=fake.msisdn()[:10],
            street=fake.street_name(),
            number=fake.building_number(),
            department=fake.word(),
            locality=fake.municipality(),
            province=fake.province(),
            emergency_contact_name=fake.name(),
            emergency_contact_phone=fake.phone_number()[:15],
            country_code=fake.country_code(),
            area_code=fake.random_int(min=1, max=300),
            phone=fake.msisdn()[:10],
            is_deleted=fake.boolean(chance_of_getting_true=creating_archived_chances)
        )
        db.session.add(jockey)

    print("Committing jockeys and amazons")
    db.session.commit()
    print("Seeding jockeys and amazons related entities")
    # Seed related data
    for jockey in db.session.query(JockeyAmazon).all():
        seed_school_institutions(jockey)
        seed_family_members(jockey)
        seed_work_assignment(jockey)

    print("Commiting...")
    # Commit all changes to the database
    db.session.commit()


def seed_charges(num_entries=3):
    """
    Seed the database with initial charge data.

    This function creates a specified number of Charge objects with predefined data
    generated using Faker and inserts them into the database. Each Charge object includes
    details such as the date of charge, amount, payment method, employee ID, jockey/amazon ID,
    observations, and timestamps for insertion and update.

    Example:
        seed_charges(num_entries=5)

    Returns:
        None
    """

    charges = []

    for _ in range(num_entries):
        charges.append(
            Charge(
                date_of_charge=fake.date_between(start_date="-1y", end_date="today"),
                amount=round(
                    fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2
                ),
                payment_method=fake.random_element(
                    elements=[e.name for e in PaymentMethodEnum]
                ),
                employee_id=fake.random_int(min=1, max=20),
                jya_id=fake.random_int(min=1, max=20),
                observations=fake.sentence(),
                inserted_at=fake.date_time_this_year(),
                updated_at=fake.date_time_this_year(),
            )
        )

    db.session.bulk_save_objects(charges)
    db.session.commit()


def seed_payments(num_entries=5):
    """
    Seed the database with initial payment data.

    This function creates a specified number of Payment objects with predefined data
    generated using Faker and inserts them into the database. Each Payment object includes
    details such as the amount, payment date, payment type, description, beneficiary ID,
    and timestamps for insertion and update.

    Example:
        seed_payments(num_entries=10)

    Returns:
        None
    """

    payments = []
    creating_archived_chances = seeding_config.get("chances").get("creating_archived")
    for _ in range(num_entries):
        payments.append(
            Payment(
                amount=round(
                    fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2
                ),
                payment_date=fake.date_between(start_date="-1y", end_date="today"),
                payment_type=fake.random_element(
                    elements=[e.value for e in PaymentTypeEnum]
                ),
                description=fake.sentence(),
                is_archived=fake.boolean(chance_of_getting_true=creating_archived_chances),
                inserted_at=fake.date_time_this_year(),
                updated_at=fake.date_time_this_year(),
                beneficiary_id=fake.random_int(min=1, max=20),
            )
        )

    db.session.bulk_save_objects(payments)
    db.session.commit()
