from flask import Blueprint, render_template, request, url_for, redirect, flash
from dependency_injector.wiring import inject, Provide
from src.web.helpers.auth import check_user_permissions
from src.core.container import Container
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


@update_jockey_amazon_bp.route("/<int:jockey_id>", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["jockey_amazon_update"])
@inject
def edit_jockey(
    jockey_id: int,
    jockeys: AbstractJockeyAmazonRepository = Provide[
        Container.jockey_amazon_repository
    ],
):
    jockey = Mapper.from_entity(jockeys.get_by_id(jockey_id))
    if not jockey:
        return redirect(url_for("jockey_amazon_bp.get_jockeys"))

    general_form = GeneralInformationForm(data=jockey.get("general_information"))
    health_form = HealthInformationForm(data=jockey.get("health_information"))
    education_form = SchoolInformationForm(data=jockey.get("school_information"))
    # family_form = FamilyInformationForm(data=jockey.get("family_information"))
    assignment_form = WorkAssignmentForm(data=jockey.get("organization_work"))
    
    if request.method == "POST":
        if "general_submit" in request.form and general_form.validate():
            update = GeneralInformationForm.general_info_to_flat(general_form)
            if jockeys.update(jockey_id, update):
                flash("Informacion general actualizada con exito", "success")

        elif "health_submit" in request.form and health_form.validate():
            update = HealthInformationForm.health_info_to_flat(health_form)
            if jockeys.update(jockey_id, update):
                flash("Informacion general actualizada con exito", "success")

        elif "school_submit" in request.form and education_form.validate():
            print("submitted")
            update = SchoolInformationForm.school_info_to_flat(education_form)
            if jockeys.update_school_information(jockey_id, update):
                flash("Informacion escolar actualizada con exito", "success")

        elif "assignment_submit" in request.form and assignment_form.validate():
            update = WorkAssignmentForm.work_assignment_to_flat(assignment_form)
            print(update)
            if jockeys.update_assignments(jockey_id, update):
                flash("Informacion general actualizada con exito", "success")
        
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


@inject
def update_jockey(
    jockey_id: int,
    update_form,
    jockeys: AbstractJockeyAmazonRepository = Provide[
        Container.jockey_amazon_repository
    ],
):
    jockey = jockeys.get_by_id(jockey_id)
    if not update_form.validate_on_submit():
        return render_template(
            "./jockey_amazon/update_jockey_amazon.html", form=update_form, jockey=jockey
        )

    # if not jockeys.update(jockey_id, Mapper.flat_form(update_form.data)):
    #     flash("No se ha podido actualizar al Jockey/Amazon", "warning")
    #     return render_template("./jockey_amazon/update_jockey_amazon.html")

    flash("El Jockey/Amazon ha sido actualizado exitosamente ")
    return redirect(url_for("jockey_amazon_bp.show_jockey", jockey_id=jockey_id))
