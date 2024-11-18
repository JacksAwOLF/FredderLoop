from apiclient import discovery

from googleCred import credentials
import constants

def create_service(type) -> any:
    return discovery.build(type, constants.SERVICES[type], credentials=credentials)

class Service:
    def __init__(self, type: str):
        self.type = type
        self.service = None

    def _initialize(self):
        print(f"creating service: {self.type}@{constants.SERVICES[self.type]}")
        self.service = discovery.build(self.type, constants.SERVICES[self.type], credentials=credentials)
        
    def get_service(self):
        if not self.service:
            self._initialize()
        return self.service

    def __str__(self):
        return f"type: {self.type}, version: {constants.SERVICES[self.type]}, service: {self.service}"

    def __del__(self):
        print(f"closing service: {self.type}@{constants.SERVICES[self.type]}")
        try:
            self.service.close()
        except:
            pass  # do nothing


# class Services:
#     def __init__(self):
#         self.services = {}

#     def create_service(self, type: str):
#         if type not in constants.SERVICES.keys():
#             raise TypeError(
#                 f"service type unknown: {type}\n    valid types: {constants.SERVICES.keys()}"
#             )

#         if type in self.services.keys():
#             print(f"type {type} already defined, recreating...")
#             del self.services[type]

#         self.services[type] = Service(type)
#         return self # for factory like behavior

#     def get_service(self, type: str):
#         if type not in self.services.keys():
#             raise TypeError(f"type not found, current services: {self.services.keys()}")
#         return self.services[type].get_service()

#     def get_services(self, types: list) -> list:
#         services = []
#         for type in types:
#             services.append(self.get_service(type))
#         return services

#     def __del__(self):
#         for svc in self.services.values():
#             del svc
