import graphene

from openspace_dto.openspace_dto import OpenSpaceObject
from openspace_dto.response_dto import ResponseObjects
from openspace_dto_builder.openspace_dto_builder import OpenSpaceBuilder



class OpenSpaceQuery(graphene.ObjectType):
    all_openspace=graphene.List(OpenSpaceObject)
    openspace=graphene.Field(OpenSpaceObject,openspace_id=graphene.UUID(required=True))

    def resolve_all_openspace(self,info):
        return OpenSpaceBuilder.get_all_openspace()
    
    def resolve_openspace(self,info,openspace_id):
        if id is not None:
            return  OpenSpaceBuilder.get_openspace_data(openspace_id=openspace_id)
        else:
            response=ResponseObjects.get_response(id=14)
            return response
