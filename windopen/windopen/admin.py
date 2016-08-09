from django.contrib import admin
from windopen.models import UserProfile, Profile

# Register your models here.
# class TwitterProfileAdmin(admin.ModelAdmin):
# 	list_display = ('user','twitter_user')

admin.site.register(UserProfile)
admin.site.register(Profile)
# admin.site.register(InstagramProfile)
# admin.site.register(TwitterProfile, TwitterProfileAdmin)
# admin.site.register(GithubProfile)
# admin.site.register(MeetupToken)
# admin.site.register(LinkedinProfile)
# admin.site.register(TumblrProfile)
