from django.shortcuts import render
from .models import Post, Category,Tag
from django.views.generic import ListView,DetailView
# Create your views here.

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