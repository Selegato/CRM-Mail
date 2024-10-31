import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

from app.config import SMTP_PASSWORD, SMTP_PORT, SMTP_SERVER, SMTP_USER
from app.logger import logger


def send_mail(
    form_data: dict,
    attachments: List[str],
    platform: str,
    tenant_data: dict,
    mail_to: str,
) -> bool:
    """Send mail with attachments"""
    try:
        msg = MIMEMultipart()
        msg["From"] = SMTP_USER
        msg["To"] = mail_to

        # Mail subject
        msg["Subject"] = (
            f'{platform} - {tenant_data["name"]} - {form_data["contactReason"]} - {form_data["name"]} {form_data["lastName"]}'
        )
        # attachments
        for file_path in attachments:
            with open(file_path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={os.path.basename(file_path)}",
                )
                msg.attach(part)
        # template html
        body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    table {{
                    font-family: arial, sans-serif;
                    border-collapse: collapse;
                    width: 100%;
                    }}
                    td, th {{
                    border: 1px solid #dddddd;
                    text-align: left;
                    padding: 8px;
                    }}
                    tr:nth-child(even) {{
                    background-color: #dddddd;
                    }}
                </style>
            </head>
            <body>
                <h2>New Contact</h2>
                <table>
                    <tr>
                        <th>ID:</th>
                        <td>{form_data['documentNumber']}</td>
                    </tr>
                    <tr>
                        <th>Name:</th>
                        <td>{form_data['name']}</td>
                    </tr>
                    <tr>
                        <th>Last Name:</th>
                        <td>{form_data['lastName']}</td>
                    </tr>
                    <tr>
                        <th>E-mail:</th>
                        <td>{form_data['email']}</td>
                    </tr>
                    <tr>
                        <th>Phone:</th>
                        <td>{form_data['phone']}</td>
                    </tr>
                    <tr>
                        <th>Mobile:</th>
                        <td>{form_data['celPhone']}</td>
                    </tr>
                    <tr>
                        <th>Reason:</th>
                        <td>{form_data['contactReason']}</td>
                    </tr>
                    <tr>
                        <th>Related:</th>
                        <td>{form_data['contactRelatedTo']}</td>
                    </tr>
                    <tr>
                        <th>Message:</th>
                        <td>{form_data['description']}</td>
                    </tr>
                </table>
            </body>
            </html>
            """

        msg.attach(MIMEText(body, "html"))

        # Send to server
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, msg["To"], msg.as_string())

        # Delete attachments
        for file_path in attachments:
            try:
                os.remove(file_path)
            except Exception as e:
                logger.error(
                    f"Error to remove file {form_data['email']} para {msg['To']}", e
                )
        # return true to update the database
        return True
    except Exception as e:
        logger.error(f"Error to send email {form_data['email']}", e)
        return False
