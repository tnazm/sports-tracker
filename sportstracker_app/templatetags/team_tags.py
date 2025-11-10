from django import template
from sportstracker_app.models import Team

register = template.Library()

@register.simple_tag
def team_by_name(name):
    # returns a Team or None
    return Team.objects.filter(name=name).first()
