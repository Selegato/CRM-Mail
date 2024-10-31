import os


def create_temp_dir() -> str:
    """Create a temp folder to save files"""
    TEMP_DIR = os.path.join(os.getcwd(), "temp")
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    return TEMP_DIR


def add_mascara_phone(phone):
    """add mask to phone number"""
    if not phone:
        return ""
    try:
        return f"({phone[:2]}) {phone[2:7]}-{phone[7:]}"
    except Exception as e:
        print(f"Error formatting phone number {phone} {e}")
        return phone


def add_mascara_cpf(cpf: str) -> str:
    """add mask to cpf number"""
    if not cpf or len(cpf) != 11:
        raise ValueError("CPF inválido")
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
