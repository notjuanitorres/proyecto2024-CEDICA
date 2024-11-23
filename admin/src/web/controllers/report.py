from flask import Blueprint, render_template, request
from dependency_injector.wiring import inject, Provide
from src.core.container import Container
from src.core.module.payment.repositories import AbstractPaymentRepository
from src.core.module.charges.repositories import AbstractChargeRepository
from src.core.module.user.repositories import AbstractUserRepository
from src.core.module.jockey_amazon.repositories import AbstractJockeyAmazonRepository
from src.web.helpers.auth import check_user_permissions

report_bp = Blueprint(
    "report_bp", __name__, template_folder="../templates/report", url_prefix="/reportes"
)


@report_bp.route("/", methods=["GET"])
@check_user_permissions(['report_index'])
@inject
def index(
    charge_repository: AbstractChargeRepository = Provide[Container.charges_repository],
    jockey_amazon_repository: AbstractJockeyAmazonRepository = Provide[Container.jockey_amazon_repository],
):
    # 1. KPIs
    total_jya = jockey_amazon_repository.total_jya()
    current_month_income = charge_repository.current_month_income()
    # 2. Gráfico de Propuestas Elegidas (para gráfico de torta)
    proposals_data = jockey_amazon_repository.proposals_data()

    # 3. Gráficos de Clientes
    certified_jya = jockey_amazon_repository.certified_jya()
    uncertified_jya = total_jya - certified_jya

    # Gráfico por Tipo de Cliente
    disability_types_data = jockey_amazon_repository.disability_types_data()

    # Gráfico por Categoría de Cliente
    disability_data = jockey_amazon_repository.disability_data()

    # Pasar los datos al template
    return render_template('report/index.html', 
                           total_jya=total_jya,
                           current_month_income=current_month_income,
                           proposals_data=proposals_data,
                           certified_jya=certified_jya,
                           disability_types_data=disability_types_data,
                           disability_data=disability_data,
                           uncertified_jya=uncertified_jya)


@report_bp.route("/ranking_propousals", methods=["GET"])
# @report_bp.route("/ranking_propuestas", methods=["GET"])
@check_user_permissions(['report_show'])
@inject
def reports_proposals(
    charge_repository: AbstractChargeRepository = Provide[Container.charges_repository],
    jockey_amazon_repository: AbstractJockeyAmazonRepository = Provide[Container.jockey_amazon_repository],
):
    # 1. KPIs
    total_jya = jockey_amazon_repository.total_jya()
    current_month_income = charge_repository.current_month_income()
    proposals_data = jockey_amazon_repository.proposals_data()
    proposals_data = sorted(proposals_data, key=lambda x: x[1], reverse=True)
    # Lógica para generar el reporte de ranking de propuestas de trabajo más solicitadas
    return render_template("report/reports_proposals.html", 
                            proposals_data=proposals_data,
                            total_jya = total_jya,
                            current_month_income=current_month_income
                            )


@report_bp.route("/personas_adeudan", methods=["GET"])
@check_user_permissions(['report_show'])
@inject
def reports_debtors(
    charge_repository: AbstractChargeRepository = Provide[Container.charges_repository],
    jockey_amazon_repository: AbstractJockeyAmazonRepository = Provide[Container.jockey_amazon_repository],
):
     # 1. KPIs
    total_jya = jockey_amazon_repository.total_jya()
    current_month_income = charge_repository.current_month_income()
    #obtener los deudores
    debtors = jockey_amazon_repository.debtors()
    # Lógica para generar el reporte de personas que adeudan pagos
    return render_template("report/reports_debtors.html", 
                           debtors=debtors,
                           total_jya = total_jya,
                             current_month_income=current_month_income)


@report_bp.route("/historico_cobros", methods=["GET"])
@check_user_permissions(['report_show'])
@inject
def reports_charges(
    charge_repository: AbstractChargeRepository = Provide[Container.charges_repository],
    jockey_amazon_repository: AbstractJockeyAmazonRepository = Provide[Container.jockey_amazon_repository],
):
    # 1. KPIs
    total_jya = jockey_amazon_repository.total_jya()
    current_month_income = charge_repository.current_month_income()
    payments_data = charge_repository.last_payments_data()
    return render_template("report/reports_charges.html", 
                           payments_data=payments_data,   
                           total_jya = total_jya,
                             current_month_income=current_month_income )

    # Lógica para generar el reporte histórico de cobros en un rango de fechas asociado a una persona
    return render_template("report/historico_cobros.html")
