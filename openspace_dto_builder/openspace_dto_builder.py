import graphene

from openspace_dto.openspace_dto import OpenSpaceObject
from report.models import OpenSpace



class OpenSpaceBuilder:


    @staticmethod
    def get_openspace_data(openspace_id):
        openspace=OpenSpace.objects.get(openspace_id=openspace_id)
        data=OpenSpaceObject(
            id=openspace.id,
            name=openspace.name,
            description=openspace.description,
            area_size=openspace.area_size,
            managed_by=openspace.managed_by,
            is_active=openspace.is_active,
            latitude=openspace.latitude,
            longtude=openspace.longtude,
            easting = openspace.easting,
            northing = openspace.northing,
            utm_zone =openspace.utm_zone,
            region = openspace.region,
            district = openspace.district,
            ward = openspace.ward,
            street = openspace.street,
            contact_info = openspace.contact_info,
        )
        return data
    

    def get_all_openspace():
        all_openspace=[]
        openspaces=OpenSpace.objects.filter(is_active=True)
        for openspace in openspaces:
           data=OpenSpaceObject(
            openspace_id=openspace.openspace_id,
            name=openspace.name,
            description=openspace.description,
            area_size=openspace.area_size,
            managed_by=openspace.managed_by,
            is_active=openspace.is_active,
            latitude=openspace.latitude,
            longtude=openspace.longtude,
            easting = openspace.easting,
            northing = openspace.northing,
            utm_zone =openspace.utm_zone,
            region = openspace.region,
            district = openspace.district,
            ward = openspace.ward,
            street = openspace.street,
            contact_info = openspace.contact_info,
            )
        all_openspace.append(data)
        return all_openspace
           

            

    