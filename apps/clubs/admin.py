from django.contrib import admin

from .models import BmccClubsInfo, Club, Membership


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 0
    raw_id_fields = ("user",)
    readonly_fields = ("joined_at",)


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "active", "club_members")
    list_filter = ("category", "active")
    search_fields = ("name", "email", "advisor_name")
    inlines = [MembershipInline]


@admin.register(BmccClubsInfo)
class BmccClubsInfoAdmin(admin.ModelAdmin):
    list_display = ("__str__", "source_url", "fetched_at", "osa_email")

    def has_add_permission(self, request):
        # Single snapshot row (pk=1) is created by refresh_bmcc_clubs_info; edits are manual overrides.
        return False


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "club", "joined_at")
    list_filter = ("club",)
    search_fields = ("user__username", "user__email", "club__name")
    raw_id_fields = ("user", "club")
    readonly_fields = ("joined_at",)
