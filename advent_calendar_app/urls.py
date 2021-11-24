from django.urls import path

from advent_calendar_app.views import MRCSkillAdventCalendarView, CalendarTaskView

urlpatterns = [
    path('', MRCSkillAdventCalendarView.as_view(), name='mrc-skills-advent-calendar'),
    path('day/<slug:slug>', CalendarTaskView.as_view(), name='mrc-skills-advent-calendar-day'),
]