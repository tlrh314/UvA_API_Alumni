from datetime import datetime, timedelta
from django.utils import timezone

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import DateFieldListFilter, FieldListFilter
from django.contrib.admin.filters import ChoicesFieldListFilter

class NullListFilter(admin.SimpleListFilter):
    def lookups(self, request, model_admin):
        return (
            ("1", _("Is Empty")),
            ("0",  _("Has a Value")),
        )

    def queryset(self, request, queryset):
        kwargs = { "{0}__isnull".format(self.parameter_name) : self.value() == "1" }
        if self.value() in ("0", "1"):
            return queryset.filter(**kwargs)
        return queryset

class EmptyEmailListFilter(NullListFilter):
    title = u"Email Address"
    parameter_name = "email"

class EmptyLastCheckedListFilter(NullListFilter):
    title = u"Date Last Checked"
    parameter_name = "last_checked"

def return_dates():
	dates_dict = {}
	# When time zone support is enabled, convert "now" to the user's time
	# zone so Django'sd efinition of "Today" matches what the user expects.
	now = datetime.now()

	if timezone.is_aware(now):
		now = timezone.localtime(now)

	today = now.replace(hour=0, minute=0, second=0, microsecond=0)
	yesterday = today - timedelta(days=1)

	if today.month == 1:
		last_month = today.replace(year=today.year-1, month=12, day=1)
	else:
		last_month = today.replace(month=today.month - 1, day=1)
	last_year = today.replace(year=today.year - 1, month=1, day=1)

	last_week = today - timedelta(days=7)

	this_month = today.replace(day=1)
	this_year = today.replace(day=1, month=1)

	day_ago = now - timedelta(days=1)
	week_ago = now - timedelta(days=7)
	month_ago = now - timedelta(days=31)
	year_ago = now - timedelta(days=365)

	dates_dict["now"] = now
	dates_dict["today"] = today
	dates_dict["yesterday"] = yesterday
	dates_dict["last_year"] = last_year
	dates_dict["this_year"] = this_year
	dates_dict["last_month"] = last_month
	dates_dict["this_month"] = this_month
	dates_dict["last_week"] = last_week
	dates_dict["day_ago"] = day_ago
	dates_dict["week_ago"] = week_ago
	dates_dict["month_ago"] = month_ago
	dates_dict["year_ago"] = year_ago

	return dates_dict

class SurveyListFilter(admin.SimpleListFilter):
	title = u"Date Last survey info update"
	parameter_name = "survey_info_updated"

	def lookups(self, request, model_admin):	
		return (
				("today", _("Today")),
				("past_7_days", _("Past 7 days")),
				("this_month", _("This month")),
				("this_year", _("This year")),

				("over_day_ago", _("Longer than a day ago")),
				("over_week_ago", _("Longer than a week ago")),
				("over_month_ago", _("Longer than a month ago")),
				("over_year_ago", _("Longer than a year ago")),

				("no_date", _("No date")),
				("has_date", _("Has date")),
			)

	def queryset(self, request, queryset):
		value = self.value()
		self.dates_dict = return_dates()

		if value == None:
			return queryset		

		if value == "today":
			queryset = queryset.filter(survey_info_updated__lt=self.dates_dict["now"])
			queryset = queryset.filter(survey_info_updated__gte=self.dates_dict["today"])

		if value == "past_7_days":
			queryset = queryset.filter(survey_info_updated__lt=self.dates_dict["now"])
			queryset = queryset.filter(survey_info_updated__gte=self.dates_dict["last_week"])

		if value == "this_month":
			queryset = queryset.filter(survey_info_updated__lt=self.dates_dict["now"])
			queryset = queryset.filter(survey_info_updated__gte=self.dates_dict["this_month"])

		if value == "this_year":
			queryset = queryset.filter(survey_info_updated__lt=self.dates_dict["now"])
			queryset = queryset.filter(survey_info_updated__gte=self.dates_dict["this_year"])

		if value == "over_day_ago":
			queryset = queryset.exclude(survey_info_updated__gte=self.dates_dict["day_ago"])

		if value == "over_week_ago":
			queryset = queryset.exclude(survey_info_updated__gte=self.dates_dict["week_ago"])

		if value == "over_month_ago":
			queryset = queryset.exclude(survey_info_updated__gte=self.dates_dict["month_ago"])

		if value == "over_year_ago":
			queryset = queryset.exclude(survey_info_updated__gte=self.dates_dict["year_ago"])

		if value == "no_date":
			queryset = queryset.filter(survey_info_updated__isnull=True)

		if value == "has_date":
			queryset = queryset.filter(survey_info_updated__isnull=False)

		return queryset