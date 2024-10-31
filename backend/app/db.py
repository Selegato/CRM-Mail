from datetime import datetime

from app.config import DB_NAME, DB_URI
from app.logger import logger
from pymongo import MongoClient


def connect_to_mongo() -> MongoClient:
    """connect to mongo and return the db"""
    client = MongoClient(DB_URI)
    db = client[DB_NAME]
    return db


def save_contact_database(data: dict) -> str:
    """save contact data to the database and return the contact_id"""
    db = connect_to_mongo()
    contacts = db["contacts"]
    contact_id = contacts.insert_one(data).inserted_id
    return contact_id


def get_data_tenant(tenant_id: str) -> dict:
    """get tenant data from the database"""
    db = connect_to_mongo()
    tenants = db["tenants"]
    tenant = tenants.find_one({"tenant_id": tenant_id})
    return tenant


def set_mail_send(contact_id: str) -> str:
    """set mail_sent_at field to the current datetime"""
    db = connect_to_mongo()
    contacts = db["contacts"]
    result = contacts.update_one(
        {"_id": contact_id},
        {"$set": {"mail_sent_at": datetime.now().isoformat()}},
    )
    return result


# create tenants
tenants = [
    {
        "tenant_id": "4863b71f-f97b-42fb-8a8c-8f94f63452e4",
        "name": "Store Papers",
        "reason": ["Info", "Request", "Complaint"],
        "related_to": [
            "Credit Card",
            "Physical Store",
        ],
        "mail_to_crm": "contact@papers.com",
        "mail_to_credit_card": "credit-card@papers.com",
        "mail_to_complaint": "complaints@papers.com",
    },
    {
        "tenant_id": "869ea6a0-3a27-4632-9e42-2ee431a89565",
        "name": "Donations",
        "reason": ["Info", "Request", "Suggestion", "Complaint"],
        "related_to": [
            "Donations",
            "Visit",
            "Meeting",
        ],
        "mail_to_crm": "contact@donations.ngo.ca",
        "mail_to_complaint": "complaints.donations@donations.ngo.ca",
    },
    {
        "tenant_id": "dc78a062-2895-4db2-b4d5-4690096117b7",
        "name": "SuperStore",
        "reason": ["Info", "Request", "Suggestion", "Compliment", "Complaint"],
        "related_to": [
            "Credit Card",
            "Physical Store",
            "E-commerce",
            "App",
            "Super Pay",
        ],
        "mail_to_crm": "contact@superstore.com.br",
        "mail_to_prime": "contact.prime@superstore.com.br",
        "mail_to_super_pay": "contact.superpay@superstore.com.br",
    },
]


def init_mongo_db():
    # Connect to MongoDB
    client = MongoClient(DB_URI)

    # Create a database
    db = client[DB_NAME]

    # Create a collections
    tenants_collection = db["tenants"]

    # Check if tenants collection is empty
    if tenants_collection.count_documents({}) == 0:
        # Insert data
        tenants_collection.insert_many(tenants)
        logger.warning("Tenants data inserted successfully!")

    else:
        logger.warning("Tenants data already exists!")

    # create index
    tenants_collection.create_index("tenant_id", unique=True)
