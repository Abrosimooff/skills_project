"""skills URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from colors_app.views import MRCSkillColorsView
# from core.views.test import MRCTestView
from memory_app.views import MRCMemoryGameView
from online_dozor_app.views import MRCOnlineDozorView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('skills/marusia/colors/', MRCSkillColorsView.as_view(), name='mrc-skills-colors'),
    path('skills/marusia/memory/', MRCMemoryGameView.as_view(), name='mrc-skills-memory'),
    path('skills/marusia/online_dozor/', MRCOnlineDozorView.as_view(), name='mrc-skills-online-dozor'),
    # path('skills/test/', MRCTestView.as_view(), name='mrc-test'),

    path('skills/marusia/advent_calendar/', include('advent_calendar_app.urls'))
    # path('skills/marusia/santa/', include('santa_app.urls'))

]
