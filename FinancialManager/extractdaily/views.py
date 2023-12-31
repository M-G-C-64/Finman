from django.shortcuts import render

import asyncio

# async def workk():
#     gc = gspread.service_account()
#     sh = gc.open("FM_input")

#     importt(sh)
#     exportt(sh)

# Create your views here.
def ext(request):
    return render(request, 'hello_world.html')


def default(request):

    try:
        from .extract_daily import importt, exportt, graphs
        import gspread
        gc = gspread.service_account()
        sh = gc.open("FM_input")

        importt(sh)
        exportt(sh)
        graphs()
        

    # task = asyncio.create_task(workk())
    # asyncio.run(asyncio.sleep(8))
        return render(request, 'default.html')
    
    except:
        return render(request, 'failed.html')

def graphs(request):
    numbers = range(1,11)
    return render(request, 'graphs.html', {'numbers': numbers})

def sql_upload(request):
    try:
        if request.method == 'POST':
            from .extract_daily import custom_graphs

            sql_input = request.POST['sql_input']
            x_axis = request.POST['x_axis']
            y_axis = request.POST['y_axis']

            custom_graphs(sql_input, x_axis, y_axis)
            print("custom_graphs complete")
            return render(request, 'sql_upload.html')
    except:
        return render(request, 'failed.html')

