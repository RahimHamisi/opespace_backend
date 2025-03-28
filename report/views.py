import uuid
from django.shortcuts import render
import graphene
import utm

from openspace_dto.openspace_dto import *
from openspace_dto.response_dto import ResponseObjects
from report.models import OpenSpace, Report



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
        openspace_id=graphene.String(required=True)
        input=OpenSpaceInput()


    output=graphene.Field(OpenSpaceObject)
    response=graphene.Field(ResponseObjects)
    @classmethod
    def mutate(cls,root, info, openspace_id, input):
        try:
            open_space = OpenSpace.objects.get(openspace_id=openspace_id)
            for key, value in vars(input).items():  
                if value is not None:  
                    setattr(open_space, key, value) 
            open_space.save()
            response=ResponseObjects.get_response(id=12)
            return UpdateOpenSpace(output=open_space,response=response)
        
        except OpenSpace.DoesNotExist:
            response=ResponseObjects.get_response(id=14)
            return UpdateOpenSpace(response=response)
        
class DeleteOpenSpace(graphene.Mutation):
    class Arguments:
        openspace_id=graphene.String(required=True)

    response=graphene.Field(ResponseObjects)

    @classmethod
    def mutate(self,root,info,openspace_id):
        try:
            open_space=OpenSpace.objects.get(openspace_id=openspace_id)
            open_space.is_active=False
            open_space.save()
            response=ResponseObjects.get_response(id=13)
            return DeleteOpenSpace(response=response)
        except:
            response-ResponseObjects.get_response(id=14)
            return DeleteOpenSpace(response=response)
        
class CreateReport(graphene.Mutation):
    class Arguments:
        input=ReportInput(required=True)
        action = ReportActionEnum(default_value="submit")
        temporary_id = graphene.UUID()  

    output=graphene.Field(ReportResponseOutput)
    verification = graphene.Field(ReportVerificationOutput)

    @classmethod
    def mutate(cls,root,info,input,action, temporary_id=None):
        try:
            open_space=OpenSpace.objects.get(openspace_id=input.openspace_id)
            user=info.context.user
            if input.user_type == 'registered':
                if user.is_authenticated:
                    user_output = UserOutputObject(
                        id=str(user.id),
                        username=user.username,
                        phone_number=user.phone_number,
                        email=user.email,
                        first_name=user.first_name,
                        last_name=user.last_name,
                        is_verified=user.is_verified,
                        is_active=user.is_active,
                        is_staff=user.is_staff,
                        user_type=input.user_type
                    )
                else:
                    response=ResponseObjects.get_response(id=17)
                    output=ReportResponseOutput(
                        response=response,
                        message=None,
                        user=None,
                        reference_id=None
                    )
                  
                    return CreateReport(output=output)
                
            elif input.user_type =="anonymous":
                user_output = UserOutputObject(
                        id=user.id,
                        username=None,
                        phone_number=None,
                        email=None,
                        first_name=None,
                        last_name=None,
                        is_verified=None,
                        is_active=None,
                        is_staff=None,
                        user_type=input.user_type
                )
            else:
                response=ResponseObjects.get_response(id=16)
                output=ReportResponseOutput(
                    response=response,
                    message=None,
                    reference_id=None,
                    user=None

                )
                return CreateReport(output=output)
            
            if action == "submit" and not temporary_id:  
                temp_id = uuid.uuid4()
                return CreateReport(
                    verification=ReportVerificationOutput(
                        content_to_verify=f"Category: {input.category}, Description: {input.description}",
                        description=input.description,
                        category=input.category,
                        openspace_id=input.openspace_id,
                        temporary_id=temp_id
                    )
                )
            elif action == "submit" and temporary_id:
                report=Report.objects.create(
                    open_space=open_space,
                    category=input.category,
                    description=input.description,
                    user=user if input.user_type == 'registered' else None
                )
                report.save() 
                message=f"Thanks for submitting your report,use your report id:{report.reference_id} to Track the progress"
                response=ResponseObjects.get_response(id=15)
                output=ReportResponseOutput(
                    response=response,
                    message=message,
                    reference_id=report.reference_id,
                    user=user_output
                )
                return CreateReport(output=output)
            
            elif action == "edit" and temporary_id:  
                return CreateReport(
                    verification=ReportVerificationOutput(
                        content_to_verify=f"Category: {input.category}, Description: {input.description}",
                        description=input.description,
                        category=input.category,
                        openspace_id=input.openspace_id,
                        temporary_id=temporary_id
                    )
                )
            elif action == "cancel" and temporary_id: 
                response = ResponseObjects.get_response(id=20) 
                output = ReportResponseOutput(
                    response=response,
                    message=None,
                    reference_id=None,
                    user=None
                )
                return CreateReport(output=output)

            else:
                return None
            
        except OpenSpace.DoesNotExist:
            raise Exception("Error: Open space not found.")
        except Exception as e:
            raise Exception(f"Failed to submit report: {str(e)}")
class UpdateReport(graphene.Mutation):
    class Arguments:
        input=input=ReportInput(required=True)
        id=graphene.UUID(required=True)

    output=graphene.Field(ReportResponseOutput)

    @classmethod
    def mutate(self,input,id):
        pass
            

class OpenSpaceMutation(graphene.ObjectType):
    create_openspace=CreateOpenSpace.Field()
    update_openspace=UpdateOpenSpace.Field()
    delete_openspace=DeleteOpenSpace.Field()
    create_report=CreateReport.Field()
    update_report=UpdateReport.Field()