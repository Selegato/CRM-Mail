import asyncio
import os
import random
import re

import aiohttp
import requests
from faker import Faker
from nanoid import generate


def only_numbers(text):
    return re.sub(r"[\D\s]", "", text)


def phone_generator():
    return "".join([str(random.randint(0, 9)) for _ in range(11)])


def gera_payload_testes_dados_aleatorios():
    tenant_ids = [
        "4863b71f-f97b-42fb-8a8c-8f94f63452e4",  # Storepapers
        "869ea6a0-3a27-4632-9e42-2ee431a89565",  # Donations
        "dc78a062-2895-4db2-b4d5-4690096117b7",  # SuperStore
    ]

    headers = {"tenantId": random.choice(tenant_ids)}

    fake = Faker("pt_BR")

    # standard payload
    payload = {
        "documentNumber": only_numbers(fake.cpf()),
        "documentType": "1",
        "name": fake.first_name(),
        "lastName": fake.last_name(),
        "email": fake.email(),
        "phone": phone_generator(),
        "celPhone": phone_generator(),
        "isPrime": "false",
        "isMobile": random.choice(["false", "true"]),
        "description": fake.text(),
        "contactReason": [],
        "contactRelatedTo": [],
    }
    # random file attachment
    attach_file = random.choice([True, False])
    files = None
    if attach_file:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        test_folder = os.path.join(current_dir, "img")
        all_files = os.listdir(test_folder)
        selected_file = random.choice(all_files)
        file_path = os.path.join(test_folder, selected_file)

        file_extension = os.path.splitext(selected_file)[1]
        random_filename = f"{generate(size=5)}{file_extension}"

        files = [("files", (random_filename, open(file_path, "rb"), "image/png"))]

    if headers["tenantId"] == "dc78a062-2895-4db2-b4d5-4690096117b7":  # Storepapers
        payload["isPrime"] = random.choice(["false", "true"])
        reason_store_paper = [
            "Info",
            "Request",
            "Suggestion",
            "Compliment",
            "Complaint",
        ]
        payload["contactReason"] = random.choice(reason_store_paper)
        related_store_paper = [
            "Credit Card",
            "Physical Store",
            "E-commerce",
            "App",
            "Super Pay",
        ]
        payload["contactRelatedTo"] = random.choice(related_store_paper)

        return payload, files, headers

    elif headers["tenantId"] == "869ea6a0-3a27-4632-9e42-2ee431a89565":  # Donations
        reason_donations = ["Info", "Request", "Suggestion", "Complaint"]
        payload["contactReason"] = random.choice(reason_donations)
        related_donations = ["Donations", "Visit", "Meeting"]
        payload["contactRelatedTo"] = random.choice(related_donations)
        return payload, files, headers
    elif headers["tenantId"] == "4863b71f-f97b-42fb-8a8c-8f94f63452e4":  # Storepapers
        reason_store_paper = ["Info", "Request", "Complaint"]
        payload["contactReason"] = random.choice(reason_store_paper)
        related_store_paper = ["Credit Card", "Physical Store"]
        payload["contactRelatedTo"] = random.choice(related_store_paper)
        return payload, files, headers


def envia_payload_sync(payload, files, headers):
    """send payload to backend sync"""
    URL = "http://localhost:8000/api/app/contact"
    response = requests.request("POST", URL, headers=headers, data=payload, files=files)
    return response


def testes_sync(NUMERO_TESTES):
    """Run sync tests"""
    for _ in range(NUMERO_TESTES):
        payload, files, headers = gera_payload_testes_dados_aleatorios()
        response = envia_payload_sync(payload, files, headers)
        print(response.status_code, response.text)


async def envia_payload_async(payload, files, headers):
    """async send payload to backend"""
    URL = "http://localhost:8000/api/app/contact"
    async with aiohttp.ClientSession() as session:
        if not files:
            async with session.post(URL, headers=headers, data=payload) as response:
                response_text = await response.text()
                return response.status, response_text
        else:
            form_data = aiohttp.FormData()

            # Trata o payload

            for key, value in payload.items():
                form_data.add_field(key, value)

            # Trata o arquivo
            if isinstance(files, list):
                for file_tuple in files:
                    # Pega os elementos dda tupla
                    field_name = file_tuple[0]  # 'files'
                    file_info = file_tuple[1]  # (filename, file_object, content_type)

                    filename = file_info[0]  # '4.jpg'
                    file_object = file_info[1]  # BufferedReader object
                    content_type = file_info[2]  # 'image/png'

                    # Lê o conteúdo do arquivo
                    file_content = file_object.read()

                    # Adiciona o arquivo ao form_data
                    form_data.add_field(
                        field_name,
                        file_content,
                        filename=filename,
                        content_type=content_type,
                    )
            else:
                raise TypeError("files deve ser uma lista de tuples")

            async with session.post(URL, headers=headers, data=form_data) as response:
                response_text = await response.text()
                return response.status, response_text


async def testes_async(NUMERO_TESTES):
    """Run async tests"""
    tasks = []
    for _ in range(NUMERO_TESTES):
        payload, files, headers = gera_payload_testes_dados_aleatorios()
        tasks.append(envia_payload_async(payload, files, headers))

    for task in asyncio.as_completed(tasks):
        response = await task
        print(response)


if __name__ == "__main__":
    # number of tests
    NUMERO_TESTES = 25
    modo_teste = "async"  # Alterar SYNC ou ASYNC

    if modo_teste == "sync":
        testes_sync(NUMERO_TESTES)
    elif modo_teste == "async":
        asyncio.run(testes_async(NUMERO_TESTES))
