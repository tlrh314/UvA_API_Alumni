from django import template

from ...survey.models import JobAfterLeaving

register = template.Library()


@register.simple_tag(name="get_which_job")
def get_which_job(which_position_value):
    jobname = JobAfterLeaving.WHICH_POSITION_CHOICES[int(which_position_value)][1]
    if jobname == "Current":
        return jobname + " Position"
    else:
        return jobname + " Job after Leaving API"

