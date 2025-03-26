import graphene

from report.schema import OpenSpaceQuery
from report.views import OpenSpaceMutation
from user_auth.schema import UserQuery
from user_auth.views import UserMutation 



class Query(OpenSpaceQuery,UserQuery,graphene.ObjectType):
    pass




class Mutation(OpenSpaceMutation,UserMutation,graphene.ObjectType):
    pass




schema=graphene.Schema(query=   Query,mutation=Mutation)