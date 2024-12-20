from django.http import FileResponse
import os

from .studio import generate_fault_report


def download_report(request):
    
    # file_path = "static/reports/fault_report.pdf"
    file_path = "fault_report.pdf"
    fault_ref = "45636"
    fault_start = "2024-12-10 14:00"
    fault_end = "2024-12-10 17:00"
    fault_duration = "3 hours, 0 minutes"
    events = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit."
    conclusion = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit."


    generate_fault_report(file_path, fault_ref, fault_start, fault_end, fault_duration, events, conclusion)
    return FileResponse(open(file_path, "rb"), content_type='application/pdf')

