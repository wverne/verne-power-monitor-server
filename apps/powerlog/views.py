import datetime
import pytz

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET

from ..sensor.models import Sensor

from .forms import PowerLogForm
from .models import PowerLog


@login_required
def post_log(request):
    """
    Allow users to post new power logs to the server.
    """
    sensors = Sensor.objects.order_by('name')

    if request.method == 'POST':
        form = PowerLogForm(request.POST)
        if form.is_valid():
            PowerLog.objects.create(
                timestamp=datetime.datetime.now(tz=pytz.UTC),
                sensor=form.cleaned_data['sensor'],
                network_ssid=form.cleaned_data['network_ssid'],
                network_local_ip=form.cleaned_data['network_local_ip']
            )
    else:
        form = PowerLogForm()

    return render(request, 'powerlog/post_log.html', {
        'form': form,
        'sensors': sensors
    })


@login_required
@require_GET
def recent_logs(request):
    """
    Display a table of recent power logs.
    """
    recent_power_logs = PowerLog.objects\
        .select_related('sensor')\
        .order_by('-timestamp')[:10]
    return render(request, 'powerlog/recent_logs.html', {
        'recent_power_logs': recent_power_logs
    })
