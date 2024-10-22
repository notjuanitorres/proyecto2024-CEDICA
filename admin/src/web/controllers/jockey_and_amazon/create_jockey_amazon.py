from flask import Blueprint, render_template, request, url_for, redirect, flash, session
from dependency_injector.wiring import inject, Provide
from src.web.helpers.auth import check_user_permissions
from src.core.container import Container
from src.core.module.jockey_amazon import (
    # JockeyAmazonCreateForm,
    GeneralInformationForm,
    HealthInformationForm,
    FamilyInformationForm,
    SchoolInformationForm,
    WorkAssignmentForm,
    JockeyAmazonMapper as Mapper,
    AbstractJockeyAmazonRepository,
    EducationLevelEnum,
)
from src.web.helpers.create import check_creation_in_process

create_jockey_amazon_bp = Blueprint(
    "create",
    __name__,
    url_prefix="/crear",
)

@inject
def add_jockey(
    create_form,
    jockeys: AbstractJockeyAmazonRepository = Provide[
        Container.jockey_amazon_repository
    ],
):
    created_jockey = jockeys.add(Mapper.to_entity(create_form))
    session["create_ja"] = None
    flash("Jockey/Amazon creado con éxito!", "success")
    return redirect(
        url_for("jockey_amazon_bp.show_jockey", jockey_id=created_jockey.id)
    )


@create_jockey_amazon_bp.route("/", methods=["GET"])
@check_user_permissions(permissions_required=["jockey_amazon_new"])
@inject
def init():
    session["create_ja"] = {
        "general_information": {},
        "health_information": {},
        "family_information": {},
        "school_information": {},
        "work_assignment_information": {},
    }
    return redirect(url_for("jockey_amazon_bp.create.create_general_information"))


# Step one
@create_jockey_amazon_bp.route("/informacion-general", methods=["GET", "POST"])
def create_general_information():
    general_information = GeneralInformationForm()

    if general_information.validate_on_submit():
        session["create_ja"]["general_information"] = general_information.data
        return redirect(url_for("jockey_amazon_bp.create.create_health_information"))

    return render_template("create/general_information.html", general_form=general_information)


# Step two
@create_jockey_amazon_bp.route("/informacion-salud", methods=["GET", "POST"])
@check_creation_in_process("create_ja")
def create_health_information():
    health_information = HealthInformationForm()

    if health_information.validate_on_submit():
        session["create_ja"]["health_information"] = health_information.data
        return redirect(url_for("jockey_amazon_bp.create.create_family_information"))

    return render_template("create/health_information.html", health_form=health_information)


# Step three
@create_jockey_amazon_bp.route("/informacion-familia", methods=["GET", "POST"])
@check_creation_in_process("create_ja")
def create_family_information():
    family_information = FamilyInformationForm()

    # TODO: Check family members creation
    # if family_information.validate_on_submit():
    #     session["create_ja"]["family_information"] = family_information.data
    #     return redirect(url_for("jockey_amazon_bp.create.create_school_information"))
    if request.method == "GET":
        return render_template(
            "create/family_information.html",
            family_form=family_information,
            EducationLevelEnum=EducationLevelEnum,
        )

    return redirect(url_for("jockey_amazon_bp.create.create_school_information"))


# Step four
@create_jockey_amazon_bp.route("/informacion-escuela", methods=["GET", "POST"])
@check_creation_in_process("create_ja")
def create_school_information():
    school_information = SchoolInformationForm()

    if school_information.validate_on_submit():
        session["create_ja"]["school_information"] = school_information.data
        return redirect(url_for("jockey_amazon_bp.create.create_work_assignment"))

    return render_template("create/school_information.html", education_form=school_information)


# Step five
@create_jockey_amazon_bp.route('/asignacion-trabajo', methods=['GET', 'POST'])
@check_creation_in_process("create_ja")
def create_work_assignment():
    assignment_information = WorkAssignmentForm()

    if assignment_information.validate_on_submit():
        session["create_ja"]["work_assignment_information"] = assignment_information.data
        return add_jockey(create_form=session["create_ja"])

    return render_template('create/work_assignments_information.html', assignments_form=assignment_information)
