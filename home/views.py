from django.shortcuts import render, get_object_or_404
from .models import Post, Prefrances
from django.db.models import Q
from django.views.generic import ListView, DetailView
from itertools import chain
from django.contrib.auth.decorators import login_required
from django.contrib import messages

'''class SearchDetailView(DetailView):
    model = Post
    template_name = 'home/search_detail.html'
    '''
def home(request):
    qs = Post.objects.all()
    qs_chain = chain(qs)
    qslis = sorted(qs_chain, key=lambda instance: instance.pk, reverse = True)
    qslength = len(qslis) - 1
    context = {
        "posts": qs,
        "howmany" : qslength,
        "title" : True
    }
    return render(request, 'home/base.html', context)

class SearhListView(ListView):
    template_name = 'home/home.html'
    ordering = ['-date_posted']
    count = 0
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('search')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('search', None)

        if query is not None:
            post_result = Post.objects.search(query)
            queryset_chain = chain(
                post_result
            )
            qs = sorted(queryset_chain, key=lambda instance: instance.pk, reverse = True)
            self.count = len(qs)
            
            return qs
        return Post.objects.none()
def search_detail(request, id=None):
    eachpost = get_object_or_404(Post, id=id)
    context = {"eachpost":eachpost}
    return render(request, "home/search_detail.html", context)
@login_required
def searchpreference(request, postid, userpreference):
    if request.method =="POST":
        eachpost = get_object_or_404(Post, id=postid)
        obj=''
        valueobj=''
        try:
            obj = Prefrances.objects.get(user=request.user, post=eachpost)
            valueobj = obj.value#value of the userprefernce
            valueobj = int(valueobj)
            userpreference = int(userpreference)
            if valueobj != userpreference:
                obj.delete()
                upref = Prefrances()
                upref.user = request.user
                upref.post = eachpost
                upref.value = userpreference
                if userpreference == 1 and valueobj != 1:
                    eachpost.likes += 1
                    eachpost.dislikes -=1 
                elif userpreference == 2 and valueobj != 2:
                    eachpost.likes -= 1
                    eachpost.dislikes += 1
                upref.save()
                eachpost.save()
                context={
                    "eachpost" : eachpost,
                    "postid": postid
                }
                return render(request, 'home/search_detail.html', context)
            elif valueobj == userpreference:
                obj.delete()

                if userpreference == 1:
                    eachpost.likes -=1
                elif userpreference == 2:
                    eachpost.dislikes -=1
                eachpost.save()
                context = {
                    "eachpost" : eachpost,
                    "postid" : postid
                }
                return render(request, "home/search_detail.html", context)
            
        
        except Prefrances.DoesNotExist: 
            upref = Prefrances()
            upref.user = request.user
            upref.post = eachpost
            upref.value = userpreference
            userpreference = int(userpreference)
            if userpreference == 1:
                eachpost.likes += 1
            elif userpreference == 2:
                eachpost.dislikes += 1
            upref.save()
            eachpost.save()
            context = {
                "eachpost" : eachpost,
                "postid" : postid
            }
            return render(request, "home/search_detail.html", context)
    else:
        eachpost=get_object_or_404(Post, id=postid)
        context ={
            "eachpost" : eachpost,
            "postid" : postid
        }
        return render(request, "home/search_detail.html", context)

def about(request):
    return render(request, 'home/about.html')
