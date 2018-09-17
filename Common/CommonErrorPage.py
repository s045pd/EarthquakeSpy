from django.shortcuts import render_to_response

def handler404(request, *args, **argv):
    """定义默认的404界面
    
    """
    return render_to_response('404.html')
