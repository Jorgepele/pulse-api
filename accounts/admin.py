from django.contrib import admin

from .models import Membership, Organization, User


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "is_staff", "is_active")
    search_fields = ("email", "full_name")


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "owner", "created_at")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [MembershipInline]
