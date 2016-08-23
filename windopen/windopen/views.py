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
from scripts.steam import gamespulling, steamidpulling
from scripts.github import *
from scripts.tumblr import TumblrOauthClient
from scripts.twilioapi import *
from scripts.instagram import *
from scripts.scraper import steamDiscounts
from scripts.quandl import *
from scripts.twitter import TwitterOauthClient
from scripts.nytimes import *
from scripts.meetup import *
from scripts.linkedin import LinkedinOauthClient
from scripts.yelp import requestData
from scripts.facebook import *
from scripts.googlePlus import *
from scripts.dropbox import *
from scripts.foursquare import *

# Python
import os
import oauth2 as oauth
import simplejson as json
import requests
from datetime import timedelta
from calendar import monthrange
import time
import hashlib

# Models
from windopen.models import *
from windopen.serializers import SnippetSerializer
from windopen.forms import UserForm, NewDeviceForm, DeviceForm
from windopen_starter.log import logger_windopen as log
from rpyc_server import MTU_SERVER


profile_track = None
getTumblr = TumblrOauthClient(settings.TUMBLR_CONSUMER_KEY, settings.TUMBLR_CONSUMER_SECRET)
getInstagram = InstagramOauthClient(settings.INSTAGRAM_CLIENT_ID, settings.INSTAGRAM_CLIENT_SECRET)
getTwitter = TwitterOauthClient(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET, settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
getGithub = GithubOauthClient('2a11ce63ea7952d21f02', '7e20f82a34698fb33fc837186e96b12aaca2618d')
getLinkedIn = LinkedinOauthClient(settings.LINKEDIN_CLIENT_ID, settings.LINKEDIN_CLIENT_SECRET)
getFacebook = FacebookOauthClient(settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_SECRET)
getGoogle = GooglePlus(settings.GOOGLE_PLUS_APP_ID, settings.GOOGLE_PLUS_APP_SECRET)
getDropbox = DropboxOauthClient(settings.DROPBOX_APP_ID, settings.DROPBOX_APP_SECRET)
getFoursquare = FoursquareOauthClient(settings.FOURSQUARE_APP_ID, settings.FOURSQUARE_APP_SECRET)

def index(request):
    print "index: " + str(request.user)

    if not request.user.is_active:
        if request.GET.items():
            if profile_track == 'github':
                code = request.GET['code']
                getGithub.get_access_token(code)
                getGithub.getUserInfo()
                print getGithub.access_token
                try:
                    user = User.objects.get(username = getGithub.username + '_github')
                except User.DoesNotExist:
                    username = getGithub.username + '_github'
                    new_user = User.objects.create_user(username, username+'@madewithgithub.com', 'password')
                    new_user.save()
                    try:
                        profile = GithubProfile.objects.get(user = new_user.id)
                        profile.access_token = getGithub.access_token
                    except GithubProfile.DoesNotExist:
                        profile = GithubProfile(user=new_user, access_token=getGithub.access_token, scopes=getGithub.scopes ,github_user=getGithub.username)
                    profile.save()
                user = authenticate(username=getGithub.username+'_github', password='password')
                login(request, user)
            elif profile_track == 'twitter':
                oauth_verifier = request.GET['oauth_verifier']
                getTwitter.get_access_token_url(oauth_verifier)

                try:
                    user = User.objects.get(username = getTwitter.username + '_twitter')#(username=getTwitter.username)
                except User.DoesNotExist:
                    username = getTwitter.username + '_twitter'
                    new_user = User.objects.create_user(username, username+'@madewithtwitter.com', 'password')
                    new_user.save()
                    profile = TwitterProfile(user = new_user,oauth_token = getTwitter.oauth_token, oauth_token_secret= getTwitter.oauth_token_secret, twitter_user=getTwitter.username)
                    profile.save()
                user = authenticate(username=getTwitter.username+'_twitter', password='password')
                login(request, user)
            elif profile_track == 'instagram':
                code = request.GET['code']
                getInstagram.get_access_token(code)

                try:
                    user = User.objects.get(username=getInstagram.user_data['username']+'_instagram')
                except User.DoesNotExist:
                    username = getInstagram.user_data['username']+'_instagram'
                    new_user = User.objects.create_user(username, username+'@madewithinstagram.com', 'password')
                    new_user.save()
                    profile = InstagramProfile(user = new_user, access_token = getInstagram.access_token, instagram_user=getInstagram.user_data['username'])
                    profile.save()
                user = authenticate(username=getInstagram.user_data['username']+'_instagram' , password='password')
                login(request, user)
            elif profile_track == 'linkedin':
                code = request.GET['code']
                getLinkedIn.get_access_token(code)
                getLinkedIn.getUserInfo()

                try:
                    user = User.objects.get(username=getLinkedIn.user_id+'_linkedin')
                except User.DoesNotExist:
                    username = getLinkedIn.user_id+'_linkedin'
                    new_user = User.objects.create_user(username, username+'@madwithlinkedin.com', 'password')
                    new_user.save()
                    try:
                        profile =LinkedinProfile.objects.get(user = new_user.id)
                        profile.access_token = LinkedinProfile.access_token
                    except LinkedinProfile.DoesNotExist:
                        profile = LinkedinProfile(user=new_user, access_token=getLinkedIn.access_token, linkedin_user=getLinkedIn.user_id)
                    profile.save()
                user = authenticate(username=getLinkedIn.user_id+'_linkedin', password='password')
                login(request, user)

            elif profile_track == 'facebook':
                code = request.GET['code']
                getFacebook.get_access_token(code)
                userInfo = getFacebook.get_user_info()
                username = userInfo['first_name'] + userInfo['last_name']

                try:
                    user = User.objects.get(username=username+'_facebook')
                except User.DoesNotExist:
                    new_user = User.objects.create_user(username+'_facebook', username+'@madewithfacbook', 'password')
                    new_user.save()

                    try:
                        profile = FacebookProfile.objects.get(user=new_user.id)
                        profile.access_token = getFacebook.access_token
                    except:
                        profile = FacebookProfile()
                        profile.user = new_user
                        profile.fb_user_id = userInfo['id']
                        profile.profile_url = userInfo['link']
                        profile.access_token = getFacebook.access_token
                    profile.save()
                user = authenticate(username=username+'_facebook', password='password')
                login(request, user)
            elif profile_track == 'tumblr':
                if not getTumblr.is_authorized:
                    oauth_verifier = request.GET['oauth_verifier']
                    getTumblr.access_token_url(oauth_verifier)
                    getTumblr.getUserInfo()
                    try:
                        user = User.objects.get(username = getTumblr.username + '_tumblr')
                    except User.DoesNotExist:
                        username = getTumblr.username + '_tumblr'
                        new_user = User.objects.create_user(username, username+'@madewithtumblr.com', 'password')
                        new_user.save()
                        try:
                            profile =TumblrProfile.objects.get(user = new_user.id)
                            profile.access_token = getTumblr.access_token['oauth_token']
                            profile.access_token_secret = getTumblr.access_token['oauth_token_secret']
                        except TumblrProfile.DoesNotExist:
                            profile = TumblrProfile(user=new_user, access_token=getTumblr.access_token['oauth_token'], access_token_secret= getTumblr.access_token['oauth_token_secret'], tumblr_user=getTumblr.username)
                        profile.save()
                user = authenticate(username=getTumblr.username+'_tumblr', password='password')
                login(request, user)


            elif profile_track == 'google':
                code = request.GET['code']
                state = request.GET['state']
                getGoogle.get_access_token(code, state)
                userInfo = getGoogle.get_user_info()
                username = userInfo['given_name'] + userInfo['family_name']

                try:
                    user = User.objects.get(username=username+'_google')
                except User.DoesNotExist:
                    new_user = User.objects.create_user(username+'_google', username+'@madewithgoogleplus', 'password')
                    new_user.save()

                    try:
                        profle = GoogleProfile.objects.get(user = new_user.id)
                        profile.access_token = getGoogle.access_token
                    except:
                        profile = GoogleProfile()
                        profile.user = new_user
                        profile.google_user_id = userInfo['id']
                        profile.access_token = getGoogle.access_token
                        profile.profile_url = userInfo['link']
                    profile.save()
                user = authenticate(username=username+'_google', password='password')
                login(request, user)

            elif profile_track == 'dropbox':
                code = request.GET['code']
                state = request.GET['state']
                getDropbox.get_access_token(code, state)
                userInfo = getDropbox.get_user_info()
                username = userInfo['name_details']['given_name'] + userInfo['name_details']['surname']

                try:
                    user = User.objects.get(username=username+'_dropbox')
                except User.DoesNotExist:
                    new_user = User.objects.create_user(username+'_dropbox', username+'@madewithdropbox', 'password')
                    new_user.save()

                    try:
                        profile = DropboxProfile.objects.get(user=new_user.id)
                        profile.access_token = getDropbox.access_token
                    except:
                        profile = DropboxProfile()
                        profile.user = new_user
                        profile.access_token = getDropbox.access_token
                        profile.dropbox_user_id = userInfo['uid']
                    profile.save()
                user = authenticate(username=username+'_dropbox', password='password')
                login(request, user)

            elif profile_track == 'foursquare':
                code = request.GET['code']
                getFoursquare.get_access_token(code)
                userInfo = getFoursquare.get_user_info()
                username = userInfo['firstName'] + userInfo['lastName']

                try:
                    user = User.objects.get(username=username+'_foursquare')
                except User.DoesNotExist:
                    new_user = User.objects.create_user(username+'_foursquare', username+'@madewithfoursquare', 'password')
                    new_user.save()

                    try:
                        profile = FoursquareProfile.object.get(user=new_user.id)
                        profile.access_token = getFoursquare.access_token

                    except:
                        profile = FoursquareProfile()
                        profile.user = new_user
                        profile.foursquare_id = userInfo['id']
                        profile.access_token = getFoursquare.access_token
                    profile.save()

                user = authenticate(username=username+'_foursquare', password='password')
                login(request, user)





    else:
        if request.GET.items():
            user = User.objects.get(username = request.user.username)
            if profile_track == 'github':
                code = request.GET['code']
                getGithub.get_access_token(code)
                getGithub.getUserInfo()

                try:
                    githubUser = GithubProfile.objects.get(user=user.id)
                except GithubProfile.DoesNotExist:
                    profile = GithubProfile(user=new_user, access_token=getGithub.access_token, scopes=getGithub.scopes ,github_user=getGithub.username)
                    profile.save()
            elif profile_track == 'twitter':
                oauth_verifier = request.GET['oauth_verifier']
                getTwitter.get_access_token_url(oauth_verifier)

                try:
                    twitterUser = TwitterProfile.objects.get(user = user.id)
                except TwitterProfile.DoesNotExist:
                    profile = TwitterProfile(user = user, oauth_token = getTwitter.oauth_token, oauth_token_secret= getTwitter.oauth_token_secret, twitter_user=getTwitter.username)
                    profile.save()
            elif profile_track == 'instagram':
                code = request.GET['code']
                getInstagram.get_access_token(code)

                try:
                    instagramUser = InstagramProfile.objects.get(user= user.id)
                except InstagramProfile.DoesNotExist:
                    profile = InstagramProfile(user = user, access_token = getInstagram.access_token, instagram_user=getInstagram.user_data['username'])
                    profile.save()
            elif profile_track == 'linkedin':
                code = request.GET['code']
                getLinkedIn.get_access_token(code)
                getLinkedIn.getUserInfo()

                try:
                    linkedinUser = LinkedinProfile.objects.get(user=user.id)
                except LinkedinProfile.DoesNotExist:
                    profile = LinkedinProfile(user = user, access_token = getLinkedIn.access_token, linkedin_user=getLinkedIn.user_id)
                    profile.save()
            elif profile_track == 'tumblr':
                if not getTumblr.is_authorized:
                    oauth_verifier = request.GET['oauth_verifier']
                    getTumblr.access_token_url(oauth_verifier)
                    getTumblr.getUserInfo()

                    try:
                        tumblrUser = TumblrProfile.objects.get(user=user.id)
                    except TumblrProfile.DoesNotExist:
                        profile = TumblrProfile(user=user, access_token=getTumblr.access_token['oauth_token'], access_token_secret= getTumblr.access_token['oauth_token_secret'], tumblr_user=getTumblr.username)
                        profile.save()


    context = {'hello': 'world'}
    return render(request, 'windopen/index.html', context)

# device = models.ForeignKey(Device, 'uuid')
# user = models.ForeignKey(User)
# status = models.CharField(max_length=128)
# action_start = models.DateTimeField(default=date.today())
# action_end = models.DateTimeField(default=date.today())

@login_required
def open_window(request):
    if request.method == 'GET':
        log.info('request: %s',request.GET.get('uuid'))
        try:
            uuid = request.GET.get('uuid', '')
            if not uuid:
                return HttpResponseBadRequest('Empty uuid')
            d = Device.objects.get(uuid=uuid)
            log.info('a luat device: %s', d.__dict__)
            if not d:
                return Http404('Device `{}` not found'.format(uuid))
            if d.status == 'open':
                return HttpResponse(json.dumps({'msg':'Already opened'}))
            log.info('e close %s', MTU_SERVER)
            if MTU_SERVER:
                result = MTU_SERVER.open_window(d.uuid)
                return HttpResponse(json.dumps({'msg':result}))
            else:
                return Http404(json.dumps({'msg':'Communication server down'}))
        except Exception as err:
            log.error('ERRORRR: %s', err)
            HttpResponse('error')
    return Http404('Use GET for displaying actions')


@login_required
def close_window(request):
    pass

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
        device.open_code = 'http://' + app_path + 'open' + sep + open_code
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
        device.close_code = 'http://' + app_path + 'open' + sep + close_code
        device.save()
        return HttpResponse(json.dumps({'close_code': device.close_code}))
    else:
        return HttpResponseNotAllowed('Use GET to generate close code for device')


@login_required
def devices(request):
    if request.method in ['POST', 'PUT']:
#         form = DeviceForm()
#         return render_to_response('windopen/new_device.html', {'form': form}, context_instance=RequestContext(request)
        return HttpResponseNotAllowed('Use GET to display devices')
    else:
        context = RequestContext(request)
#         log.warning('second context: %s',context)
        try:
            devices = Device.objects.filter(user=request.user)
        except Exception as err:
            log.error('err dev: %s', err)
#         log.warning('devices: %s', len(devices))
        context.update({'devices': devices})
#         log.info('### context full: %s', context)
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

#################
#   STEAM API   #
#################

def steam(request):
    key = '231E98D442E52B87110816C3D5114A1D'
    SteamUN = "Marorin"
    steamID = steamidpulling(SteamUN, key)
    game = gamespulling(steamID, key)
    return render(request,'windopen/steam.html', {"game": game })

def steamDiscountedGames(request):
    data = steamDiscounts()
    return JsonResponse({ 'data': data })

#################
#  FACEBOOK API #
#################

def facebook(request):
    '''
    This is an example of getting basic user info and display it
    '''
    userInfo = getFacebook.get_user_info()
    return render(request, 'windopen/facebookAPIExample.html', { 'userInfo' : userInfo})

#################
#  GOOGLE API   #
#################
def googlePlus(request):

    userInfo = getGoogle.get_user_info()
    return render(request, 'windopen/googlePlus.html', {'userInfo' : userInfo})

#################
#  DROPBOX API  #
#################
def dropbox(request):
    userInfo = getDropbox.get_user_info()
    return render(request, 'windopen/dropbox.html', {'userInfo' : userInfo})

def dropboxSearchFile(request):
    if request.method == 'POST':
        SEARCH_FILE_URL = 'https://api.dropbox.com/1/search/auto/'
        requestParams = {'query': request.POST['filename'],
                         'file_limit': '1000',
                         'include_deleted': True,
                         'access_token': getDropbox.access_token}
        response = requests.post(SEARCH_FILE_URL, data=requestParams)

        if response.status_code!=200:
            raise(Exception('Invalid response, response code {c}'.format(c=response.status_code)))

        return render(request, 'windopen/dropboxSearchFile.html', {'data': response.json()})

#######################
#    FOURSQUARE API   #
#######################

def foursquare(request):
    userInfo = getFoursquare.get_user_info()
    return render(request, 'windopen/foursquare.html', {'data' : userInfo})


#################
#    YELP API   #
#################

def yelp(request):
    data = {}
    if request.method == 'POST':
        location = request.POST.get('location')
        data = requestData(location)
    return render(request, 'windopen/yelp.html', { 'data': data })

#################
#   MEETUP API  #
#################

def meetup(request):
    REDIRECT_URI = 'http://127.0.0.1:8000/hackathon/meetupToken'
    AUTHORIZE_URL = 'https://secure.meetup.com/oauth2/authorize?client_id=' + settings.MEETUP_CONSUMER_KEY + '&response_type=code' + '&redirect_uri=' + REDIRECT_URI
    return HttpResponseRedirect(AUTHORIZE_URL)

def meetupToken(request):
    access_token_url = 'https://secure.meetup.com/oauth2/access?'
    REDIRECT_URI = 'http://127.0.0.1:8000/hackathon/meetupToken'
    url = access_token_url + 'client_id=' +  settings.MEETUP_CONSUMER_KEY + '&client_secret=' + settings.MEETUP_CONSUMER_SECRET + '&grant_type=authorization_code' + '&redirect_uri=' + REDIRECT_URI + '&code=' +  request.GET.get('code')

    response = requests.post(url)
    access_token = json.loads(response.content)['access_token']
 
    if not MeetupToken.objects.all().exists():
        meetupToken = MeetupToken(access_token = access_token)
        meetupToken.save()
    else:
        meetupToken = MeetupToken(access_token = access_token)
        MeetupToken.objects.all()[0] = meetupToken
    return HttpResponseRedirect('http://127.0.0.1:8000/windopen/meetupUser/')

def meetupUser(request):
    if not MeetupToken.objects.all().exists():
        return HttpResponseRedirect('http://127.0.0.1:8000/windopen/meetup')
    access_token = MeetupToken.objects.all()[0]
    meetupData = {}
    userData = retrieveUserData('https://api.meetup.com/2/member/self/?access_token=' + str(access_token))
    meetupData['userData'] = userData
    return render(request, 'windopen/meetup.html', { 'data': meetupData })

#################
#   QUANDL API  #
#################

def quandlDowJones(request):
    '''Returns JSON response about the latest dowjones index.'''
    dowjonesdata = fetchData(settings.QUANDLAPIKEY, 'https://www.quandl.com/api/v1/datasets/BCB/UDJIAD1.json?')
    print dowjonesdata
    return JsonResponse({'data': dowjonesdata})

def quandlSnp500(request):
    '''Returns JSON response about the latest SNP 500 index.'''
    snpdata = fetchData(settings.QUANDLAPIKEY, 'https://www.quandl.com/api/v1/datasets/YAHOO/INDEX_GSPC.json?')
    return JsonResponse({'data': snpdata})

def quandlNasdaq(request):
    '''Returns JSON response about the latest nasdaq index.'''
    nasdaqdata = fetchData(settings.QUANDLAPIKEY, 'https://www.quandl.com/api/v1/datasets/NASDAQOMX/COMP.json?')
    return JsonResponse({'data': nasdaqdata})

def quandlapple(request):
    '''Returns JSON response about the latest apple stock.'''
    appledata = fetchstockData(settings.QUANDLAPIKEY, 'https://www.quandl.com/api/v1/datasets/GOOG/NASDAQ_AAPL.json')
    return JsonResponse({'data': appledata})

def quandlNasdaqdiff(request):
    '''Returns JSON response about the latest nasdaq index.'''
    nasdaqdata = rdiffData(settings.QUANDLAPIKEY, 'https://www.quandl.com/api/v1/datasets/NASDAQOMX/COMP.json?')
    return JsonResponse({'data': nasdaqdata})

def quandlSnp500diff(request):
    '''Returns JSON response about the latest SNP 500 index.'''
    snpdata = rdiffData(settings.QUANDLAPIKEY, 'https://www.quandl.com/api/v1/datasets/YAHOO/INDEX_GSPC.json?')
    return JsonResponse({'data': snpdata})

def quandlDowJonesdiff(request):
    '''Returns JSON response about the latest dowjones index.'''
    dowjonesdata = rdiffData(settings.QUANDLAPIKEY, 'https://www.quandl.com/api/v1/datasets/BCB/UDJIAD1.json?')
    return JsonResponse({'data': dowjonesdata})

def quandlapplediff(request):
    '''Returns JSON response about the latest apple stock.'''
    appledata = rdiffData(settings.QUANDLAPIKEY, 'https://www.quandl.com/api/v1/datasets/GOOG/NASDAQ_AAPL.json')
    return JsonResponse({'data': appledata})

def quandlstocks(request):
    everyData = {}
    dowjonesdata = fetchData(settings.QUANDLAPIKEY, 'https://www.quandl.com/api/v1/datasets/BCB/UDJIAD1.json?')
    everyData['dow'] = dowjonesdata
    everyData['dowdiff'] = rdiffData(settings.QUANDLAPIKEY, 'https://www.quandl.com/api/v1/datasets/BCB/UDJIAD1.json?')
    snpdata = fetchData(settings.QUANDLAPIKEY, 'https://www.quandl.com/api/v1/datasets/YAHOO/INDEX_GSPC.json?')
    everyData['snp'] = snpdata
    everyData['snpdiff'] = rdiffData(settings.QUANDLAPIKEY, 'https://www.quandl.com/api/v1/datasets/YAHOO/INDEX_GSPC.json?')
    nasdaqdata = fetchData(settings.QUANDLAPIKEY, 'https://www.quandl.com/api/v1/datasets/NASDAQOMX/COMP.json?')
    everyData['nasdaq'] = nasdaqdata
    everyData['nasdaqdiff'] = rdiffData(settings.QUANDLAPIKEY, 'https://www.quandl.com/api/v1/datasets/NASDAQOMX/COMP.json?')
    everyData['apple'] = fetchstockData(settings.QUANDLAPIKEY, 'https://www.quandl.com/api/v1/datasets/GOOG/NASDAQ_AAPL.json')
    everyData['applediff'] = rdiffData(settings.QUANDLAPIKEY, 'https://www.quandl.com/api/v1/datasets/GOOG/NASDAQ_AAPL.json')
    return render(request, 'windopen/quandl.html', { 'everyData': everyData })

#################
#  NYTIMES API  #
#################

def nytimespop(request):
    '''Returns JSON response about the most viewed articles for the last 24 hours.'''
    popdata = fetcharticle(settings.POPAPIKEY, 'http://api.nytimes.com/svc/mostpopular/v2/mostviewed/all-sections/1.json?')
    return JSONResponse({'data': popdata})

def nytimestop(request):
    '''Returns JSON response about the articles located in the homepage'''
    topdata = fetcharticle(settings.TOPAPIKEY, 'http://api.nytimes.com/svc/topstories/v1/home.json?')
    return JSONResponse({'data': topdata})

def nytimesarticles(request):
    everyData = {}
    popdata = fetcharticle(settings.POPAPIKEY, 'http://api.nytimes.com/svc/mostpopular/v2/mostviewed/all-sections/1.json?')
    topdata = topdata = fetcharticle(settings.TOPAPIKEY, 'http://api.nytimes.com/svc/topstories/v1/home.json?')
    everyData['top'] = topdata
    everyData['pop'] = popdata
    return render(request, 'windopen/nytimes.html', { 'everyData': everyData })

#################
#   GITHUB API  #
#################

def githubUser(request):
    '''Returns Github Profile data for a specific user.'''
    parsedData = {}
    if request.method == 'POST':
        user = request.POST.get('user')
        parsedData['userData'] = getUserData(user, settings.GITHUB_CLIENT_ID, settings.GITHUB_CLIENT_SECRET)
    return render(request, 'windopen/github.html', {'data': parsedData})

def githubTopRepositories(request):
    '''Returns Top Commited Repositories for a specific Github User'''

    parsedData = {}
    if request.method == 'POST':
        user = request.POST.get('user')
        repositories = getUserRepositories(user, settings.GITHUB_CLIENT_ID, settings.GITHUB_CLIENT_SECRET)
        list = getTopContributedRepositories(user, repositories, settings.GITHUB_CLIENT_ID, settings.GITHUB_CLIENT_SECRET)
        filtered = filterCommits(list)
        parsedData['committed'] = filtered
        print parsedData
    return render(request, 'windopen/githubTopRepositories.html', {'data': parsedData})

def githubResume(request):
    '''A sample application which pulls various Github data to form a Resume of sorts'''

    allData = {}
    userData = getUserData('DrkSephy', settings.GITHUB_CLIENT_ID, settings.GITHUB_CLIENT_SECRET)
    repositories = getUserRepositories('DrkSephy', settings.GITHUB_CLIENT_ID, settings.GITHUB_CLIENT_SECRET)
    list = getTopContributedRepositories('DrkSephy', repositories, settings.GITHUB_CLIENT_ID, settings.GITHUB_CLIENT_SECRET)
    filtered = filterCommits(list)
    stargazers = getStarGazerCount('DrkSephy', settings.GITHUB_CLIENT_ID, settings.GITHUB_CLIENT_SECRET)
    filteredStargazers = filterStarGazerCount(stargazers)
    forkedRepos = getForkedRepositories('DrkSephy', settings.GITHUB_CLIENT_ID, settings.GITHUB_CLIENT_SECRET)
    allData['userData'] = userData
    allData['filteredData'] = filtered
    allData['filteredStargazers'] = filteredStargazers
    allData['forkedRepos'] = forkedRepos
    return render(request, 'windopen/githubResume.html', { 'data': allData })


#################
#   TUMBLR API  #
#################

def tumblr(request):
    ''' Tumblr api calls '''
    if getTumblr.is_authorized:
        #get blogger twitterthecomic's blog information
        blog = getTumblr.getBlogInfo('twitterthecomic')
        #get tags that was tagged along starbucks
        tagged_blog = getTumblr.getTaggedInfo("starbucks")
        #get blog information tagged with starbucks
        blogontag = getTumblr.getTaggedBlog("starbucks")
    else:
        blog, tagged_blog, blogontag = '', '',''
        global profile_track
        profile_track = 'tumblr'
        tumblr_url = getTumblr.authorize_url()
        return HttpResponseRedirect(tumblr_url)

    context = {'title': "What's up Starbucks?", 'blogData': blog, 'blogTag': tagged_blog, 'blogontag': blogontag}
    return render(request, 'windopen/tumblr.html', context)


####################
#   INSTAGRAM API  #
####################

def instagram(request):
    print getInstagram.is_authorized

    if getInstagram.is_authorized:
        if request.method == 'GET':
            if request.GET.items():
                instagram_tag = request.GET.get('instagram_tag')
                instagramUser = InstagramProfile.objects.get(user = request.user)
                tagged_media = getTaggedMedia(instagram_tag, instagramUser.access_token)
            else:
                instagram_tag, tagged_media = '', ''
    else:
        global profile_track
        profile_track = 'instagram'
        instagram_url =getInstagram.get_authorize_url()
        return HttpResponseRedirect(instagram_url)

    context = {'title': 'Instagram', 'tagged_media': tagged_media, 'search_tag': instagram_tag}
    return render(request, 'windopen/instagram.html', context)

def instagramUser(request):
    ''' Returns JSON response about a specific Instagram User. '''

    access_token = InstagramProfile.objects.get(instagram_user='mk200789').access_token
    parsedData = getUserInfo(access_token)
    return JsonResponse({ 'data': parsedData })

def instagramUserMedia(request):
    ''' Returns JSON response about a specific Instagram User's Media. '''

    access_token = InstagramProfile.objects.get(instagram_user='mk200789').access_token
    parsedData = getUserMedia(32833691, access_token)
    return JsonResponse({'data': parsedData })

def instagramMediaByLocation(request):
    print request.user
    if request.method == 'GET':
        if request.GET.items():
            #check if user has a User profile
            if request.user in User.objects.all():
                #check if user has an Instagram profile
                user = User.objects.get(username=request.user)
                #if user has an Instagram profile, query the search
                if InstagramProfile.objects.all().filter(user=user.id):
                    address = request.GET.get('address_field')
                    access_token = InstagramProfile.objects.get(user=user.id).access_token
                    geocode_result = searchForLocation(address)
                    if geocode_result:
                        location_ids = searchLocationIds(geocode_result['lat'], geocode_result['lng'], access_token)
                        media = searchLocationMedia(location_ids, access_token)
                        title = address
                        err_msg = ''
                else:
                    title, media, err_msg, location_ids, geocode_result = 'Media by location','', str(request.user)+ ' does not have an InstagramProfile','', ''
        else:
            title, media, err_msg, location_ids, geocode_result = 'Media by location', '','', '', ''


    context = {'title': title, 'geocode_result':geocode_result, 'media':media, 'list_id':location_ids, 'err_msg': err_msg}
    return render(request, 'windopen/instagram_q.html', context)


####################
#   TWITTER API    #
####################

def twitter(request):
    if getTwitter.is_authorized:
        value = getTwitter.get_trends_available(settings.YAHOO_CONSUMER_KEY)
    else:
        global profile_track
        profile_track = 'twitter'
        twitter_url = getTwitter.get_authorize_url()
        return HttpResponseRedirect(twitter_url)

    context ={'title': 'twitter', 'value': value}
    return render(request, 'windopen/twitter.html', context)

def twitterTweets(request):
    print getTwitter.is_authorized
    if getTwitter.is_authorized:
        if request.method == 'GET':
            if request.GET.items():
                tweets = request.GET.get('tweets')
                content, jsonlist = getTwitter.get_tweets(tweets)
            else:
                content, jsonlist = '', ''
    else:
        global profile_track
        profile_track = 'twitter'
        twitter_url = getTwitter.get_authorize_url()
        return HttpResponseRedirect(twitter_url)

    context ={'title': 'twitter tweet', 'content': content, 'data': jsonlist}
    return render(request, 'windopen/twitter_tweet.html', context)


##################
#  LINKEDIN  API #
##################

def linkedin(request):
    if getLinkedIn.is_authorized:
        content = getLinkedIn.getUserInfo()
    else:
        global profile_track
        profile_track = 'linkedin'
        linkedin_url = getLinkedIn.get_authorize_url()
        return HttpResponseRedirect(linkedin_url)

    context = {'title': 'linkedin example', 'content': content}
    return render(request, 'windopen/linkedin.html', context)


#########################
# Snippet RESTful Model #
#########################

class CRUDBaseView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    pass

class SnippetView(CRUDBaseView):
    serializer_class = SnippetSerializer
    queryset = Snippet.objects.all()


##################
#   Twilio API   #
##################

def twilio(request):
    if request.method == 'POST':
        number = request.POST.get('number')
        message = request.POST.get('message')
        sendSMS(str(message), str(number), '+13473781813')
        context = {'message': 'Your message has been sent successfully!'}
        return HttpResponseRedirect('/hackathon/api/')
    return render(request, 'windopen/twilio.html')


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


def instagram_login(request):
    global profile_track
    profile_track = 'instagram'
    instagram_url = getInstagram.get_authorize_url()
    return HttpResponseRedirect(instagram_url)

def tumblr_login(request):
    global profile_track
    profile_track = 'tumblr'
    tumblr_url = getTumblr.authorize_url()
    return HttpResponseRedirect(tumblr_url)

def twitter_login(request):
    global profile_track
    profile_track = 'twitter'
    twitter_url = getTwitter.get_authorize_url()
    return HttpResponseRedirect(twitter_url)

def github_login(request):
    global profile_track
    profile_track = 'github'
    github_url = getGithub.get_authorize_url()
    return HttpResponseRedirect(github_url)

def linkedin_login(request):
    global profile_track
    profile_track = 'linkedin'
    linkedin_url = getLinkedIn.get_authorize_url()
    return HttpResponseRedirect(linkedin_url)

def facebook_login(request):
    global profile_track
    profile_track = 'facebook'
    facebook_url = getFacebook.get_authorize_url()
    return HttpResponseRedirect(facebook_url)


def google_login(request):
    global profile_track
    profile_track = 'google'
    google_url = getGoogle.get_authorize_url()
    return HttpResponseRedirect(google_url)

def dropbox_login(request):
    global profile_track
    profile_track = 'dropbox'
    dropbox_url = getDropbox.get_authorize_url()
    return HttpResponseRedirect(dropbox_url)

def foursquare_login(request):
    global profile_track
    profile_track = 'foursquare'
    forsquare_url = getFoursquare.get_authorize_url()
    return HttpResponseRedirect(forsquare_url)
