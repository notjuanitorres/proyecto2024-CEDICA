from flask import Blueprint, render_template, request, url_for, redirect, flash
from dependency_injector.wiring import inject, Provide
from src.web.helpers.auth import check_user_permissions
from src.core.container import Container
from src.core.module.jockey_amazon import (
    JockeyAmazonCreateForm,
)
from src.core.module.jockey_amazon.models import EducationLevelEnum
from src.core.module.jockey_amazon.mappers import JockeyAmazonMapper as Mapper
from src.core.module.jockey_amazon.repositories import AbstractJockeyAmazonRepository
from src.core.module.employee.repositories import EmployeeRepository
from src.core.module.equestrian.repositories import EquestrianRepository


create_jockey_amazon_bp = Blueprint(
    "create_jockey_amazon",
    __name__,
    template_folder="./templates/jockey_amazon/create/",
    url_prefix="/crear",
)


@create_jockey_amazon_bp.route("/", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["jockey_amazon_new"])
@inject
def init(
    jockeys: AbstractJockeyAmazonRepository = Provide[
        Container.jockey_amazon_repository
    ],
    employees: EmployeeRepository = Provide[Container.employee_repository],
    equestrian: EquestrianRepository = Provide[Container.equestrian_repository],
):
    create_form = JockeyAmazonCreateForm()

    create_form.organization_information.work_assignments.professor_or_therapist_id.choices = [
        (t.id, f"{t.name} {t.lastname}") for t in employees.get_therapist()
    ]

    create_form.organization_information.work_assignments.conductor_id.choices = [
        (r.id, f"{r.name} {r.lastname}") for r in employees.get_rider()
    ]

    create_form.organization_information.work_assignments.track_assistant_id.choices = [
        (a.id, f"{a.name} {a.lastname}") for a in employees.get_track_auxiliary()
    ]

    create_form.organization_information.work_assignments.horse_id.choices = [
        (h.id, h.name) for h in equestrian.get_horses()
    ]

    if request.method == "POST":
        return add_jockey(create_form=create_form, jockeys=jockeys)

    return render_template(
        "./jockey_amazon/create_jockey_amazon.html",
        form=create_form,
        EducationLevelEnum=EducationLevelEnum,
    )


@inject
def add_jockey(
    create_form,
    jockeys: AbstractJockeyAmazonRepository = Provide[
        Container.jockey_amazon_repository
    ],
    employees: EmployeeRepository = Provide[Container.employee_repository],
    equestrian: EquestrianRepository = Provide[Container.equestrian_repository],
):

    if not create_form.validate_on_submit():
        print(create_form.data)
        print(create_form.errors)
        therapists = employees.get_therapist()
        riders = employees.get_rider()
        track_auxiliaries = employees.get_track_auxiliary()
        horses = equestrian.get_horses()
        return render_template(
            "./jockey_amazon/create_jockey_amazon.html",
            form=create_form,
            EducationLevelEnum=EducationLevelEnum,
            therapists=therapists,
            riders=riders,
            track_auxiliaries=track_auxiliaries,
            horses=horses,
        )
    created_jockey = jockeys.add(Mapper.to_entity(create_form.data))
    flash("Jockey/Amazon creado con éxito!", "success")

    return redirect(
        url_for("jockey_amazon_bp.show_jockey", jockey_id=created_jockey.id)
    )
