# Django
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseBadRequest, Http404
from django.template import RequestContext

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Django REST Framework
from rest_framework import viewsets, mixins

# Scripts
# from scripts.steam import gamespulling, steamidpulling
# from scripts.github import *
# from scripts.tumblr import TumblrOauthClient
# from scripts.twilioapi import *
# from scripts.instagram import *
# from scripts.scraper import steamDiscounts
# from scripts.quandl import *
# from scripts.twitter import TwitterOauthClient
# from scripts.nytimes import *
# from scripts.meetup import *
# from scripts.linkedin import LinkedinOauthClient
# from scripts.yelp import requestData
# from scripts.facebook import *
# from scripts.googlePlus import *
# from scripts.dropbox import *
# from scripts.foursquare import *

# Python
import os
import oauth2 as oauth
import simplejson as json
import requests
from datetime import timedelta
from calendar import monthrange
import time
import hashlib
import random

# Models
from windopen.models import *
from windopen.serializers import SnippetSerializer
from windopen.forms import UserForm, NewDeviceForm, DeviceForm
from windopen_starter.log import logger_windopen as log
from rpyc_server import MTU_SERVER


# profile_track = None
# getTumblr = TumblrOauthClient(settings.TUMBLR_CONSUMER_KEY, settings.TUMBLR_CONSUMER_SECRET)
# getInstagram = InstagramOauthClient(settings.INSTAGRAM_CLIENT_ID, settings.INSTAGRAM_CLIENT_SECRET)
# getTwitter = TwitterOauthClient(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET, settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
# getGithub = GithubOauthClient('2a11ce63ea7952d21f02', '7e20f82a34698fb33fc837186e96b12aaca2618d')
# getLinkedIn = LinkedinOauthClient(settings.LINKEDIN_CLIENT_ID, settings.LINKEDIN_CLIENT_SECRET)
# getFacebook = FacebookOauthClient(settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_SECRET)
# getGoogle = GooglePlus(settings.GOOGLE_PLUS_APP_ID, settings.GOOGLE_PLUS_APP_SECRET)
# getDropbox = DropboxOauthClient(settings.DROPBOX_APP_ID, settings.DROPBOX_APP_SECRET)
# getFoursquare = FoursquareOauthClient(settings.FOURSQUARE_APP_ID, settings.FOURSQUARE_APP_SECRET)

def index(request):
    print "index: " + str(request.user)

#     if not request.user.is_active:
#         if request.GET.items():
#             if profile_track == 'github':
#                 code = request.GET['code']
#                 getGithub.get_access_token(code)
#                 getGithub.getUserInfo()
#                 print getGithub.access_token
#                 try:
#                     user = User.objects.get(username = getGithub.username + '_github')
#                 except User.DoesNotExist:
#                     username = getGithub.username + '_github'
#                     new_user = User.objects.create_user(username, username+'@madewithgithub.com', 'password')
#                     new_user.save()
#                     try:
#                         profile = GithubProfile.objects.get(user = new_user.id)
#                         profile.access_token = getGithub.access_token
#                     except GithubProfile.DoesNotExist:
#                         profile = GithubProfile(user=new_user, access_token=getGithub.access_token, scopes=getGithub.scopes ,github_user=getGithub.username)
#                     profile.save()
#                 user = authenticate(username=getGithub.username+'_github', password='password')
#                 login(request, user)
#             elif profile_track == 'twitter':
#                 oauth_verifier = request.GET['oauth_verifier']
#                 getTwitter.get_access_token_url(oauth_verifier)
# 
#                 try:
#                     user = User.objects.get(username = getTwitter.username + '_twitter')#(username=getTwitter.username)
#                 except User.DoesNotExist:
#                     username = getTwitter.username + '_twitter'
#                     new_user = User.objects.create_user(username, username+'@madewithtwitter.com', 'password')
#                     new_user.save()
#                     profile = TwitterProfile(user = new_user,oauth_token = getTwitter.oauth_token, oauth_token_secret= getTwitter.oauth_token_secret, twitter_user=getTwitter.username)
#                     profile.save()
#                 user = authenticate(username=getTwitter.username+'_twitter', password='password')
#                 login(request, user)
#             elif profile_track == 'instagram':
#                 code = request.GET['code']
#                 getInstagram.get_access_token(code)
# 
#                 try:
#                     user = User.objects.get(username=getInstagram.user_data['username']+'_instagram')
#                 except User.DoesNotExist:
#                     username = getInstagram.user_data['username']+'_instagram'
#                     new_user = User.objects.create_user(username, username+'@madewithinstagram.com', 'password')
#                     new_user.save()
#                     profile = InstagramProfile(user = new_user, access_token = getInstagram.access_token, instagram_user=getInstagram.user_data['username'])
#                     profile.save()
#                 user = authenticate(username=getInstagram.user_data['username']+'_instagram' , password='password')
#                 login(request, user)
#             elif profile_track == 'linkedin':
#                 code = request.GET['code']
#                 getLinkedIn.get_access_token(code)
#                 getLinkedIn.getUserInfo()
# 
#                 try:
#                     user = User.objects.get(username=getLinkedIn.user_id+'_linkedin')
#                 except User.DoesNotExist:
#                     username = getLinkedIn.user_id+'_linkedin'
#                     new_user = User.objects.create_user(username, username+'@madwithlinkedin.com', 'password')
#                     new_user.save()
#                     try:
#                         profile =LinkedinProfile.objects.get(user = new_user.id)
#                         profile.access_token = LinkedinProfile.access_token
#                     except LinkedinProfile.DoesNotExist:
#                         profile = LinkedinProfile(user=new_user, access_token=getLinkedIn.access_token, linkedin_user=getLinkedIn.user_id)
#                     profile.save()
#                 user = authenticate(username=getLinkedIn.user_id+'_linkedin', password='password')
#                 login(request, user)
# 
#             elif profile_track == 'facebook':
#                 code = request.GET['code']
#                 getFacebook.get_access_token(code)
#                 userInfo = getFacebook.get_user_info()
#                 username = userInfo['first_name'] + userInfo['last_name']
# 
#                 try:
#                     user = User.objects.get(username=username+'_facebook')
#                 except User.DoesNotExist:
#                     new_user = User.objects.create_user(username+'_facebook', username+'@madewithfacbook', 'password')
#                     new_user.save()
# 
#                     try:
#                         profile = FacebookProfile.objects.get(user=new_user.id)
#                         profile.access_token = getFacebook.access_token
#                     except:
#                         profile = FacebookProfile()
#                         profile.user = new_user
#                         profile.fb_user_id = userInfo['id']
#                         profile.profile_url = userInfo['link']
#                         profile.access_token = getFacebook.access_token
#                     profile.save()
#                 user = authenticate(username=username+'_facebook', password='password')
#                 login(request, user)
#             elif profile_track == 'tumblr':
#                 if not getTumblr.is_authorized:
#                     oauth_verifier = request.GET['oauth_verifier']
#                     getTumblr.access_token_url(oauth_verifier)
#                     getTumblr.getUserInfo()
#                     try:
#                         user = User.objects.get(username = getTumblr.username + '_tumblr')
#                     except User.DoesNotExist:
#                         username = getTumblr.username + '_tumblr'
#                         new_user = User.objects.create_user(username, username+'@madewithtumblr.com', 'password')
#                         new_user.save()
#                         try:
#                             profile =TumblrProfile.objects.get(user = new_user.id)
#                             profile.access_token = getTumblr.access_token['oauth_token']
#                             profile.access_token_secret = getTumblr.access_token['oauth_token_secret']
#                         except TumblrProfile.DoesNotExist:
#                             profile = TumblrProfile(user=new_user, access_token=getTumblr.access_token['oauth_token'], access_token_secret= getTumblr.access_token['oauth_token_secret'], tumblr_user=getTumblr.username)
#                         profile.save()
#                 user = authenticate(username=getTumblr.username+'_tumblr', password='password')
#                 login(request, user)
# 
# 
#             elif profile_track == 'google':
#                 code = request.GET['code']
#                 state = request.GET['state']
#                 getGoogle.get_access_token(code, state)
#                 userInfo = getGoogle.get_user_info()
#                 username = userInfo['given_name'] + userInfo['family_name']
# 
#                 try:
#                     user = User.objects.get(username=username+'_google')
#                 except User.DoesNotExist:
#                     new_user = User.objects.create_user(username+'_google', username+'@madewithgoogleplus', 'password')
#                     new_user.save()
# 
#                     try:
#                         profle = GoogleProfile.objects.get(user = new_user.id)
#                         profile.access_token = getGoogle.access_token
#                     except:
#                         profile = GoogleProfile()
#                         profile.user = new_user
#                         profile.google_user_id = userInfo['id']
#                         profile.access_token = getGoogle.access_token
#                         profile.profile_url = userInfo['link']
#                     profile.save()
#                 user = authenticate(username=username+'_google', password='password')
#                 login(request, user)
# 
#             elif profile_track == 'dropbox':
#                 code = request.GET['code']
#                 state = request.GET['state']
#                 getDropbox.get_access_token(code, state)
#                 userInfo = getDropbox.get_user_info()
#                 username = userInfo['name_details']['given_name'] + userInfo['name_details']['surname']
# 
#                 try:
#                     user = User.objects.get(username=username+'_dropbox')
#                 except User.DoesNotExist:
#                     new_user = User.objects.create_user(username+'_dropbox', username+'@madewithdropbox', 'password')
#                     new_user.save()
# 
#                     try:
#                         profile = DropboxProfile.objects.get(user=new_user.id)
#                         profile.access_token = getDropbox.access_token
#                     except:
#                         profile = DropboxProfile()
#                         profile.user = new_user
#                         profile.access_token = getDropbox.access_token
#                         profile.dropbox_user_id = userInfo['uid']
#                     profile.save()
#                 user = authenticate(username=username+'_dropbox', password='password')
#                 login(request, user)
# 
#             elif profile_track == 'foursquare':
#                 code = request.GET['code']
#                 getFoursquare.get_access_token(code)
#                 userInfo = getFoursquare.get_user_info()
#                 username = userInfo['firstName'] + userInfo['lastName']
# 
#                 try:
#                     user = User.objects.get(username=username+'_foursquare')
#                 except User.DoesNotExist:
#                     new_user = User.objects.create_user(username+'_foursquare', username+'@madewithfoursquare', 'password')
#                     new_user.save()
# 
#                     try:
#                         profile = FoursquareProfile.object.get(user=new_user.id)
#                         profile.access_token = getFoursquare.access_token
# 
#                     except:
#                         profile = FoursquareProfile()
#                         profile.user = new_user
#                         profile.foursquare_id = userInfo['id']
#                         profile.access_token = getFoursquare.access_token
#                     profile.save()
# 
#                 user = authenticate(username=username+'_foursquare', password='password')
#                 login(request, user)
# 
# 
# 
# 
# 
#     else:
#         if request.GET.items():
#             user = User.objects.get(username = request.user.username)
#             if profile_track == 'github':
#                 code = request.GET['code']
#                 getGithub.get_access_token(code)
#                 getGithub.getUserInfo()
# 
#                 try:
#                     githubUser = GithubProfile.objects.get(user=user.id)
#                 except GithubProfile.DoesNotExist:
#                     profile = GithubProfile(user=new_user, access_token=getGithub.access_token, scopes=getGithub.scopes ,github_user=getGithub.username)
#                     profile.save()
#             elif profile_track == 'twitter':
#                 oauth_verifier = request.GET['oauth_verifier']
#                 getTwitter.get_access_token_url(oauth_verifier)
# 
#                 try:
#                     twitterUser = TwitterProfile.objects.get(user = user.id)
#                 except TwitterProfile.DoesNotExist:
#                     profile = TwitterProfile(user = user, oauth_token = getTwitter.oauth_token, oauth_token_secret= getTwitter.oauth_token_secret, twitter_user=getTwitter.username)
#                     profile.save()
#             elif profile_track == 'instagram':
#                 code = request.GET['code']
#                 getInstagram.get_access_token(code)
# 
#                 try:
#                     instagramUser = InstagramProfile.objects.get(user= user.id)
#                 except InstagramProfile.DoesNotExist:
#                     profile = InstagramProfile(user = user, access_token = getInstagram.access_token, instagram_user=getInstagram.user_data['username'])
#                     profile.save()
#             elif profile_track == 'linkedin':
#                 code = request.GET['code']
#                 getLinkedIn.get_access_token(code)
#                 getLinkedIn.getUserInfo()
# 
#                 try:
#                     linkedinUser = LinkedinProfile.objects.get(user=user.id)
#                 except LinkedinProfile.DoesNotExist:
#                     profile = LinkedinProfile(user = user, access_token = getLinkedIn.access_token, linkedin_user=getLinkedIn.user_id)
#                     profile.save()
#             elif profile_track == 'tumblr':
#                 if not getTumblr.is_authorized:
#                     oauth_verifier = request.GET['oauth_verifier']
#                     getTumblr.access_token_url(oauth_verifier)
#                     getTumblr.getUserInfo()
# 
#                     try:
#                         tumblrUser = TumblrProfile.objects.get(user=user.id)
#                     except TumblrProfile.DoesNotExist:
#                         profile = TumblrProfile(user=user, access_token=getTumblr.access_token['oauth_token'], access_token_secret= getTumblr.access_token['oauth_token_secret'], tumblr_user=getTumblr.username)
#                         profile.save()


    context = {'hello': 'world'}
    return render(request, 'windopen/index.html', context)

# device = models.ForeignKey(Device, 'uuid')
# user = models.ForeignKey(User)
# status = models.CharField(max_length=128)
# action_start = models.DateTimeField(default=date.today())
# action_end = models.DateTimeField(default=date.today())

@login_required
def actions_details(request, uuid):
    if request.method != 'GET':
        return HttpResponseNotAllowed()
    context = RequestContext(request)
    try:
        actions = Action.objects.filter(device_id = uuid)
    except Exception as err:
        log.warning('No actions on device: %s', err)
        actions = []
    context.update({'actions': actions})
    colors = []
    users = []
    for action in actions:
        if not action.user.username in users:
            r = lambda: random.randint(0,255)
            colors.append({'user': action.user.username, 'color': '#%02X%02X%02X' % (r(),r(),r())})
            users.append(action.user.username)
    log.info('culori: %s', colors)
    context.update({'colors': colors})
    context.update({'device': str(uuid)})
    log.info('____@@@@@@@@@@@@@: %s',context)
    return render_to_response('windopen/actions_details.html', context_instance=context)
        

def open_window_remote(request, code):
    if request.method != 'GET':
        return HttpResponseNotAllowed()
        
    log.info('Command: open remote')
    sep = os.path.sep
    app_path = sep.join(request.path.strip(sep).split(sep)[:2])
    host = request.META.get('HTTP_HOST')
    app_path = host + sep + app_path + sep
    log.info('app_path: %s', app_path)
    open_code = 'http://' + app_path + code + sep
    log.info('open_code_reverse: %s', open_code)
    try:
        d = Device.objects.get(open_code = open_code)
    except Exception as err:
        log.error('Device not found %s', open_code)
    return HttpResponse(open_code)


def close_window_remote(request, code):
    log.info('remote code: %s', code)
    if request.method == 'GET':
        log.info('Command: close remote')
    return HttpResponse()


@login_required
def open_window(request):
    if request.method == 'GET':
        log.info('request: %s',request.GET.get('uuid'))
#         return HttpResponse(json.dumps({'msg':'ok'}))
        try:
            uuid = request.GET.get('uuid', '')
            if not uuid:
                return HttpResponseBadRequest('Empty uuid')
            try:
                d = Device.objects.get(uuid=uuid)
            except Exception as err:
                d = None
            log.info('a luat device: %s', d.__dict__)
            if not d:
                return Http404('Device `{}` not found'.format(uuid))
            if d.status == 'open':
                return HttpResponse(json.dumps({'msg':'Already opened'}))
            else:
                d.status = 'open'
                d.save()
                a = Action(device=d, user=request.user)
                a.status = 'open'
                a.action_start = datetime.now()
                a.action_end = datetime.now()
                a.save()
                MTU_SERVER.service.open_window(uuid)
            log.info('Command: open window %s', uuid)
            log.info('MTU_SERVER: %s', dir(MTU_SERVER))
            log.info('MTU_SERVER: %s', dir(MTU_SERVER.service))
            return HttpResponse(json.dumps({'msg':'ok'}))
        except Exception as err:
            log.error('ERRORRR: %s', err)
            HttpResponse('error')
    return Http404('Use GET for actions')


@login_required
def close_window(request):
    if request.method == 'GET':
        log.info('request: %s',request.GET.get('uuid'))
#         return HttpResponse(json.dumps({'msg':'ok'}))
        try:
            uuid = request.GET.get('uuid', '')
            if not uuid:
                return HttpResponseBadRequest('Empty uuid')
            try:
                d = Device.objects.get(uuid=uuid)
            except Exception as err:
                d = None
            log.info('a luat device: %s', d.__dict__)
            if not d:
                return Http404('Device `{}` not found'.format(uuid))
            if d.status == 'close':
                return HttpResponse(json.dumps({'msg':'Already closed'}))
            else:
                d.status = 'close'
                d.save()
                a = Action(device=d, user=request.user)
                a.status = 'close'
                a.action_start = datetime.now()
                a.action_end = datetime.now()
                a.save()
                MTU_SERVER.service.close_window(uuid)
            log.info('Command: close window %s', uuid)
            log.info('MTU_SERVER: %s', MTU_SERVER)
            return HttpResponse(json.dumps({'msg':'ok'}))
        except Exception as err:
            log.error('ERRORRR: %s', err)
            HttpResponse('error')
    return Http404('Use GET for actions')

@login_required
def actions(request):
    if request.method == 'GET':
        log.info('request: %s',request.GET)
        req_params = request.GET
        interval = req_params.get('interval', 'week')
        uuid = req_params.get('uuid')
        if interval == 'week':
            end_day = datetime.now()
            start_day = end_day + timedelta(days= -7)
        elif interval == 'year':
            end_day = datetime.now()
            if monthrange(end_day.year, 2)[1] == 29 and end_day.month > 2:
                start_day = end_day + timedelta(days = -366)
            else:
                start_day = end_day + timedelta(days = -365)    
        elif interval == 'day':
            end_day = datetime.now()
            start_day = end_day + timedelta(days = -1)
        else:
            end_day = datetime.now()
            no_days = monthrange(end_day.year, end_day.month-1)[1]
            start_day = end_day + timedelta(days = no_days*-1)
        actions = Action.objects.filter(action_start__range=[start_day, end_day], device_id = uuid, status__in=['open','close'])
        response = []
        for action in actions:
            point = {'x': action.action_start.strftime('%Y,%m,%d,%H,%M,%S')}
            if action.status == 'open':
                point['y'] = 1
            else:
                point['y'] = 0
            response.append(point)
        log.info('graph info: %s', response)
        return HttpResponse(json.dumps({'actions': response}))
    else:
        return HttpResponseNotAllowed('Use GET for displaying actions')

@login_required
def generate_open_code(request):
    log.info('request path: %s', request.path)
    if request.method == 'GET':
        sep = os.path.sep
        app_path = request.path.strip(sep).split(sep)[0]
        host = request.META.get('HTTP_HOST')
        app_path = host + sep + app_path + sep
        time_salt = time.time()
        uuid = request.GET.get('uuid', '')
        if not uuid:
            return HttpResponse(json.dumps({'open_code': 'invalid device uuid `{}`'.format(uuid)}))
        open_code = hashlib.sha224('{}{}'.format(uuid, time_salt)).hexdigest()
        device = Device.objects.get(uuid = uuid, user=request.user)
        device.open_code = 'http://' + app_path + 'open_remote' + sep + open_code + sep
        device.save()
        return HttpResponse(json.dumps({'open_code': device.open_code}))
    else:
        return HttpResponseNotAllowed('Use GET to generate open code for device')


@login_required
def generate_close_code(request):
    if request.method == 'GET':
        sep = os.path.sep
        app_path = request.path.strip(sep).split(sep)[0]
        host = request.META.get('HTTP_HOST')
        app_path = host + sep + app_path + sep
        time_salt = time.time()
        uuid = request.GET.get('uuid', '')
        if not uuid:
            return HttpResponse(json.dumps({'close_code': 'invalid device uuid `{}`'.format(uuid)}))
        close_code = hashlib.sha224('{}{}'.format(uuid, time_salt)).hexdigest()
        device = Device.objects.get(uuid = uuid, user=request.user)
        device.close_code = 'http://' + app_path + 'close_remote' + sep + close_code + sep
        device.save()
        return HttpResponse(json.dumps({'close_code': device.close_code}))
    else:
        return HttpResponseNotAllowed('Use GET to generate close code for device')


@login_required
def devices(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed('Use GET to display devices')
    
    context = RequestContext(request)
    try:
        devices = Device.objects.filter(user=request.user)
    except Exception as err:
        log.warning('No devices registered for user: %s | %s', request.user, err)
        devices = []
    context.update({'devices': devices})
    return render_to_response('windopen/devices.html', context_instance=context)


@login_required
def new_device(request):
    if request.method == 'POST':
        form = NewDeviceForm(request.POST)
        if not form.is_valid():
            log.error(dir(form.errors))
            log.error(form.errors['new_device'].data)
            return HttpResponse(json.dumps({'status':'error', 'msg': form.errors['new_device'][0] if 'new_device' in form.errors else form.errors}), content_type='application/json')
        else:
            log.info('new_sn: %s', form.cleaned_data)
            new_sn = form.cleaned_data['new_device']
            # check if the device is already registerd
            existing_device = Device.objects.filter(uuid=new_sn)
            if existing_device:
                log.info('Device `%s` is already registered to user `%s`', new_sn, existing_device[0].user.username)
                status = 'error'
                msg = 'Device is already registered'
                return HttpResponse(json.dumps({'status': status, 'msg': msg}), content_type='application/json')
            # check if the device is connected to the rpyc server and if is in the unregistered table
            unreg_device = UnregisteredDevice.objects.filter(uuid=new_sn)
            if unreg_device:
                d = Device(user=request.user, 
                           uuid=new_sn,
                           registered=datetime.now(),
                           last_seen=datetime.now(),
                           active=True)
                d.save()
                unreg_device.delete()
                status = 'success'
                msg = 'Successfully registered new device'
                log.info('Registered new device `%s` to user `%s`', new_sn, request.user)
                for i in range(10):
                    try:
                        a = Action(device=d, user=request.user)
                        if i % 2 == 1:
                            a.status = 'open'
                        else:
                            a.status = 'close'
                        a.action_start = datetime.now()-timedelta(5)
                        a.action_end = datetime.now()-timedelta(5)
                        a.save()
                    except Exception as err:
                        log.error('err create action: %s', err)
                    time.sleep(2)    
        
                log.info('done creating actions')
            else:
                status = 'error'
                msg = 'The device is not connected. Please connect the device and check for the green LED'
                log.warning('Device `%s` is not connected.', new_sn)

            return HttpResponse(json.dumps({'status': status, 'msg': msg}), content_type='application/json')
    else:
        form = NewDeviceForm()
    return render_to_response('windopen/new_device.html', {'form': form}, context_instance=RequestContext(request))

##################
#  API Examples  #
##################

def api_examples(request):
    context = {'title': 'API Examples Page'}
    return render(request, 'windopen/api_examples.html', context)


######################
# Registration Views #
######################

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
            return HttpResponseRedirect('/windopen/login/')
        else:
            print user_form.errors
    else:
        user_form = UserForm()


    return render(request,
            'windopen/register.html',
            {'user_form': user_form, 'registered': registered} )

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/windopen/devices')
            else:
                return HttpResponse("Your Django Windopen account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'windopen/login.html', {})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/windopen/login/')

