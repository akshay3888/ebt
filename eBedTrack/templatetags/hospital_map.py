from django.utils import timezone
from django import template
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.forms import forms
from django.db.models import Count
from django.http import HttpResponseRedirect
# from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.db.models.functions import Upper,Lower
from django.template.defaultfilters import urlencode,force_escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def hospital_map(query):
    return mark_safe('http://maps.google.com/maps?t=m&amp;q=%s' % urlencode(force_escape(query)))

