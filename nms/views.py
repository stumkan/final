from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .models import Ticket, Region, FaultType, Site, User, TicketStatus

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json
from datetime import datetime


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
