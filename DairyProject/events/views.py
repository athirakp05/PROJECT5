from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.shortcuts import get_object_or_404, render, redirect
from events.models import Meeting
from .forms import MeetingForm
from django.contrib import messages
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

def meeting(request):
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting=form.save()
            generate_brochure(request, meeting.meeting_id)
            messages.success(request, 'Meeting details saved successfully!')
            return redirect('admindash')
        else:
            print(form.errors)  # Print form errors for debugging
            messages.error(request, 'There were errors in the form. Please fix them.')
    else:
        form = MeetingForm()

    return render(request, 'admin/meeting.html', {'form': form})

def meetinglist(request):
    meetings = Meeting.objects.all()
    return render(request, 'event/meetinglist.html', {'meetings': meetings})

def generate_brochure(request, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{meeting.title}_brochure.pdf"'
    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(300, 770, f"Meeting Brochure: {meeting.title}")
    p.setFont("Helvetica", 12)
    p.drawString(100, 740, f"Date: {meeting.date}")
    p.drawString(100, 720, f"Time: {meeting.time}")
    p.drawString(100, 700, f"Location: {meeting.location}")
    p.drawString(100, 680, f"Description: {meeting.description}")
    p.save()
    return response
