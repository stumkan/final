from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

class User(AbstractUser):
    ROLES = (
        ('noc', 'NOC Staff'),
        ('technician', 'Technician'),
        ('manager', 'Manager'),
        ('client', 'Client')
    )
    role = models.CharField(max_length=50, choices=ROLES, default='client')


class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Site(models.Model):
    name = models.CharField(max_length=100, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='sites')

    def __str__(self):
        return self.name

class FaultType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class TicketStatus(models.Model):
    """
    Represents the status of a ticket.
    Possible values: active, resolved, outstanding.
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    fault_start = models.CharField(max_length=255, null=True, blank=True)
    fault_end = models.CharField(max_length=255, null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    status = models.ForeignKey('TicketStatus', on_delete=models.CASCADE, related_name='tickets', default=1) 
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets', null=True, blank=True)
    fault_type = models.ForeignKey(FaultType, on_delete=models.CASCADE, related_name='tickets', null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='tickets', null=True, blank=True)
    site_A = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='site_A_tickets', null=True, blank=True)
    site_B = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='site_B_tickets', null=True, blank=True)

    def __str__(self):
        if self.site_B and self.site_A != self.site_B:
            return f"{self.fault_type.name} at {self.site_A.name} and {self.site_B.name}, started at {self.fault_start}. Status : {self.status.name}"
        else:
            return f"{self.fault_type.name} at {self.site_A.name}, started at {self.fault_start}. Status : {self.status.name}"

    def serialize(self):
            return {
                "id": self.id,
                "fault_start": self.fault_start,
                "fault_end": self.fault_end,
                "summary": self.summary,
                "status": self.status.name if self.status else None,
                "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "assigned_to": self.assigned_to.username if self.assigned_to else None,
                "fault_type": self.fault_type.name if self.fault_type else None,
                "region": self.region.name if self.region else None,
                "site_A": self.site_A.name if self.site_A else None,
                "site_B": self.site_B.name if self.site_B else None,
            }

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.ticket.title}"


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=100, default="No Title Provided")
    content = models.TextField()  # Store the Markdown content
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note by {self.user.username} on {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    def serialize(self):
            return {
                "id": self.id,
                "title": self.title,
                "content": self.content,

            }