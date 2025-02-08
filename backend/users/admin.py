from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rest_framework.authtoken.models import TokenProxy

from users.models import Follow

User = get_user_model()


class UserAdmin(admin.ModelAdmin):

    list_display = (
        'username', 'email', 'first_name',
        'last_name', 'followers', 'recipes',
    )
    list_filter = ('username', 'email',)
    search_fields = ('username', 'email', 'first_name', 'last_name')

    @admin.display(description='Количество подписчиков')
    def followers(self, obj):
        return obj.following.count()

    @admin.display(description='Количество рецептов')
    def recipes(self, obj):
        return obj.recipes.count()


class FollowAdmin(admin.ModelAdmin):
    list_display = ("user", "following",)


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.unregister(Group)
admin.site.unregister(TokenProxy)
