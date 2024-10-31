from typing import List

from app.db import get_data_tenant, set_mail_send
from app.logger import logger
from app.mailing import send_mail
from app.rules_send_mail import regra_de_envio
from app.utils import add_mascara_cpf, add_mascara_phone


def process_mail(form_data: dict, file_paths: List[str], contact_id: str) -> None:
    """Process data before sending mail"""
    form_data["phone"] = add_mascara_phone(form_data["phone"])
    form_data["celPhone"] = add_mascara_phone(form_data["celPhone"])
    form_data["documentNumber"] = add_mascara_cpf(form_data["documentNumber"])

    # load data from tenant
    try:
        tenant_data = get_data_tenant(form_data["tenantId"])
    except Exception as e:
        logger.critical(f"Error consulting DB inside email job")
        return

    # set platform based on form data
    platform = "App" if form_data["isMobile"] else "Site"

    # set mail_to based on tenant rules
    mail_to = regra_de_envio(form_data, tenant_data)

    # send mail
    if send_mail(form_data, file_paths, platform, tenant_data, mail_to):
        print("TEST -> Mail sent successfully")
        # set mail send on db
        set_mail_send(contact_id)
        print("TEST -> Mail set DB")
