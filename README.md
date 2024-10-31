# Multi-Tenant Email Contact Service

## Project Overview

This is a multi-tenant email contact service developed to simplify customer service (CRM) via email. The application uses React with Material UI and Vite for the front-end, FastAPI for the back-end, MongoDB as the database, and Docker to simulate the execution environment.

## Objective

Create a multi-tenant contact application for SAC via email, allowing different companies to use the same system while maintaining data independence and specific configurations for each tenant.

## General User Flow

1. The user clicks on a contact link on the tenant's website.
2. They are redirected to the contact page, where they can fill out the form and attach images if necessary.
3. Upon submitting the form, the user receives a submission confirmation or an error notification.

# Requirements and Features

## Front-End

1. **Reception of Encoded Data:**
   The front-end receives tenant and client data encoded as a payload in the link to facilitate dynamic loading of information.

2. **API Queries:**
   Based on the tenantID extracted from the payload, the front-end makes three calls to the back-end to obtain:
   - Tenant name
   - Contact reasons
   - Tenant-specific contact reasons

3. **Conditional Filling:**
   - If the client is logged in, the data (CPF, Email, First Name, Last Name, Phone, Mobile) is automatically filled and locked for editing.
   - If the client is not logged in, all fields must be filled manually.

4. **Field Validations:**
   All fields have specific validations with error messages to guide the user.

5. **Form Submission:**
   The form data is sent to the back-end API for processing.


## Back-End

1. **Data Revalidation:**
   The back-end revalidates all data received from the front-end and returns error messages if there are inconsistencies.

2. **Creation Date Attribute:**
   Adds the `Created_at` field to the form to record the submission date.

3. **File Validation:**
   If there are attached files, the back-end validates the extensions and size before saving them in a temporary folder.

4. **Database Saving:**
   The data is saved in MongoDB, and a success response (status 200) is sent to the front-end. In case of failure, an error is sent to the front-end, requesting the client to contact SAC through another method.

5. **Background Processing:**
   A background task is initiated to process and send the email:
   - Formats the data (masks fields when necessary).
   - Retrieves tenant-specific information and sets the `platform` variable.
   - Executes tenant-specific business logic to determine the destination email.

6. **Email Sending:**
   The email sending function is called with the necessary data and a specific HTML template.
   If the sending is successful, the `mail_sent_at` field is updated in the database for record-keeping.



## Technologies Used
- **Front-End:** React, Material UI, Vite
- **Back-End:** FastAPI
- **Database:** MongoDB
- **Containerization:** Docker and Docker Compose

## Project Setup

### Prerequisites
- Docker

### Installation Instructions:
1. Clone the repository and navigate to the root folder:
    ```sh
    git clone https://github.com/Selegato/CRM-Mail
    cd CRM-Mail
    docker-compose up --build
    ```

### Health Check Tests:
- **MongoDB Database:**
    - URL: [http://localhost:8081/](http://localhost:8081/)
    - User: `admin`
    - Password: `pass`
    - Verify that the QA database is present with the `tenants` collection.

- **API:**
    - URL: [http://localhost:8000/](http://localhost:8000/)
    - Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

- **Simulated Email Service:**
    - URL: [http://localhost:8025/](http://localhost:8025/)

- **Front-End:**
    - URL: [http://localhost:3000/](http://localhost:3000/)
    - Note: The message "Page cannot be loaded" will be displayed until the payload is loaded.

## Manual Testing
For manual testing, there are three configured tenants. Each can be tested with complete data (simulating a logged-in user) or basic data (simulating a non-logged-in user).

### Simulation with Logged-In and Non-Logged-In Users:
- Copy the generated link for each tenant, paste it into the browser, fill in the fields, and submit the form.
- Check the simulated email service at [http://localhost:8025/](http://localhost:8025/) to confirm sending and receiving.

### Testing via Postman:
- Directly test the API endpoints with Postman by sending various payloads and verifying the API responses for different scenarios.


### tenant 1

4863b71f-f97b-42fb-8a8c-8f94f63452e4 - papers company

## Basic data encoded

http://localhost:3000/?payload=eyJ0ZW5hbnRJZCI6IjQ4NjNiNzFmLWY5N2ItNDJmYi04YThjLThmOTRmNjM0NTJlNCIsInRpdGxlIjoiQ29udGFjdC11cyIsImFsZXJ0U3VjY2Vzc01lc3NhZ2UiOiJNZW5zYWdlbSBlbnZpYWRhIGNvbSBzdWNlc3NvISIsImFsZXJ0RXJyb3JNZXNzYWdlIjoiT3BzLiBBbGdvIGRldSBlcnJhZG8uIFRlbnRlIG5vdmFtZW50ZSBlbSBhbGd1bnMgaW5zdGFudGVzLiIsImlzUHJpbWUiOmZhbHNlLCJpc01vYmlsZSI6ZmFsc2UsInByaW1hcnlDb2xvciI6IiMwMEY5YzQifQ==

{"tenantId":"4863b71f-f97b-42fb-8a8c-8f94f63452e4","title":"Contact-us","alertSuccessMessage":"Mensagem enviada com sucesso!","alertErrorMessage":"Ops. Algo deu errado. Tente novamente em alguns instantes.","isPrime":false,"isMobile":false,"primaryColor":"#00F9c4"}

## Full data encoded

http://localhost:3000/?payload=eyJ0ZW5hbnRJZCI6IjQ4NjNiNzFmLWY5N2ItNDJmYi04YThjLThmOTRmNjM0NTJlNCIsInRpdGxlIjoiQ29udGFjdC11cyIsImFsZXJ0U3VjY2Vzc01lc3NhZ2UiOiJNZW5zYWdlbSBlbnZpYWRhIGNvbSBzdWNlc3NvISIsImFsZXJ0RXJyb3JNZXNzYWdlIjoiT3BzLiBBbGdvIGRldSBlcnJhZG8uIFRlbnRlIG5vdmFtZW50ZSBlbSBhbGd1bnMgaW5zdGFudGVzLiIsImRvY3VtZW50TnVtYmVyIjoiOTExOTgxMTg4ODEiLCJuYW1lIjoiSm9obiIsImxhc3ROYW1lIjoiRG9lIiwiZW1haWwiOiJKb2huLmRvZUBnbWFpbC5jb20iLCJwaG9uZSI6IiIsImNlbFBob25lIjoiKzU1MDE4ODEyMzQ4NTEiLCJpc1ByaW1lIjpmYWxzZSwiaXNNb2JpbGUiOmZhbHNlLCJwcmltYXJ5Q29sb3IiOiIjMDA2OWI0In0=

{"tenantId":"4863b71f-f97b-42fb-8a8c-8f94f63452e4","title":"Contact-us","alertSuccessMessage":"Mensagem enviada com sucesso!","alertErrorMessage":"Ops. Algo deu errado. Tente novamente em alguns instantes.","documentNumber":"91198118881","name":"John","lastName":"Doe","email":"John.doe@gmail.com","phone":"","celPhone":"+5501881234851","isPrime":false,"isMobile":false,"primaryColor":"#0069b4"}

### tenant 2
869ea6a0-3a27-4632-9e42-2ee431a89565 - Donations

## Basic data encoded

http://localhost:3000/?payload=eyJ0ZW5hbnRJZCI6Ijg2OWVhNmEwLTNhMjctNDYzMi05ZTQyLTJlZTQzMWE4OTU2NSIsInRpdGxlIjoiQ29udGFjdC11cyIsImFsZXJ0U3VjY2Vzc01lc3NhZ2UiOiJNZW5zYWdlbSBlbnZpYWRhIGNvbSBzdWNlc3NvISIsImFsZXJ0RXJyb3JNZXNzYWdlIjoiT3BzLiBBbGdvIGRldSBlcnJhZG8uIFRlbnRlIG5vdmFtZW50ZSBlbSBhbGd1bnMgaW5zdGFudGVzLiIsImlzUHJpbWUiOmZhbHNlLCJpc01vYmlsZSI6ZmFsc2UsInByaW1hcnlDb2xvciI6IiNGRjAwMDAifQ==

{"tenantId":"869ea6a0-3a27-4632-9e42-2ee431a89565","title":"Contact-us","alertSuccessMessage":"Mensagem enviada com sucesso!","alertErrorMessage":"Ops. Algo deu errado. Tente novamente em alguns instantes.","isPrime":false,"isMobile":false,"primaryColor":"#FF0000"}

## Full data encoded

http://localhost:3000/?payload=eyJ0ZW5hbnRJZCI6Ijg2OWVhNmEwLTNhMjctNDYzMi05ZTQyLTJlZTQzMWE4OTU2NSIsInRpdGxlIjoiQ29udGFjdC11cyIsImFsZXJ0U3VjY2Vzc01lc3NhZ2UiOiJNZW5zYWdlbSBlbnZpYWRhIGNvbSBzdWNlc3NvISIsImFsZXJ0RXJyb3JNZXNzYWdlIjoiT3BzLiBBbGdvIGRldSBlcnJhZG8uIFRlbnRlIG5vdmFtZW50ZSBlbSBhbGd1bnMgaW5zdGFudGVzLiIsImRvY3VtZW50TnVtYmVyIjoiOTExOTgxMTg4ODEiLCJuYW1lIjoiSm9obiIsImxhc3ROYW1lIjoiRG9lIiwiZW1haWwiOiJKb2huLmRvZUBnbWFpbC5jb20iLCJwaG9uZSI6IiIsImNlbFBob25lIjoiKzU1MDE4ODEyMzQ4NTEiLCJpc1ByaW1lIjpmYWxzZSwiaXNNb2JpbGUiOmZhbHNlLCJwcmltYXJ5Q29sb3IiOiIjRkYwMDAwIn0=

{"tenantId":"869ea6a0-3a27-4632-9e42-2ee431a89565","title":"Contact-us","alertSuccessMessage":"Mensagem enviada com sucesso!","alertErrorMessage":"Ops. Algo deu errado. Tente novamente em alguns instantes.","documentNumber":"91198118881","name":"John","lastName":"Doe","email":"John.doe@gmail.com","phone":"","celPhone":"+5501881234851","isPrime":false,"isMobile":false,"primaryColor":"#FF0000"}

### tenant 3
dc78a062-2895-4db2-b4d5-4690096117b7 - superstore

## basic data encoded

http://localhost:3000/?payload=eyJ0ZW5hbnRJZCI6ImRjNzhhMDYyLTI4OTUtNGRiMi1iNGQ1LTQ2OTAwOTYxMTdiNyIsInRpdGxlIjoiQ29udGFjdC11cyIsImFsZXJ0U3VjY2Vzc01lc3NhZ2UiOiJNZW5zYWdlbSBlbnZpYWRhIGNvbSBzdWNlc3NvISIsImFsZXJ0RXJyb3JNZXNzYWdlIjoiT3BzLiBBbGdvIGRldSBlcnJhZG8uIFRlbnRlIG5vdmFtZW50ZSBlbSBhbGd1bnMgaW5zdGFudGVzLiIsImlzUHJpbWUiOmZhbHNlLCJpc01vYmlsZSI6ZmFsc2UsInByaW1hcnlDb2xvciI6IiNmOWQwMDAifQ==

{"tenantId":"dc78a062-2895-4db2-b4d5-4690096117b7","title":"Contact-us","alertSuccessMessage":"Mensagem enviada com sucesso!","alertErrorMessage":"Ops. Algo deu errado. Tente novamente em alguns instantes.","isPrime":false,"isMobile":false,"primaryColor":"#f9d000"}

## full data encoded

http://localhost:3000/?payload=eyJ0ZW5hbnRJZCI6ImRjNzhhMDYyLTI4OTUtNGRiMi1iNGQ1LTQ2OTAwOTYxMTdiNyIsInRpdGxlIjoiQ29udGFjdC11cyIsImFsZXJ0U3VjY2Vzc01lc3NhZ2UiOiJNZW5zYWdlbSBlbnZpYWRhIGNvbSBzdWNlc3NvISIsImFsZXJ0RXJyb3JNZXNzYWdlIjoiT3BzLiBBbGdvIGRldSBlcnJhZG8uIFRlbnRlIG5vdmFtZW50ZSBlbSBhbGd1bnMgaW5zdGFudGVzLiIsImRvY3VtZW50TnVtYmVyIjoiOTExOTgxMTg4ODEiLCJuYW1lIjoiSm9obiIsImxhc3ROYW1lIjoiRG9lIiwiZW1haWwiOiJKb2huLmRvZUBnbWFpbC5jb20iLCJwaG9uZSI6IiIsImNlbFBob25lIjoiKzU1MDQ4ODEyNzM4NTEiLCJpc1ByaW1lIjpmYWxzZSwiaXNNb2JpbGUiOmZhbHNlLCJwcmltYXJ5Q29sb3IiOiIjZjlkMDAwIn0=

{"tenantId":"dc78a062-2895-4db2-b4d5-4690096117b7","title":"Contact-us","alertSuccessMessage":"Mensagem enviada com sucesso!","alertErrorMessage":"Ops. Algo deu errado. Tente novamente em alguns instantes.","documentNumber":"91198118881","name":"John","lastName":"Doe","email":"John.doe@gmail.com","phone":"","celPhone":"+5504881273851","isPrime":false,"isMobile":false,"primaryColor":"#f9d000"}


## Automated Tests
To run the automated tests that simulate asynchronous contact submissions with random data, follow the instructions below:

### Verify Active Containers:
- List the running Docker containers to confirm that the backend is active:
    ```sh
    docker ps
    ```

### Access the Backend Container:
- Connect to the backend container:
    ```sh
    docker exec -it crm-mail-backend-1 /bin/bash
    ```

### Run the Tests:
- Navigate to the tests folder and execute the automated test script:
    ```sh
    cd tests/
    python tests.py
    ```

### About the Tests
- This test generates 25 asynchronous contact requests with random data for the three tenants configured in the system.
- It includes the sending of attachments, which may increase the total execution time.
- Note: The execution time may vary due to the processing of attachments and the creation of multiple simultaneous requests.