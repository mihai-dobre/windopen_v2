from django.contrib import admin
from windopen_app.models import UserProfile, Profile, Device, UnregisteredDevice, Action
# Register your models here.
# class TwitterProfileAdmin(admin.ModelAdmin):
# 	list_display = ("user","twitter_user")


admin.site.register(UserProfile)
admin.site.register(Profile)
admin.site.register(Device)
admin.site.register(UnregisteredDevice)
admin.site.register(Action)
# admin.site.register(InstagramProfile)
# admin.site.register(TwitterProfile, TwitterProfileAdmin)
# admin.site.register(GithubProfile)
# admin.site.register(MeetupToken)
# admin.site.register(LinkedinProfile)
# admin.site.register(TumblrProfile)