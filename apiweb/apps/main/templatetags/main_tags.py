from django import template

from ...survey.models import JobAfterLeaving

register = template.Library()


@register.simple_tag(name="get_which_job")
def get_which_job(which_position_value):
    return JobAfterLeaving.WHICH_POSITION_CHOICES[int(which_position_value)][1]


@register.simple_tag(name="get_which_job_long")
def get_which_job_long(which_position_value):
    jobname = get_which_job(which_position_value)
    if jobname == "Current":
        return jobname + " Position"
    else:
        return jobname + " Job after Leaving API"
