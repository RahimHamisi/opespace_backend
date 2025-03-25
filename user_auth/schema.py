import graphene

from openspace_dto.user_dto import UserOutputObject
from openspace_dto_builder.user_dto_builder import UserBuilder



class UserQuery(graphene.ObjectType):
    all_users=graphene.List(UserOutputObject)
    user=graphene.Field(UserOutputObject,id=graphene.UUID(required=True))



    @staticmethod
    def resolve_all_users(self,info):
        return UserBuilder.get_users()
    
    @staticmethod
    def resolve_user(self,info,id):
        return UserBuilder.get_user_data(id=id)