from django.contrib import admin

# Register your models here.
# Define a new User admin
from authentification.models import User, UserStrike, StrikeReason


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(UserStrike)
class Strike(admin.ModelAdmin):
    pass


@admin.register(StrikeReason)
class StrikeReason(admin.ModelAdmin):
    pass
