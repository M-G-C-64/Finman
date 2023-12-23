from django.shortcuts import render

import asyncio

# async def workk():
#     gc = gspread.service_account()
#     sh = gc.open("FM_input")

#     importt(sh)
#     exportt(sh)

# Create your views here.
def ext(request):

    try:
        # from .extract_daily import importt, exportt
        # import gspread
        # gc = gspread.service_account()
        # sh = gc.open("FM_input")

        # importt(sh)
        # exportt(sh)
    
        # task = asyncio.create_task(workk())
        # asyncio.run(asyncio.sleep(8))

        return render(request, 'hello_world.html')
    
    except:
        return render(request, 'failed.html')



