import graphene

from openspace_dto.response_dto import ResponseObjects
from openspace_dto.user_dto import UserOutputObject



class OpenSpaceInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    latitude = graphene.Float(required=False)
    longtude = graphene.Float(required=False)
    easting = graphene.Float(required=False)
    northing = graphene.Float(required=False)
    utm_zone = graphene.String(required=False)
    description = graphene.String(required=False)
    area_size = graphene.Float(required=False)
    region = graphene.String(required=False)
    district = graphene.String(required=False)
    ward = graphene.String(required=False)
    street = graphene.String(required=False)
    managed_by = graphene.String(required=False)
    contact_info = graphene.String(required=False)
    is_active = graphene.Boolean(required=False)

class OpenSpaceObject(graphene.ObjectType):
    openspace_id=graphene.String()
    name = graphene.String()
    latitude = graphene.Float()
    longtude = graphene.Float()
    easting = graphene.Float()
    northing = graphene.Float()
    utm_zone = graphene.String()
    description = graphene.String()
    area_size = graphene.Float()
    region = graphene.String()
    district = graphene.String()
    ward = graphene.String()
    street = graphene.String()
    managed_by = graphene.String()
    contact_info = graphene.String()
    is_active = graphene.Boolean()

class ReportInput(graphene.InputObjectType):
    openspace_id=graphene.String(required=True)
    description=graphene.String(required=True)
    category=graphene.String(required=True)
    user_type=graphene.String(required=True)     


class ReportResponseOutput(graphene.ObjectType):
    reference_id=graphene.String()
    message=graphene.String()
    response=graphene.Field(ResponseObjects)
    user=graphene.Field(UserOutputObject)


class ReportVerificationOutput(graphene.ObjectType):
    content_to_verify = graphene.String()
    description = graphene.String()
    category = graphene.String()
    openspace_id = graphene.UUID()
    temporary_id = graphene.UUID()

class ReportActionEnum(graphene.Enum):
    SUBMIT = "submit"
    EDIT = "edit"
    CANCEL = "cancel"

class ReportStatusEnum(graphene.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"

    @property
    def description(self):
        descriptions = {
            "pending": "Report submitted, awaiting review",
            "in_progress": "Report is being worked on",
            "resolved": "Report has been addressed"
        }
        return descriptions[self.value]