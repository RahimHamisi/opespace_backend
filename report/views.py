from django.shortcuts import render
import graphene
import utm

from openspace_dto.openspace_dto import *
from openspace_dto.response_dto import ResponseObjects
from report.models import OpenSpace

# Create your views here.
class CreateOpenSpace(graphene.Mutation):
    class Arguments:
        input=OpenSpaceInput()
    
    output=graphene.Field(OpenSpaceObject)
    response=graphene.Field(ResponseObjects)

    @classmethod
    def mutate(self,root,info,input):

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
    


class OpenSpaceMutation(graphene.ObjectType):
    create_openspace=CreateOpenSpace.Field()