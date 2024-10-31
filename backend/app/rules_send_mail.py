def regra_prime_super_geral(contact_form: dict, tenant_data: dict) -> str:
    """Rules to send email based on tenant data and contact form data SUPERSTORE prime>superpay>crm"""
    if contact_form["isPrime"] == True:
        return tenant_data["mail_to_prime"]
    if contact_form["contactRelatedTo"] == "Super Pay":
        return tenant_data["mail_to_super_pay"]
    else:
        return tenant_data["mail_to_crm"]


def regra_cartao_geral(contact_form: dict, tenant_data: dict) -> str:
    """"""
    if contact_form["contactReason"] == "Complaint":
        return tenant_data["mail_to_complaint"]
    else:
        return tenant_data["mail_to_crm"]


def regra_de_envio(form_data: dict, tenant_data: dict) -> str:
    """Rules to send email based on tenant data and contact form data"""
    if tenant_data["name"] == "SuperStore":
        mail_to = regra_prime_super_geral(form_data, tenant_data)
        return mail_to
    if tenant_data["name"] in ["Donations", "Store Papers"]:
        return regra_cartao_geral(form_data, tenant_data)
    else:
        return tenant_data["mail_to_sac"]
