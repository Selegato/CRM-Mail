import mimetypes
import os
from datetime import datetime
from typing import List, Optional

from app.backgroud_tasks import process_mail
from app.config import ALLOWED_MIME_TYPES, MAX_FILES, MAX_SIZE, TEMP_DIR
from app.db import get_data_tenant, save_contact_database
from app.logger import logger
from app.models import ContactForm
from fastapi import APIRouter, BackgroundTasks, File, Form, Header, UploadFile
from fastapi.responses import JSONResponse
from pydantic import ValidationError

router = APIRouter()


@router.get("/")
async def get_contact() -> JSONResponse:
    """Health check"""
    return JSONResponse(content={"message": "API WORKING"})


@router.get("/api/app/contact/tenantName")
async def get_contact_reason(tenantId: str = Header(...)) -> JSONResponse:
    """Get tenant name by tenantId"""
    try:
        tenant = get_data_tenant(tenantId)
        if tenant:
            return JSONResponse(content=tenant["name"])
        else:
            logger.warning(f"Warning invalid Tenant: {tenantId}")
            return JSONResponse(content={"error": "Invalid tenantId."}, status_code=404)
    except Exception as e:
        logger.critical(f"Error getting tenant name DB ERROR")
        return JSONResponse(
            content={"error": "Error getting tenant name."}, status_code=500
        )


@router.get("/api/app/contact/reasons")
async def get_contact_reason(tenantId: str = Header(...)) -> JSONResponse:
    """Get contact reasons by tenantId"""
    try:
        tenant = get_data_tenant(tenantId)
        if tenant:
            return JSONResponse(content=tenant["reason"])
        else:
            logger.warning(f"Warning invalid Tenant: {tenantId}")
            return JSONResponse(content={"error": "Invalid tenantId."}, status_code=404)
    except Exception as e:
        logger.critical(f"Error getting tenant name DB ERROR")
        return JSONResponse(
            content={"error": "Error getting Reasons."}, status_code=500
        )


@router.get("/api/app/contact/related")
async def get_related_reason(tenantId: str = Header(...)) -> JSONResponse:
    """Get related reasons by tenantId"""
    try:
        tenant = get_data_tenant(tenantId)
        if tenant:
            return JSONResponse(content=tenant["related_to"])
        else:
            logger.warning(f"Warning invalid Tenant: {tenantId}")
            return JSONResponse(content={"error": "Invalid tenantId."}, status_code=404)
    except Exception as e:
        logger.critical(f"Error getting tenant name DB ERROR")
        return JSONResponse(
            content={"error": "Error getting related."}, status_code=500
        )


@router.post("/api/app/contact")
async def create_contact(
    background_tasks: BackgroundTasks,
    documentNumber: str = Form(...),
    documentType: str = Form(...),
    name: str = Form(...),
    lastName: str = Form(...),
    email: str = Form(...),
    phone: Optional[str] = Form(None),
    celPhone: str = Form(...),
    isPrime: bool = Form(...),
    isMobile: bool = Form(...),
    description: str = Form(...),
    contactReason: str = Form(...),
    contactRelatedTo: str = Form(...),
    files: List[UploadFile] = File(None),
    tenantId: str = Header(...),
) -> JSONResponse:
    """recieve a new contact with or without files, save the files in a temp folder,
    save the contact to database and send an email with files and delete files from db
    """
    raw_data = {
        "documentNumber": documentNumber,
        "documentType": documentType,
        "name": name,
        "lastName": lastName,
        "email": email,
        "phone": phone,
        "celPhone": celPhone,
        "isPrime": isPrime,
        "isMobile": isMobile,
        "description": description,
        "contactReason": contactReason,
        "contactRelatedTo": contactRelatedTo,
        "tenantId": tenantId,
    }

    try:
        form_data = ContactForm(
            documentNumber=documentNumber,
            documentType=documentType,
            name=name,
            lastName=lastName,
            email=email,
            phone=phone,
            celPhone=celPhone,
            isPrime=isPrime,
            isMobile=isMobile,
            description=description,
            contactReason=contactReason,
            contactRelatedTo=contactRelatedTo,
            tenantId=tenantId,
        )
        # add created_at field
        form_data.created_at = datetime.now().isoformat()
        # save files in temp folder
        file_paths = []
        # check for empty list
        if files and isinstance(files, list):
            # check for max files
            if len(files) > MAX_FILES:
                raise ValueError(
                    f"Numero maximo de arquivos excedido, limite: {MAX_FILES}"
                )
            # check size and mime type
            for file in files:
                mime_type, _ = mimetypes.guess_type(file.filename)
                if file.filename and file.size > 0 and mime_type in ALLOWED_MIME_TYPES:
                    if file.size > MAX_SIZE:
                        raise ValueError(f"File too big: {MAX_SIZE}")
                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                    new_filename = f"{timestamp}_{file.filename}"
                    file_path = os.path.join(TEMP_DIR, new_filename)
                    with open(file_path, "wb") as f:
                        f.write(await file.read())
                    file_paths.append(file_path)
                else:
                    logger.error(f"Invalid file received: {file.filename}, {raw_data}")

        print("->TEST new contact")

        # dump model to dict
        form_data = form_data.model_dump()

        # save contact to database
        try:
            contact_id = save_contact_database(form_data)
            print(f"->TEST contact saved: {contact_id}")
        except Exception as e:
            logger.error(f"Error saving contact: {form_data} - {e}")
            raise Exception("Error saving contact")
        # case the contact is saved, set responde 200
        response = JSONResponse(
            content={"message": "contact received"}, status_code=200
        )

        # send email with files
        background_tasks.add_task(process_mail, form_data, file_paths, contact_id)

        return response

    # validation errors
    except ValidationError as e:
        error_message = e.errors()[0]["msg"]
        logger.error(f"Validation error: {raw_data} - {error_message}")
        return JSONResponse(
            content={"Validation error": error_message}, status_code=500
        )

    # value errors (ex: max number files, file too big)
    except ValueError as e:
        logger.error(f"Value error: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=400)

    # error server/DB
    except Exception as e:
        logger.critical(f"Error DB create_contact post", e)
        return JSONResponse(
            content={
                "error saving": "an error occurred when trying to save the contact"
            },
            status_code=500,
        )
