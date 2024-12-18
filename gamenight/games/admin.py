from typing import cast

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm
from django.utils.translation import gettext_lazy as _

from gamenight.games.widgets import Base64ImageWidget

from .models import Fixture, Game, User


class FixtureRankInline(admin.TabularInline):
    model = Fixture.users.through


@admin.register(Fixture)
class FixtureAdmin(admin.ModelAdmin):
    inlines = (FixtureRankInline,)
    list_display = ("game", "started", "ended", "applied")
    list_filter = ["game__name", ("ended", admin.EmptyFieldListFilter), "applied", "users"]
    ordering = ("-started",)
    readonly_fields = ("graph",)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    ordering = ("name",)
    list_display = (
        "name",
        "minimum_players",
        "maximum_players",
        "ranked",
        "estimated_duration",
        "decay",
        "randomness",
    )


class UserChangeForm(DjangoUserChangeForm):
    qrcode_img = forms.CharField(widget=Base64ImageWidget, required=False)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["qrcode_img"].initial = cast(User, self.instance).get_qrcode()


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    form = UserChangeForm
    list_display = ("username", "score", "first_name", "last_name", "is_staff")
    fieldsets = (
        (None, {"fields": ("username", "password", "score", "qrcode_img")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
