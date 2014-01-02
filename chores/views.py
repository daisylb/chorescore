from django.views.generic import ListView
from . import models
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.contrib import messages
from django.db.models import Sum, Max
from django.contrib.auth.models import User
from .lib import template
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required

class ChoreList (ListView):
    model = models.Chore
    template_name = "chore_list.html"

@template('chore_list.html')
def chore_list(request):
    if request.user.is_authenticated():
        return {
            'chores': models.Chore.objects.all().annotate(
                last_performed=Max('events__performed_at')
            ).order_by('category'),
            'scoreboard': models.get_scoreboard(14),
            'last10': models.ChoreEvent.objects.all().order_by('-performed_at')[:10]
        }
    else:
        return {'__template__': 'login.html'}

@login_required
@template('chore_done.html')
def mark_chore_done(request, chore_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed()

    chore = models.Chore.objects.get(id=chore_id)

    # Enforce a 60-second time limit
    time_limit = datetime.now() - timedelta(seconds = 60)
    evts_in_time_limit = models.ChoreEvent.objects.filter(
            chore=chore, user=request.user, performed_at__gte=time_limit)
    if len(evts_in_time_limit) > 0:
        return {
            '__template__': 'chore_rate_limited.html',
            'chore': chore,
            'time_limit': 60,
        }

    chore_event = models.ChoreEvent(chore=chore, user=request.user)
    chore_event.save()

    return {
        'chore_event': chore_event,
        'scoreboard': models.get_scoreboard(14),
        'scoreboard_days': 14,
    }
