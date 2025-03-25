import graphene

from openspace_dto.response_dto import ResponseObjects




class UserInputObject(graphene.InputObjectType):
    username=graphene.String(required=True)
    email=graphene.String()
    phone_number=graphene.String()
    password=graphene.String(required=True)
    first_name=graphene.String()
    last_name=graphene.String()

class UserOutputObject(graphene.ObjectType):
    id=graphene.String()
    username=graphene.String()
    phone_number=graphene.String()
    email=graphene.String()
    first_name=graphene.String()
    last_name=graphene.String()
    is_verified=graphene.Boolean()
    is_active=graphene.Boolean()
    is_staff=graphene.Boolean()

class TokenOutputObject(graphene.ObjectType):
    access_token=graphene.String()
    refresh_token=graphene.String()

class UserResponseOutput(graphene.ObjectType):
    user_data=graphene.Field(UserOutputObject)
    response=graphene.Field(ResponseObjects)
    tokens=graphene.Field(TokenOutputObject)
