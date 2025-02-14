"""Module to assist creating Google services"""

from apiclient import discovery

from src.utils import google_cred

DRIVE_SERVICE = "drive"
DOCS_SERVICE = "docs"
FORMS_SERVICE = "forms"

SERVICES = {
    DRIVE_SERVICE: "v3",
    DOCS_SERVICE: "v1",
    FORMS_SERVICE: "v1",
}


def _create_service(service_type) -> any:
    """Function to create service"""
    return discovery.build(
        service_type,
        SERVICES[service_type],
        credentials=google_cred.credentials,
    )

def create_docs_service():
    """Helper function to create docs service"""
    return _create_service(DOCS_SERVICE)

def create_drive_service():
    """Helper function to create drive service"""
    return _create_service(DRIVE_SERVICE)

def create_forms_service():
    """Helper function to create forms service"""
    return _create_service(FORMS_SERVICE)
