import graphene

from openspace_dto.openspace_dto import OpenSpaceObject, OpenSpaceReports, ReportOutput, TrackProgressOutput
from openspace_dto.response_dto import ResponseObjects
from openspace_dto_builder.openspace_dto_builder import OpenSpaceBuilder
from openspace_dto_builder.report_dto_builder import ReportBuilder
from report.models import OpenSpace, Report




class OpenSpaceQuery(graphene.ObjectType):
    all_openspace=graphene.List(OpenSpaceObject)
    openspace_details=graphene.Field(OpenSpaceObject,openspace_id=graphene.UUID(required=True))
    all_reports=graphene.List(ReportOutput)
    progress_track=graphene.Field(TrackProgressOutput,reference_id=graphene.String(required=True))
    openspace_reports=graphene.List(OpenSpaceReports)


    def resolve_all_openspace(self,info):
        return OpenSpaceBuilder.get_all_openspace() #Ready for returning all openspaces registered in this application
    
    def resolve_openspace_details(self,info,openspace_id):
            return  OpenSpaceBuilder.get_openspace_data(openspace_id=openspace_id) #Ready for retrieving openspace details 
    
    def resolve_all_reports(self,info):
        return ReportBuilder.get_all_reports() #Ready for returning all reports with their area focusing e each report
    
        
    def resolve_openspace_reports(self,info):
        return ReportBuilder.get_reports_by_open_space()  #Ready returning a list of reports based in open space
       
        
    def resolve_progress_track(self,info,reference_id):
        try:
            return ReportBuilder.get_to_track_report(reference_id) #Ready for Tracking Progress of reports
        except:
            return ResponseObjects.get_response(id=18)

    

    

