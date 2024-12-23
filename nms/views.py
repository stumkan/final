
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .models import Ticket, Region, FaultType, Site, User, TicketStatus, Comment, Note
from markdown import markdown as md

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

import json
from datetime import datetime

from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from django.db.models import Q


def search_tickets(request):
    query = request.GET.get('q', '').strip()
    tickets = Ticket.objects.all()

    if query.isdigit():  # If the input is numeric, search by fault_ref
        tickets = tickets.filter(id=query)  # Assuming 'id' is used as the fault reference
    else:  # If the input contains text
        tickets = tickets.filter(
            Q(fault_type__name__icontains=query) |  # Searching in fault_type (assuming FaultType has a 'name' field)
            Q(region__name__icontains=query) |  # Searching in region (assuming Region has a 'name' field)
            Q(site_A__name__icontains=query) |  # Searching in site_A (assuming Site has a 'name' field)
            Q(site_B__name__icontains=query) |  # Searching in site_B (assuming Site has a 'name' field)
            Q(assigned_to__username__icontains=query)  # Searching in assigned_to (username of User model)
        )

    return render(request, 'nms/search_results.html', {'tickets': tickets, 'query': query})



@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)

    if request.method == 'POST':
        note.title = request.POST.get('title')
        note.content = request.POST.get('content')
        note.save()
        return redirect('view_note', note_id=note.id)  # Redirect to the view_note page for the edited note

    return render(request, 'nms/edit_note.html', {'note': note})

@login_required
def create_note(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        Note.objects.create(user=request.user, title=title, content=content)
        return redirect('list_notes')  # Redirect to the notes list after saving
    return render(request, 'nms/create_note.html')

def list_notes(request):
    notes = Note.objects.filter(user=request.user).order_by('-created_at')

    # Serialize tickets using the model's serialize method
    serialized_notes = [note.serialize() for note in notes]

    # Return the serialized data as JSON
    return JsonResponse({'notes': serialized_notes})


@login_required
def create_note(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        Note.objects.create(user=request.user, content=content)
        return redirect('notes_list')  # Redirect to the list of notes

    return render(request, 'nms/create_note.html')



# @login_required
# def view_note(request, note_id):
#     note = get_object_or_404(Note, id=note_id, user=request.user)
#     rendered_content = md(note.content, extensions=['markdown.extensions.extra', 'markdown.extensions.nl2br'])

#     return render(request, 'nms/view_note.html', {'note': note, 'content': rendered_content})


def view_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    rendered_content = md(note.content, extensions=['extra', 'codehilite'])  # Render Markdown
    return render(request, 'nms/view_note.html', {'note': note, 'rendered_content': rendered_content})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json

@csrf_exempt
def update_ticket(request, ticket_id):
    if request.method == "POST":
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)

            # Retrieve the ticket to update
            ticket = get_object_or_404(Ticket, id=ticket_id)

            # Update fields with the provided data
            ticket.fault_start = data.get('fault_start', ticket.fault_start)
            ticket.fault_end = data.get('fault_end', ticket.fault_end)
            ticket.summary = data.get('summary', ticket.summary)

            # Handle status
            status_id = data.get('status')
            if status_id:
                ticket.status = get_object_or_404(TicketStatus, id=status_id)

            # Handle assigned_to
            assigned_to_id = data.get('assigned_to')
            ticket.assigned_to = get_object_or_404(User, id=assigned_to_id) if assigned_to_id else None

            # Handle fault_type
            fault_type_id = data.get('fault_type')
            ticket.fault_type = get_object_or_404(FaultType, id=fault_type_id) if fault_type_id else None

            # Handle region
            region_id = data.get('region')
            ticket.region = get_object_or_404(Region, id=region_id) if region_id else None

            # Handle site_A
            site_A_id = data.get('site_A')
            ticket.site_A = get_object_or_404(Site, id=site_A_id) if site_A_id else None

            # Handle site_B
            site_B_id = data.get('site_B')
            ticket.site_B = get_object_or_404(Site, id=site_B_id) if site_B_id else None

            # Save the updated ticket
            ticket.save()

            return JsonResponse({'message': 'Ticket updated successfully'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)

# @csrf_exempt
# def update_ticket(request, ticket_id):
#     if request.method == "POST":
#         try:
#             # Parse JSON data from the request body
#             data = json.loads(request.body)

#             # Retrieve the ticket to update
#             ticket = get_object_or_404(Ticket, id=ticket_id)

#             # print("print ticket")
#             # print(ticket.id)
#             # print(ticket.fault_start)
#             # print(ticket.fault_end)
#             # print(ticket.summary)
#             # print(ticket.status)
#             # print(ticket.assigned_to)
#             # print(ticket.fault_type)
#             # print(ticket.region)
#             # print(ticket.site_A)
#             # print(ticket.site_B)

#             # Update fields with the provided data
#             ticket.fault_start = data.get('fault_start', ticket.fault_start)
#             ticket.fault_end = data.get('fault_end', ticket.fault_end)
#             ticket.summary = data.get('summary', ticket.summary)
#             ticket.status = get_object_or_404(TicketStatus, id=data.get('status', ticket.status.id))
#             ticket.assigned_to = get_object_or_404(User, id=data.get('assigned_to', ticket.assigned_to.id)) if data.get('assigned_to') else None
#             ticket.fault_type = get_object_or_404(FaultType, id=data.get('fault_type', ticket.fault_type.id)) if data.get('fault_type') else None
#             ticket.region = get_object_or_404(Region, id=data.get('region', ticket.region.id)) if data.get('region') else None
#             ticket.site_A = get_object_or_404(Site, id=data.get('site_A', ticket.site_A.id)) if data.get('site_A') else None
#             ticket.site_B = get_object_or_404(Site, id=data.get('site_B', ticket.site_B.id)) if data.get('site_B') else None

#             # Save the updated ticket
#             ticket.save()

#             return JsonResponse({'message': 'Ticket updated successfully'}, status=200)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     return JsonResponse({'error': 'Invalid HTTP method'}, status=405)


@csrf_exempt
def update_tickets(request, ticket_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            ticket = get_object_or_404(Ticket, id=ticket_id)

            ticket.fault_start = data.get('fault_start', ticket.fault_start)
            ticket.fault_end = data.get('fault_end', ticket.fault_end)
            ticket.summary = data.get('summary', ticket.summary)
            ticket.status = get_object_or_404(TicketStatus, id=data.get('status', ticket.status.id))
            ticket.assigned_to = get_object_or_404(User, id=data.get('assigned_to', ticket.assigned_to.id)) if data.get('assigned_to') else None
            ticket.fault_type = get_object_or_404(FaultType, id=data.get('fault_type', ticket.fault_type.id))
            ticket.region = get_object_or_404(Region, id=data.get('region', ticket.region.id))
            ticket.site_A = get_object_or_404(Site, id=data.get('site_A', ticket.site_A.id))
            ticket.site_B = get_object_or_404(Site, id=data.get('site_B', ticket.site_B.id)) if data.get('site_B') else None

            ticket.save()
            messages.success(request, "Ticket updated successfully!")
            return JsonResponse({'message': 'Ticket updated successfully!'}, status=200)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def add_comment(request, ticket_id):
    if request.method == 'POST':
        ticket = get_object_or_404(Ticket, id=ticket_id)
        content = request.POST.get('content')
        Comment.objects.create(ticket=ticket, user=request.user, content=content)
        return HttpResponseRedirect(reverse('view_ticket', args=[ticket_id]))


def view_ticket(request, ticket_id):
    # Fetch the ticket and its comments
    ticket = get_object_or_404(Ticket, id=ticket_id)
    comments = ticket.comments.select_related('user').order_by('-created_date')

    statuses = TicketStatus.objects.all()
    fault_types = FaultType.objects.all()
    regions = Region.objects.all()
    sites = Site.objects.all()
    users = User.objects.all()


    return render(request, 'nms/view_ticket.html', {
        'ticket': ticket,
        'statuses': statuses,
        'fault_types': fault_types,
        'regions': regions,
        'sites': sites,
        'users': users,
        'comments': comments
    })


def get_ticket_detail(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
        return JsonResponse(ticket.serialize())
    except Ticket.DoesNotExist:
        return JsonResponse({"error": "Ticket not found"}, status=404)


@login_required
def load_ticket_box(request, ticket_box):

    # Filter emails returned based on mailbox
    if ticket_box == "open":
        tickets = Ticket.objects.filter(status__name__in=['active', 'outstanding', 'canceled']).order_by('-created_at')

    elif ticket_box == "closed":
        tickets = Ticket.objects.filter(status__name__in=['closed']).order_by('-created_at')

    else:
        return JsonResponse({"error": "Invalid ticketbox."}, status=400)

    # Serialize tickets using the model's serialize method
    serialized_tickets = [ticket.serialize() for ticket in tickets]

    # Return the serialized data as JSON
    return JsonResponse({'tickets': serialized_tickets})


@csrf_exempt 
def create_ticket(request):
    if request.method == 'POST':
        try:
            # Parse JSON payload
            data = json.loads(request.body)
            user = request.user

            # Fetch related objects
            fault_type = FaultType.objects.get(id=data.get('fault_type')) if data.get('fault_type') else None
            region = Region.objects.get(id=data.get('region')) if data.get('region') else None
            site_A = Site.objects.get(id=data.get('site_A')) if data.get('site_A') else None
            site_B = Site.objects.get(id=data.get('site_B')) if data.get('site_B') else None
            ticket_status = TicketStatus.objects.get(id=data.get('ticket_status')) if data.get('ticket_status') else None

            # Create the Ticket
            ticket = Ticket.objects.create(
                fault_start=data.get('fault_start'),
                fault_end=data.get('fault_end'),
                summary=data.get('summary'),
                status=ticket_status,
                fault_type=fault_type,
                region=region,
                site_A=site_A,
                site_B=site_B,
                assigned_to=user
            )
            return JsonResponse({'message': 'Ticket created successfully!', 'ticket_id': ticket.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


def index(request):

        # Authenticated users view their inbox
    if request.user.is_authenticated:
        regions = Region.objects.all()
        fault_types = FaultType.objects.all()
        sites = Site.objects.all()
        regions = Region.objects.all()
        ticket_status = TicketStatus.objects.all()

        context = {
            "regions": regions,
            "fault_types": fault_types,
            "sites": sites,
            "ticket_status": ticket_status
        }
        return render(request, "nms/index.html", context)

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "nms/index.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            messages.success(request, "You have logged in successfully.")
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Your credentials are incorrect.")
            return render(request, "nms/login.html")
    else:
        return render(request, "nms/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "nms/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            messages.error(request, "Email address already taken.")
            return render(request, "nms/register.html")

        login(request, user)
        messages.success(request, "You have registered in successfully.")
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "nms/register.html")
