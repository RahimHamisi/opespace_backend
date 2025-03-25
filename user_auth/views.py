from django.shortcuts import render
import graphene
from django.contrib.auth import authenticate
import graphql_jwt
from graphql_jwt.refresh_token.models import RefreshToken
from user_auth.models import User
from openspace_dto.user_dto import *
from openspace_dto_builder.user_dto_builder import UserBuilder


# Create your views here.
class RegisterUserMutation(graphene.Mutation):
    class Arguments:
        input=UserInputObject(required=True)
    
    output=graphene.Field(UserResponseOutput)

    @classmethod
    def mutate(self,root,info,input):
        errors=[]
        if User.objects.filter(username=input.username).exists():
            errors.append(8)
        if input.email and User.objects.filter(email=input.email):
            errors.append(9)
        if errors:
            response=ResponseObjects.get_response(id=errors[0])
            data=UserResponseOutput(
                user_data=None,
                tokens=None,
                response=response
            )
            return RegisterUserMutation(output=data)
        
        user=User.objects.create(
            username=input.username,
            email=input.email or "",
            phone_number=input.phone_number or "",
            first_name=input.first_name or "",
            last_name=input.last_name or ""
        )
        user.set_password(input.password)
        user.save()
        response=ResponseObjects.get_response(id=5)
        user_data=UserBuilder.get_user_data(id=user.id)
     
        data=UserResponseOutput(
                user_data=user_data,
                response=response,
                tokens=None
            )
        return RegisterUserMutation(output=data)
        
    
    


    
class LoginUserMutation(graphene.Mutation):
    class Arguments:
        input=UserInputObject(required=True)

    identifier=graphene.Field(TokenOutputObject)
    response=graphene.Field(ResponseObjects)

    @classmethod
    def mutate(self,root,info,input):
        user=authenticate(username=input.username,password=input.password)
        if user is None:
            response=ResponseObjects.get_response(id=2)
            user=None
            return LoginUserMutation(response=response) 
        
        access_token=graphql_jwt.shortcuts.get_token(user)
        refresh_token_obj=RefreshToken.objects.create(user=user)
        response=ResponseObjects.get_response(id=1)
        data=TokenOutputObject(
            access_token=access_token,
            refresh_token=str(refresh_token_obj)
        )
        return LoginUserMutation(identifier=data,response=response)







    
    
    
class UserMutation(graphene.ObjectType):
    login_user=LoginUserMutation.Field()
    register_user=RegisterUserMutation.Field()
    refresh_token = graphql_jwt.Refresh.Field()