from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CommentForm
from .models import Post, Category,Tag
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
# Create your views here.

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ["title","content","head_image","file_upload","category","tag"]
    template_name = 'blog/post_form_update.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate,self).dispatch(request,*args,**kwargs)
        else:
            raise PermissionDenied
class PostCreate(LoginRequiredMixin,UserPassesTestMixin, CreateView):
    model = Post
    fields = ["title","content","head_image","file_upload","category","tag"]

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            return super(PostCreate,self).form_valid(form)
        else:
            return redirect('/blog/')
    def get_context_data(self, **kwargs):
        context = super(PostCreate,self).get_context_data()
        context['categories']=Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context
class PostList(ListView):
    model=Post
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        context = super(PostList,self).get_context_data()
        context['categories']=Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

class PostDetail(DetailView):
    model=Post
    def get_context_data(self, **kwargs):
        context = super(PostDetail,self).get_context_data()
        context['categories']=Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        context['comment_form'] = CommentForm
        return context
    # template_name = 'blog/post_detail.html'

# def index(request):
#     posts = Post.objects.all().order_by('-pk')
#     return render(
#         request,
#         'blog/post_list.html',
#         {
#             'posts':posts
#         }
#     )
# def single_post_page(request,pk):
#     post = Post.objects.get(pk=pk)
#     return render(
#         request,
#         'blog/single_post_page.html',
#         {
#             'post':post
#         }
#     )

def categories_page(request,slug):
    if slug=='no-category':
        category='미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    context = {
        'categories':Category.objects.all(),
        'category_less_post_count':Post.objects.filter(category=None).count(),
        'category':category,
        'post_list':post_list,


    }
    return render(request,'blog/post_list.html',context)

def tag_page(request,slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()
    context = {
        'tag':tag,
        'categories': Category.objects.all(),
        'post_list': post_list,
        'category_less_post_count': Post.objects.filter(category=None).count(),
    }
    return render(request,'blog/post_list.html',context)

def new_comment(request,pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post,pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied