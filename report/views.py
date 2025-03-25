from django.shortcuts import render
import graphene
import utm

from openspace_dto.openspace_dto import *
from openspace_dto.response_dto import ResponseObjects
from report.models import OpenSpace



def validate_open_space(self,input=OpenSpaceInput()):
    if input.latitude is not None and input.longitude is not None:
        if OpenSpace.objects.filter(latitude=input.latitude, longtude=input.longtude, name=input.name).exists():
            raise Exception(f"OpenSpace with name '{input.name}' and coordinates ({input.latitude}, {input.longitude}) already exists.")

    elif input.easting is not None and input.northing is not None:
        if OpenSpace.objects.filter(easting=input.easting, northing=input.northing, name=input.name).exists():
            raise Exception(f"OpenSpace with name '{input.name}' and coordinates (Easting: {input.easting}, Northing: {input.northing}) already exists.")
    return True

# Create your views here.
class CreateOpenSpace(graphene.Mutation):
    class Arguments:
        input=OpenSpaceInput()
    
    output=graphene.Field(OpenSpaceObject)
    response=graphene.Field(ResponseObjects)

    @classmethod
    def mutate(self,root,info,input):
        validate_open_space(input.name,input.latitude,input.longtude,input.easting,input.northing)

        if input.latitude is not None and input.longitude is not None:
            easting, northing, zone_number, zone_letter = utm.from_latlon(input.latitude,input.longitude)
            utm_zone = f"WGS 84 UTM {zone_number} {zone_letter}"
        elif input.easting is not None and input.orthing is not None:
            latitude, longitude = utm.to_latlon(input.easting,input.northing, utm_zone.split()[2], utm_zone.split()[3])

        open_space=OpenSpace(
             name=input.name,
            latitude=input.latitude,
            longtude=input.longtude,
            easting=input.easting,
            northing=input.northing,
            utm_zone=input.utm_zone,
            description=input.description,
            area_size=input.area_size,
            region=input.region,
            district=input.district,
            ward=input.ward,
            street=input.street,
            managed_by=input.managed_by,
            contact_info=input.contact_info,
        )
        open_space.save()
        response=ResponseObjects.get_response(id=11)
        return CreateOpenSpace(output=open_space,response=response)
    
class UpdateOpenSpace(graphene.Mutation):
    class Arguments:
        id=graphene.String(required=True)
        input=OpenSpaceInput()


    output=graphene.Field(OpenSpaceObject)
    response=graphene.Field(ResponseObjects)
    @classmethod
    def mutate(self, info, id, input):
        try:
            open_space = OpenSpace.objects.get(id=id)
            for key, value in input.items():  
                if value is not None:  
                    setattr(open_space, key, value) 
            open_space.save()
            response=ResponseObjects.get_response(id=12)
            return UpdateOpenSpace(output=open_space)
        
        except OpenSpace.DoesNotExist:
            response=ResponseObjects.get_response(id=14)
            return UpdateOpenSpace(response=response)
        
class DeleteOpenSpace(graphene.Mutation):
    class Arguments:
        id=graphene.String(required=True)

    response=graphene.Field(ResponseObjects)

    @classmethod
    def mutate(self,root,info,id):
        try:
            open_space=OpenSpace.objects.get(id=id)
            open_space.is_active=False
            open_space.save()
            response=ResponseObjects.get_response(id=13)
            return DeleteOpenSpace(response=response)
        except:
            response-ResponseObjects.get_response(id=14)
            return DeleteOpenSpace(response=response)

class OpenSpaceMutation(graphene.ObjectType):
    create_openspace=CreateOpenSpace.Field()
    update_openspace=UpdateOpenSpace.Field()
    delete_openspace=DeleteOpenSpace.Field()