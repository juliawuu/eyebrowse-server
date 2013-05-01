from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import redirect

from annoying.decorators import render_to, ajax_request

from common.view_helpers import _template_values

from live_stream.query_managers import *

@login_required
@render_to('live_stream/home.html')
def home(request):

    user = request.user
    
    history_stream = live_stream_query_manager(request.GET, request.user)

    num_history = EyeHistory.objects.all().count()

    num_online = online_user_count()

    subnav = "subnav_" + request.GET.get('filter', "following")

    return _template_values(request, page_title="live stream", navbar="nav_home", sub_navbar=subnav, history_stream=history_stream, num_history=num_history, num_online=num_online)

@login_required
@ajax_request
def ping(request):

    history = live_stream_query_manager(request.GET, request.user, return_type="list")
    
    return {
        'history' : history,
        'num_history' : EyeHistory.objects.all().count(),
        'num_online' : online_user_count(),
        'is_online' : online_user(request.GET.get("username", ""))
    }

@login_required
def search(request):
    return home(request)