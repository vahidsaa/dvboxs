from django.shortcuts import render
from dailylist.models import TodayList, Today

# Create your views here.

def today_list(request):
    today = Today.objects.last()
    today_list= TodayList.objects.all().order_by('-pk')
    return render(request, 'dailylist/today_list.html', {'today_list':today_list, 'today':today})
