from datetime import date, datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username

class Profile(models.Model):
    user = models.ForeignKey(User)
    oauth_token = models.CharField(max_length=200)
    oauth_secret = models.CharField(max_length=200)

    def __unicode__(self):
        return unicode(self.user)

class Device(models.Model):
    user = models.ForeignKey(User)
    # uuid of device
    uuid = models.CharField(max_length=128, unique=True)
    open_code = models.CharField(max_length=512)
    close_code = models.CharField(max_length=512)
    registered = models.DateTimeField(default=datetime.now()) 
    last_seen = models.DateTimeField(default=datetime.now())
    active = models.BooleanField(default=None)
    status = models.CharField(max_length=32, default='close')

class Action(models.Model):
    device = models.ForeignKey(Device, 'uuid')
    user = models.ForeignKey(User)
    status = models.CharField(max_length=128)
    action_start = models.DateTimeField(default=datetime.now())
    action_end = models.DateTimeField(default=datetime.now())
    class Meta:
        ordering = ['action_start']

class UnregisteredDevice(models.Model):
    uuid = models.CharField(max_length=32)
    joined = models.DateTimeField(default=date.today())

##################################################

class GithubProfile(models.Model):
    user = models.ForeignKey(User)
    github_user = models.CharField(max_length=200)
    access_token = models.CharField(max_length=200)
    scopes = models.CharField(max_length=200)
 
    def __unicode__(self):
        return unicode(self.user)
 
class TumblrProfile(models.Model):
    user = models.ForeignKey(User)
    tumblr_user = models.CharField(max_length=200)
    access_token = models.CharField(max_length=200)
    access_token_secret = models.CharField(max_length=200)
 
    def __unicode__(self):
        return unicode(self.user)
 
class InstagramProfile(models.Model):
    user = models.ForeignKey(User)
    instagram_user = models.CharField(max_length=200)
    access_token = models.CharField(max_length=200)
 
    def __unicode__(self):
        return unicode(self.user)
 
class TwitterProfile(models.Model):
    user = models.ForeignKey(User)
    twitter_user = models.CharField(max_length=200)
    oauth_token = models.CharField(max_length=200)
    oauth_token_secret = models.CharField(max_length=200)
 
    def __unicode__(self):
        return unicode(self.user)
 
class LinkedinProfile(models.Model):
    user = models.ForeignKey(User)
    linkedin_user = models.CharField(max_length=200)
    access_token = models.CharField(max_length=200)
 
    def __unicode__(self):
        return unicode(self.user)
 
class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
 
    class Meta:
        ordering = ('created',)
 
class MeetupToken(models.Model):
    # user = models.ForeignKey(User)
    access_token = models.CharField(max_length=200)
 
    def __unicode__(self):
        return unicode(self.access_token)
 
class FacebookProfile(models.Model):
    user = models.ForeignKey(User)
    fb_user_id = models.CharField(max_length=100)
    time_created = models.DateTimeField(auto_now_add=True)
    profile_url = models.CharField(max_length=50)
    access_token = models.CharField(max_length=100)
 
class GoogleProfile(models.Model):
    user = models.ForeignKey(User)
    google_user_id = models.CharField(max_length=100)
    time_created = models.DateTimeField(auto_now_add=True)
    access_token = models.CharField(max_length=100)
    profile_url = models.CharField(max_length=100)
 
class DropboxProfile(models.Model):
    user = models.ForeignKey(User)
    dropbox_user_id = models.CharField(max_length=100)
    time_created = models.DateTimeField(auto_now_add=True)
    access_token = models.CharField(max_length=100)
 
 
class FoursquareProfile(models.Model):
    user = models.ForeignKey(User)
    foursquare_id = models.CharField(max_length=100)
    time_created = models.DateTimeField(auto_now_add=True)
    access_token = models.CharField(max_length=100)
