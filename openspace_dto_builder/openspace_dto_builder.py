import graphene

from openspace_dto.openspace_dto import OpenSpaceObject
from report.models import OpenSpace



class OPenSpaceBuilder:


    @staticmethod
    def get_openspace_data(self,id):
        openspace=OpenSpace.objects.get(id=id)
        data=OpenSpaceObject(
            name=openspace.name,
            description=openspace.description,
            area_size=openspace.area_size,
            managed_by=openspace.managed_by,
            is_active=openspace.is_active,
            latitude=openspace.latitude,
            longtude=openspace.longitude,
            easting = openspace.easting,
            northing = openspace.northing,
            utm_zone =openspace.utm_zone,
            area_size = openspace.area_size,
            region = openspace.region,
            district = openspace.district,
            ward = openspace.ward,
            street = openspace.street,
            managed_by = openspace.managed_by,
            contact_info = openspace.contact_info,
            is_active = openspace.is_active
        )
        return data
    