from django.contrib import admin
from Model.models import User, Campus, Building, Room, Seat, Reservation

# Register your models here.
class SeatAdmin(admin.ModelAdmin):
    list_display = ['seat_id', 'room', 'seat_number', 'can_charge', 'QR_Code']
    list_filter = ['seat_id', 'room', ]
    list_per_page = 20


class SeatInline(admin.TabularInline):
    model = Seat
    fields = ['seat_id', 'seat_number', 'QR_Code', 'can_charge']
    list_per_page = 10
    show_change_link = True
    extra = 0


class RoomInline(admin.TabularInline):
    model = Room
    show_change_link = True
    extra = 0

class BuildingAdmin(admin.ModelAdmin):
    list_display = ['building_id', 'campus', 'building_name']
    inlines = [RoomInline]

admin.site.register(Building, BuildingAdmin)

class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_id', 'building', 'type', 'room_name', 'number_of_seats', 'is_available', 'open_time',
                    'close_time', 'is_allnight', 'have_charge']
    list_filter = ['is_available', 'room_id']
    list_per_page = 20
    inlines = [SeatInline, ]


class BuildingInline(admin.TabularInline):
    model = Building
    show_change_link = True
    extra = 0


class CampusAdmin(admin.ModelAdmin):
    list_display = ['campus_id', 'campus_name']
    inlines = [BuildingInline]

admin.site.register(User)
admin.site.register(Campus, CampusAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Seat, SeatAdmin)
admin.site.register(Reservation)
