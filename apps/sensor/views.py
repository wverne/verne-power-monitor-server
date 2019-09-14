import datetime
import pytz

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET

from ..powerlog.models import PowerLog

from .forms import SensorForm
from .models import Sensor


@login_required
def index(request):
    """
    Display the homepage. Redirects to list_sensors for now.
    """
    return redirect(list_sensors)


@login_required
@require_GET
def list_sensors(request):
    """
    Display a list of sensors.
    """
    sensors = Sensor.objects.order_by('name')
    return render(request, 'sensor/list_sensors.html', {
        'sensors': sensors
    })


@login_required
def create_sensor(request):
    """
    Allow a new sensor to be created.
    """
    if request.method == 'POST':
        form = SensorForm(request.POST)
        if form.is_valid():
            Sensor.objects.create(
                name=form.cleaned_data['name'],
                created_at=datetime.datetime.now(tz=pytz.UTC)
            )
    else:
        form = SensorForm()

    return render(request, 'sensor/sensor_create.html', {
        'form': form
    })


@login_required
def edit_sensor(request, sensor_id):
    """
    Allow a sensor to be edited.
    """
    sensor = get_object_or_404(Sensor, id=sensor_id)

    if request.method == 'POST':
        form = SensorForm(request.POST, instance=sensor)
        if form.is_valid():
            form.save()
    else:
        form = SensorForm(instance=sensor)

    return render(request, 'sensor/sensor_edit.html', {
        'sensor': sensor,
        'form': form
    })


@login_required
def delete_sensor(request, sensor_id):
    """
    Allow a sensor to be deleted.
    """
    sensor = get_object_or_404(Sensor, id=sensor_id)
    sensor_logs = PowerLog.objects.filter(sensor=sensor)

    if request.method == 'POST':
        sensor_logs.delete()
        sensor.delete()
        return redirect(list_sensors)

    return render(request, 'sensor/sensor_delete.html', {
        'sensor': sensor,
        'sensor_logs_count': sensor_logs.count()
    })
