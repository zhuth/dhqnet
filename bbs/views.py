from django.shortcuts import render, redirect
from django.db.models import Q

from models import Post, Log
import json

def dolog(request):
    fp = request.POST.get('fp', request.GET.get('fp', request.session.get('fp', '')))
    if fp == '': return
    request.session['fp'] = fp
    path = request.path
    if request.path == 'fp': path = request.META['HTTP_REFERER']
    Log(fp=fp, ua=request.META['HTTP_USER_AGENT'], url=path, args=request.META['QUERY_STRING'], post=json.dumps(request.POST)).log()

def fp(request):
    dolog(request)
    return render(request, 'show_levels.html')

# Create your views here.
def post(request, id):
    dolog(request)
    if request.method.lower() == 'get':
        if request.GET.get('action') == 'delete' and id != '':
            Post.objects.get(id=id).delete()
            return redirect('/')
        offset = int(request.GET.get('offset', '0'))
        posts = Post.objects
        if id != '':
            posts = posts.filter(link=int(id)).order_by('created')
        else:
            posts = posts.order_by('-created')
        posts = posts[offset:offset+10]
        return render(request, 'index.html', {
            'posts': posts, 
            'post': None if id == '' else Post.objects.get(id=id),
            'offset': offset,
            'offset_next': offset + 10,
            'offset_prev': offset - 10,
            'action': request.GET.get('action'),
            'link': id})
    else:
        args = request.POST
        content = args.get('content', '')
        url = None
        if len(request.FILES) > 0:
            import dhqnet.settings, time
            fname = ''
            for _ in request.FILES:
                ext = request.FILES[_].name
                ext = ext[ext.rfind('.'):].lower()
                if ext == '.jpeg': ext = '.jpg'
                fname += str(int(time.time() * 1000000)) + ext
                with open(dhqnet.settings.STATICFILES_DIRS[0] + '/uploads/' + fname, 'wb') as f:
                    f.write(request.FILES[_].read())
            url = "/static/uploads/%s" % (fname,)
        link = None if args.get('link', '') == '' else int(args.get('link'))
        if args.get('action') == 'edit':
            p = Post.objects.get(id=link)
            p.author = args.get('author', '')
            p.content = content
            p.url = url
            p.publish()
        else:
            Post(author=args.get('author', ''), content=content, url=url, link_id=link).publish()
        return redirect('/')