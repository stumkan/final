from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from io import BytesIO
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib import messages

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from .models import Ticket, Region, FaultType, Site

from django.views.decorators.csrf import csrf_exempt

from .models import Ticket, FaultType, Region, Site, User
from django.core.exceptions import ObjectDoesNotExist
import json
from django.contrib.auth import get_user_model

def get_sites_by_region(request, region_id):
    sites = Site.objects.filter(region_id=region_id).values('id', 'name')
    return JsonResponse(list(sites), safe=False)

@csrf_exempt
@login_required
def ticketbox(request, ticketbox):

    # Filter emails returned based on mailbox
    if ticketbox == "active":
        tickets = Ticket.objects.filter(resolved=False)

    elif ticketbox == "resolved":
        tickets = Ticket.objects.filter(resolved=True)

    else:
        return JsonResponse({"error": "Invalid ticketbox."}, status=400)

    # Return emails in reverse chronologial order
    tickets = tickets.order_by("-created_at").all()
    return JsonResponse([ticket.serialize() for ticket in tickets], safe=False)



@csrf_exempt
@login_required
def create_ticket(request):
    """Handle ticket creation via POST."""
    if request.method == 'POST':
        User = get_user_model()  # Dynamically get the correct User model
        try:
            data = json.loads(request.body)

            ticket = Ticket.objects.create(
                fault_start=data.get('fault_start'),
                fault_end=data.get('fault_end'),
                summary=data.get('summary'),
                resolved=data.get('resolved', False),
                assigned_to=request.user,
                fault_type=FaultType.objects.get(id=data.get('fault_type')),
                region=Region.objects.get(id=data.get('region')),
                site_A=Site.objects.get(id=data.get('site_A')),
                site_B=Site.objects.get(id=data.get('site_B')),
            )
            ticket.save()
            return JsonResponse({"message": "Ticket created successfully!"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method."}, status=405)


def index(request):

    # Authenticated users view their inbox
    if request.user.is_authenticated:
        regions = Region.objects.all()
        fault_types = FaultType.objects.all()
        sites = Site.objects.all()
        regions = Region.objects.all()

        context = {
            "regions": regions,
            "fault_types": fault_types,
            "sites": sites
        }
        return render(request, "network_management/index.html", context)

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))

@login_required
def get_tickets(request, status):
    if request.method == 'GET':
        tickets = Ticket.objects.filter(status=status)
        return JsonResponse([{
            'id': ticket.id,
            'reference': ticket.reference,
            'title': ticket.title,
            'fault_duration': ticket.fault_duration()
        } for ticket in tickets], safe=False)

@login_required
def view_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'GET':
        return JsonResponse({
            'id': ticket.id,
            'title': ticket.title,
            'reference': ticket.reference,
            'fault_start': ticket.fault_start,
            'fault_end': ticket.fault_end,
            'summary': ticket.summary,
            'archived': ticket.archived
        })
    elif request.method == 'POST':
        # Update ticket details based on the user's role (authorization checks needed)
        pass


@login_required
def generate_pdf(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Create the PDF content
    p.drawString(100, 800, f"Ticket Reference: {ticket.reference}")
    p.drawString(100, 780, f"Title: {ticket.title}")
    p.drawString(100, 760, f"Start: {ticket.fault_start}")
    p.drawString(100, 740, f"End: {ticket.fault_end}")
    p.drawString(100, 720, f"Duration: {ticket.fault_duration()}")
    p.drawString(100, 700, f"Summary: {ticket.summary}")

    p.showPage()
    p.save()
    buffer.seek(0)

    return HttpResponse(buffer, content_type='application/pdf')        

    def login_view(request):
        if request.method == "POST":

            # Attempt to sign user in
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(request, username=email, password=password)

            # Check if authentication successful
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "mail/login.html", {
                    "message": "Invalid email and/or password."
                })
        else:
            return render(request, "network_management/login.html")

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
            return render(request, "network_management/login.html")
    else:
        return render(request, "network_management/login.html")

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
            return render(request, "network_management/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            messages.error(request, "Email address already taken.")
            return render(request, "network_management/register.html")

        login(request, user)
        messages.success(request, "You have registered in successfully.")
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network_management/register.html")
