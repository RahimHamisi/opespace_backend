import graphene

from user_auth.models import User
from openspace_dto.user_dto import UserOutputObject


class UserBuilder:



    def get_user_data(id):
        if id is not None:
            user=User.objects.get(id=id)

            data=UserOutputObject(
                id=user.id,
                username=user.username,
                phone_number=user.phone_number,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                is_verified=user.is_verified,
                is_active=user.is_active
            )
        return data
    def  get_users():
        users=User.objects.filter(is_active=True)
        all_users=[]
        for user in users:
           user_data=UserOutputObject(
              id=user.id,
              username=user.username,
              email=user.email,
              first_name=user.first_name,
              last_name=user.last_name,
              is_active=user.is_active,
              is_staff=user.is_staff,
              is_verified=user.is_verified

           )
           all_users.append(user_data)
        return all_users
           