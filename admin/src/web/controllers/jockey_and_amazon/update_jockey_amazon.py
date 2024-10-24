"""
update_jockey_amazon.py

This module defines the routes and view functions for updating jockey and amazon records,
including assigning and unassigning employees and horses. It leverages Flask, Flask-WTF,
and dependency injection for form handling and validation.
"""

from flask import Blueprint, render_template, request, url_for, redirect, flash
from dependency_injector.wiring import inject, Provide
from src.web.helpers.auth import check_user_permissions
from src.core.container import Container
from src.core.module.equestrian import (
    AbstractEquestrianRepository,
    HorseAssignSearchForm,
    HorseAssignSelectForm,
)
from src.core.module.employee import (
    AbstractEmployeeRepository,
    EmployeeMiniSearchForm,
    EmployeeSelectForm,
    JobPositionEnum as Jobs,
)
from src.core.module.jockey_amazon import (
    GeneralInformationForm,
    HealthInformationForm,
    # FamilyInformationForm,
    SchoolInformationForm,
    WorkAssignmentForm,
    JockeyAmazonMapper as Mapper,
    AbstractJockeyAmazonRepository,
    EducationLevelEnum,
)

update_jockey_amazon_bp = Blueprint(
    "update",
    __name__,
    url_prefix="/editar",
)


@inject
def update_jockey(
    jockey_id: int,
    update_form,
    jockeys: AbstractJockeyAmazonRepository = Provide[
        Container.jockey_amazon_repository
    ],
):
    """
    Update the information of a jockey or amazon.

    Args:
        jockey_id (int): The ID of the jockey or amazon to update.
        update_form: The form containing the updated information.
        jockeys (AbstractJockeyAmazonRepository): The repository for jockey and amazon data.

    Returns:
        A rendered template with the update form if validation fails, or a redirect to the jockey's detail page if successful.
    """
    jockey = jockeys.get_by_id(jockey_id)
    if not update_form.validate_on_submit():
        return render_template(
            "./jockey_amazon/update_jockey_amazon.html", form=update_form, jockey=jockey
        )

    # if not jockeys.update(jockey_id, Mapper.flat_form(update_form.data)):
    #     flash("No se ha podido actualizar al Jockey/Amazon", "warning")
    #     return render_template("./jockey_amazon/update_jockey_amazon.html")

    flash("El Jockey/Amazon ha sido actualizado éxitosamente ")
    return redirect(url_for("jockey_amazon_bp.show_jockey", jockey_id=jockey_id))


@inject
def link_employee(
    jockey_id: int,
    job_positions,
    template: str,
    flash_message: str,
    page: int = 1,
    employee_repository: AbstractEmployeeRepository = Provide[
        Container.employee_repository
    ],
    jockeys: AbstractJockeyAmazonRepository = Provide[
        Container.jockey_amazon_repository
    ],
):
    """
    Link an employee to a jockey or amazon.

    Args:
        jockey_id (int): The ID of the jockey or amazon.
        job_positions: The job positions to link.
        template (str): The template to render.
        flash_message (str): The flash message to display upon successful linking.
        page (int): The page number for pagination.
        employee_repository (AbstractEmployeeRepository): The repository for employee data.
        jockeys (AbstractJockeyAmazonRepository): The repository for jockey and amazon data.

    Returns:
        A rendered template with the search and select forms if validation fails, or a redirect to the jockey's detail page if successful.
    """
    jockey = jockeys.get_by_id(jockey_id)
    if not jockey:
        flash("No se ha encontrado al Jockey/Amazona solicitado", "warning")
        return redirect(url_for("jockey_amazon_bp.get_jockeys"))

    if jockey.is_deleted:
        flash("No se pueden asignar empleados a un Jockey/Amazona archivado", "warning")
        return redirect(url_for("jockey_amazon_bp.show_jockey", jockey_id=jockey_id))

    page = request.args.get("page", type=int, default=1)
    searched_employee = EmployeeMiniSearchForm(request.args)
    selected_employee = EmployeeSelectForm()
    employees = employee_repository.get_active_employees(job_positions, page=page)
    if request.method == "POST":
        if not (
            selected_employee.submit_employee.data and selected_employee.validate()
        ):
            return render_template(
                "./jockey_amazon/update/link/link_professor.html",
                jockey_amazon=jockey,
                employees=employees,
                search_form=searched_employee,
                select_form=selected_employee,
            )
        jockey_id = jockey.id
        employee_id = selected_employee.selected_item.data
        jockeys.assign_employee(jockey_id, employee_id, job_positions[0])
        flash(
            flash_message,
            "success",
        )
        return redirect(url_for("jockey_amazon_bp.show_jockey", jockey_id=jockey.id))
    if searched_employee.submit_search.data and searched_employee.validate():
        employees = employee_repository.get_active_employees(
            job_positions, page=page, search=searched_employee.search_text.data
        )

    return render_template(
        template,
        jockey_amazon=jockey,
        employees=employees,
        search_form=searched_employee,
        select_form=selected_employee,
    )


@update_jockey_amazon_bp.route("/<int:jockey_id>", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["jockey_amazon_update"])
@inject
def edit_jockey(
    jockey_id: int,
    jockeys: AbstractJockeyAmazonRepository = Provide[
        Container.jockey_amazon_repository
    ],
):
    """
    Edit the information of a jockey or amazon.

    Args:
        jockey_id (int): The ID of the jockey or amazon to edit.
        jockeys (AbstractJockeyAmazonRepository): The repository for jockey and amazon data.

    Returns:
        A rendered template with the edit forms if validation fails, or a redirect to the jockey's detail page if successful.
    """
    jockey = Mapper.from_entity(jockeys.get_by_id(jockey_id))
    if not jockey:
        flash("No se ha encontrado al Jockey/Amazona solicitado", "warning")
        return redirect(url_for("jockey_amazon_bp.get_jockeys"))

    if jockey.get("is_deleted"):
        flash("No se puede editar un Jockey/Amazona archivado", "warning")
        return redirect(url_for("jockey_amazon_bp.show_jockey", jockey_id=jockey_id))

    general_form = GeneralInformationForm(
        data=jockey.get("general_information"), current_dni=jockey.get("general_information").get("dni")
    )
    health_form = HealthInformationForm(data=jockey.get("health_information"))
    education_form = SchoolInformationForm(data=jockey.get("school_information"))
    # family_form = FamilyInformationForm(data=jockey.get("family_information"))
    assignment_form = WorkAssignmentForm(data=jockey.get("organization_work"))

    if request.method == "POST":
        if "general_submit" in request.form and general_form.validate():
            update = GeneralInformationForm.general_info_to_flat(general_form)
            if jockeys.update(jockey_id, update):
                flash("Información general actualizada con éxito", "success")

        elif "health_submit" in request.form and health_form.validate():
            update = HealthInformationForm.health_info_to_flat(health_form)
            if jockeys.update(jockey_id, update):
                flash("Información de salud actualizada con éxito", "success")

        elif "school_submit" in request.form and education_form.validate():
            update = SchoolInformationForm.school_info_to_flat(education_form)
            if jockeys.update_school_information(jockey_id, update):
                flash("Información escolar actualizada con éxito", "success")

        elif "assignment_submit" in request.form and assignment_form.validate():
            update = WorkAssignmentForm.work_assignment_to_flat(assignment_form)
            if jockeys.update_assignments(jockey_id, update):
                flash("Información de asignaciones de trabajo actualizada con éxito", "success")

        # elif family_form.submit.data and family_form.validate():
    #            # return update_jockey(forms=update_forms, jockey_id=jockey_id)

    return render_template(
        "./jockey_amazon/update_jockey_amazon.html",
        general_form=general_form,
        health_form=health_form,
        education_form=education_form,
        # family_form=family_form,
        assignments_form=assignment_form,
        jockey=jockey,
        EducationLevelEnum=EducationLevelEnum,
    )


@update_jockey_amazon_bp.route(
    "/<int:jockey_id>/asignar-profesor", methods=["GET", "POST"]
)
@check_user_permissions(permissions_required=["jockey_amazon_update"])
def assign_professor_or_therapist(jockey_id: int):
    """
    Assign a professor or therapist to a jockey or amazon.

    Args:
        jockey_id (int): The ID of the jockey or amazon.
    
    Returns:
        A rendered template with the search and select forms if validation fails, or a redirect to the jockey's detail page if successful.
    """
    page = request.args.get("page", type=int, default=1)
    job_positions = [Jobs.TERAPEUTA.name, Jobs.PROFESOR_EQUITACION.name]
    template = "./jockey_amazon/update/link/link_professor.html"
    return link_employee(
        jockey_id=jockey_id, page=page, job_positions=job_positions,
        template=template, flash_message="Se ha asociado correctamente al Jockey/Amazona con un Terapeuta/Profesor"
    )


@update_jockey_amazon_bp.route(
    "/<int:jockey_id>/quitar-profesor-terapeuta", methods=["GET"]
)
@check_user_permissions(permissions_required=["jockey_amazon_update"])
@inject
def unlink_professor(
    jockey_id: int,
    jockeys: AbstractJockeyAmazonRepository = Provide[
        Container.jockey_amazon_repository
    ],
):
    """
    Unlink a professor or therapist from a jockey or amazon.

    Args:
        jockey_id (int): The ID of the jockey or amazon.
        jockeys (AbstractJockeyAmazonRepository): The repository for jockey and amazon data.

    Returns:
        A redirect to the jockey's detail page.
    """
    jockey = jockeys.get_by_id(jockey_id)
    jockeys.unassign_employee(jockey_id, link_to=Jobs.TERAPEUTA.name)
    flash(
        f"Se ha desasociado correctamente al profesor/terapeuta de {jockey.first_name}",
        "warning",
    )
    return redirect(url_for("jockey_amazon_bp.show_jockey", jockey_id=jockey.id))


@update_jockey_amazon_bp.route(
    "/<int:jockey_id>/asignar-auxiliar-pista", methods=["GET", "POST"]
)
@check_user_permissions(permissions_required=["jockey_amazon_update"])
def assign_track_assistant(jockey_id: int):
    """
    Assign a track assistant to a jockey or amazon.

    Args:
        jockey_id (int): The ID of the jockey or amazon.
    
    Returns:
        A rendered template with the search and select forms if validation fails, or a redirect to the jockey's detail page if successful.
    """
    page = request.args.get("page", type=int, default=1)
    job_positions = [Jobs.AUXILIAR_PISTA.name]
    template = "./jockey_amazon/update/link/link_assistant.html"

    return link_employee(
        jockey_id=jockey_id, page=page, job_positions=job_positions,
        template=template, flash_message="Se ha asociado correctamente al Jockey/Amazona con un auxiliar de pista"
    )


@update_jockey_amazon_bp.route(
    "/<int:jockey_id>/quitar-asistente-pista",
    methods=["GET", "POST"],
)
@check_user_permissions(permissions_required=["jockey_amazon_update"])
@inject
def unlink_track_assistant(
    jockey_id: int,
    jockeys: AbstractJockeyAmazonRepository = Provide[
        Container.jockey_amazon_repository
    ],
):
    """
    Unlink a track assistant from a jockey or amazon.

    Args:
        jockey_id (int): The ID of the jockey or amazon.
        jockeys (AbstractJockeyAmazonRepository): The repository for jockey and amazon data.

    Returns:
        A redirect to the jockey's detail page.
    """
    jockey = jockeys.get_by_id(jockey_id)
    jockeys.unassign_employee(jockey_id, link_to=Jobs.AUXILIAR_PISTA.name)
    flash(
        f"Se ha desasociado correctamente al Auxiliar de Pista de {jockey.first_name}",
        "warning",
    )
    return redirect(url_for("jockey_amazon_bp.show_jockey", jockey_id=jockey.id))


@update_jockey_amazon_bp.route(
    "/<int:jockey_id>/asignar-conductor", methods=["GET", "POST"]
)
@check_user_permissions(permissions_required=["jockey_amazon_update"])
def assign_conductor(jockey_id: int):
    """
    Assign a conductor to a jockey or amazon.

    Args:
        jockey_id (int): The ID of the jockey or amazon.
    
    Returns:
        A rendered template with the search and select forms if validation fails, or a redirect to the jockey's detail page if successful.
    """
    page = request.args.get("page", type=int, default=1)
    job_positions = [Jobs.CONDUCTOR.name]
    template = "./jockey_amazon/update/link/link_conductor.html"

    return link_employee(
        jockey_id=jockey_id, page=page, job_positions=job_positions, template=template,
        flash_message="Se ha asociado correctamente al Jockey/Amazona con un Conductor"
    )


@update_jockey_amazon_bp.route(
    "/<int:jockey_id>/quitar-conductor",
    methods=["GET", "POST"],
)
@check_user_permissions(permissions_required=["jockey_amazon_update"])
@inject
def unlink_conductor(
    jockey_id: int,
    jockeys: AbstractJockeyAmazonRepository = Provide[
        Container.jockey_amazon_repository
    ],
):
    """
    Unlink a conductor from a jockey or amazon.

    Args:
        jockey_id (int): The ID of the jockey or amazon.
        jockeys (AbstractJockeyAmazonRepository): The repository for jockey and amazon data.

    Returns:
        A redirect to the jockey's detail page.
    """
    jockey = jockeys.get_by_id(jockey_id)
    jockeys.unassign_employee(jockey_id, link_to=Jobs.CONDUCTOR.name)
    flash(
        f"Se ha desasociado correctamente al Conductor de {jockey.first_name}",
        "warning",
    )
    return redirect(url_for("jockey_amazon_bp.show_jockey", jockey_id=jockey.id))


@update_jockey_amazon_bp.route(
    "/<int:jockey_id>/asignar-caballo", methods=["GET", "POST"]
)
@check_user_permissions(permissions_required=["jockey_amazon_update"])
@inject
def assign_horse(
    jockey_id: int,
    page: int = 1,
    equestrian: AbstractEquestrianRepository = Provide[Container.equestrian_repository],
    jockeys: AbstractJockeyAmazonRepository = Provide[
        Container.jockey_amazon_repository
    ],
):
    """
    Assign a horse to a jockey or amazon.

    Args:
        jockey_id (int): The ID of the jockey or amazon.
        page (int): The page number for pagination.
        equestrian (AbstractEquestrianRepository): The repository for equestrian data.
        jockeys (AbstractJockeyAmazonRepository): The repository for jockey and amazon data.

    Returns:
        A rendered template with the search and select forms if validation fails, or a redirect to the jockey's detail page if successful.
    """
    page = request.args.get("page", type=int, default=1)
    searched_horse = HorseAssignSearchForm(request.args)
    selected_horse = HorseAssignSelectForm()
    jockey = jockeys.get_by_id(jockey_id)
    horses = equestrian.get_active_horses(page=page)
    if request.method == "POST":
        if not (selected_horse.submit_horse.data and selected_horse.validate()):
            return render_template(
                "./jockey_amazon/update/link/link_horse.html",
                jockey_amazon=jockey,
                horses=horses,
                search_form=searched_horse,
                select_form=selected_horse,
            )
        jockey_id = jockey.id
        horse_id = selected_horse.selected_item.data
        jockeys.assign_horse(jockey_id, horse_id)
        flash(
            "Se ha asociado correctamente al Jockey/Amazona con un caballo",
            "success",
        )
        return redirect(url_for("jockey_amazon_bp.show_jockey", jockey_id=jockey.id))

    if searched_horse.submit_search.data and searched_horse.validate():
        horses = equestrian.get_active_horses(
            page=page,
            search=searched_horse.search_text.data,
            activity=searched_horse.filter_activity.data,
        )

    return render_template(
        "./jockey_amazon/update/link/link_horse.html",
        jockey_amazon=jockey,
        horses=horses,
        search_form=searched_horse,
        select_form=selected_horse,
    )


@update_jockey_amazon_bp.route(
    "/<int:jockey_id>/quitar-caballo",
    methods=["GET", "POST"],
)
@check_user_permissions(permissions_required=["jockey_amazon_update"])
@inject
def unlink_horse(
    jockey_id: int,
    jockeys: AbstractJockeyAmazonRepository = Provide[
        Container.jockey_amazon_repository
    ],
):
    """
    Unlink a horse from a jockey or amazon.

    Args:
        jockey_id (int): The ID of the jockey or amazon.
        jockeys (AbstractJockeyAmazonRepository): The repository for jockey and amazon data.

    Returns:
        A redirect to the jockey's detail page.
    """
    jockey = jockeys.get_by_id(jockey_id)
    jockeys.unassign_horse(jockey_id)
    flash(
        f"Se ha desasociado correctamente al caballo de {jockey.first_name}",
        "warning",
    )
    return redirect(url_for("jockey_amazon_bp.show_jockey", jockey_id=jockey.id))
