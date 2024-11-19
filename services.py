from apiclient import discovery

from googleCred import credentials
import constants

def create_service(type) -> any:
    return discovery.build(type, constants.SERVICES[type], credentials=credentials)
