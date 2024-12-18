from django.contrib import admin

# Register your models here.
from .models import User, Site, Region, FaultType, Ticket, Comment, TicketStatus


admin.site.register(User)
admin.site.register(Site)
admin.site.register(Region)
admin.site.register(FaultType)
admin.site.register(Ticket)
admin.site.register(Comment)
admin.site.register(TicketStatus)