from django.shortcuts import render
from .extract_daily import importt, exportt
import gspread
import asyncio

# Create your views here.
def ext(request):
    gc = gspread.service_account()
    sh = gc.open("FM_input")

    importt(sh)
    exportt(sh)
    return render(request, 'hello_world.html')

