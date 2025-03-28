from collections import defaultdict
import graphene
from openspace_dto.openspace_dto import OpenSpaceReports, ReportOutput, TrackProgressOutput
from openspace_dto.response_dto import ResponseObjects
from report.models import Report




class ReportBuilder:


    def get_to_track_report(reference_id):
            report=Report.objects.get(reference_id=reference_id)
            print(report)
            report_data=TrackProgressOutput(
                report_id = str(report.report_id),
                reference_id = report.reference_id,
                open_space = report.open_space,
                description = report.description,
                category = report.category,
                date_reported = report.date_reported,
                status =report.status,
                assigned_to = report.assigned_to,
                resolution_date =report.resolution_date,
                is_active = report.is_active
            )
            return report_data


    def get_reports_by_open_space():
        reports=Report.objects.filter(open_space__is_active=True).order_by('-date_reported')
        grouped_reports=defaultdict(list) #use default dict from collections module to group items dynamically 
        for report in reports:
            report_data=ReportOutput(
                report_id = str(report.report_id),
                reference_id = report.reference_id,
                open_space = report.open_space,
                user = report.user,
                description = report.description,
                category = report.category,
                date_reported = report.date_reported,
                status =report.status,
                assigned_to = report.assigned_to,
                resolution_date =report.resolution_date,
                is_active = report.is_active
            )
            grouped_reports[report.open_space].append(report_data)
            


        all_reports_for_openspace=[
            OpenSpaceReports(open_space=open_space,reports=reports_list)
            for open_space,reports_list in grouped_reports.items()
        ]
        return all_reports_for_openspace
  

    def get_all_reports():
        all_report=[]
        reports=Report.objects.filter(is_active=True)
        for report in reports:
            report_data=ReportOutput(
                report_id = report.report_id,
                reference_id = report.reference_id,
                open_space = report.open_space,
                user = report.user,
                description = report.description,
                category = report.category,
                date_reported = report.date_reported,
                status =report.status,
                assigned_to = report.assigned_to,
                resolution_date =report.resolution_date,
                is_active = report.is_active
            )
            all_report.append(report_data)
        return all_report
             
        
