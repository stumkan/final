
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .models import Ticket, Region, FaultType, Site, User, TicketStatus, Comment

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

import json
from datetime import datetime

from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required



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
            ticket.status = get_object_or_404(TicketStatus, id=data.get('status', ticket.status.id))
            ticket.assigned_to = get_object_or_404(User, id=data.get('assigned_to', ticket.assigned_to.id)) if data.get('assigned_to') else None
            ticket.fault_type = get_object_or_404(FaultType, id=data.get('fault_type', ticket.fault_type.id)) if data.get('fault_type') else None
            ticket.region = get_object_or_404(Region, id=data.get('region', ticket.region.id)) if data.get('region') else None
            ticket.site_A = get_object_or_404(Site, id=data.get('site_A', ticket.site_A.id)) if data.get('site_A') else None
            ticket.site_B = get_object_or_404(Site, id=data.get('site_B', ticket.site_B.id)) if data.get('site_B') else None

            # Save the updated ticket
            ticket.save()

            return JsonResponse({'message': 'Ticket updated successfully'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)


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
