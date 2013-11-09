#coding=utf8
from models import Post,Category,Page,Widget
from xiaojunBlog.settings import  PAGE_NUM , RECENTLY_NUM ,HOT_NUM , FIF_MIN
from django.views.generic import ListView,DetailView
from django.shortcuts import  render
from django.core.paginator import  Paginator
from django.db.models import Q
from utils.cache import  LRUCacheDict,cache
import logging

logger=logging.getLogger(__name__)

class BaseMixin(object):
    def get_context_data(self,*args,**kwargs):
        context = super(BaseMixin,self).get_context_data(**kwargs)

        try:
            context['categories'] = Category.available_list()
            context['widgets'] = Widget.available_list()
            context['recently_posts'] = Post.get_recently_posts(RECENTLY_NUM)
            context['hot_posts'] = Post.get_hots_posts(HOT_NUM)
            context['pages'] = Page.objects.filter(status=0)
            if cache.get('online.ips')!= None:
                context['online_num'] = len(cache.get('online_ips'))
        except Exception as e:
            logger.exception(u'加载基本信息出错[%s]',e)

        return context



class IndexView(BaseMixin, ListView):
    query = None
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        try:
            self.cur_page = int(request.GET.get('page',1))
        except TypeError:
            self.cur_page = 1

        if self.cur_page < 1:
            self.cur_page = 1

        return super(IndexView,self).get(request,*args,**kwargs)


    def get_context_data(self, **kwargs):

        paginator = Paginator(self.object_list,PAGE_NUM)
        kwargs['posts'] = paginator.page(self.cur_page)
        kwargs['query'] = self.query
        kwargs['title'] = "WeirdBird的储忆柜"
        return super(IndexView,self).get_context_data(**kwargs)

    def get_queryset(self):
        self.query = self.request.GET.get('s')
        if self.query:
            qarg =(
                Q(title__icontains=self.query) |
                Q(content__icontains=self.query)
            )
            posts = Post.objects.defer('content','content_html').filter(qarg,status=0)
            for post in posts:
                post.title = post.title.replace(self.query,'<font color="red">%s</font>'%self.query)
                # post.summary = post.summary.replace(self.query,'<font color="red">%s</font>'%self.query)

        else:

            posts = Post.objects.defer('content','content_html').filter(status=0)

        return  posts

class CategoryListView(IndexView):

    def get_queryset(self):
        alias = self.kwargs.get('alias')

        try:
            self.category = Category.objects.get(alias = alias)
        except Category.DoesNotExist:
            return  []

        posts = self.category.post_set.defer('content','content_html').filter(status = 0)
        return posts

    def get_context_data(self, **kwargs):
        if hasattr(self,'category'):
            kwargs['title'] = self.category.name + ' | '

        return super(CategoryListView, self).get_context_data(**kwargs)

class TagsListView(IndexView):
    def get_queryset(self):

        self.tag = self.kwargs.get('tag')

        posts = Post.objects.defer('content','content_html').filter(tags__icontains=self.tag,status=0)

        return posts

    def get_context_data(self, **kwargs):
        kwargs['title'] = self.tag+ ' | '
        return super(TagsListView,self).get_context_data(**kwargs)

class PostDetailView(BaseMixin,DetailView):
    object = None
    template_name = 'detail.html'
    queryset = Post.objects.filter(status=0)
    slug_field = 'alias'

    def get(self,request,*args,**kwargs):
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        self.cur_user_ip = ip
        alias = self.kwargs.get('slug')
        visited_ips = cache.get(alias,[])
        if ip not in visited_ips:
            try:
                post=self.queryset.get(alias=alias)
            except Post.DoesNotExist:
                logger.error(u'该文章不存在:[%s]'%alias)
                context = super(PostDetailView,self).get_context_data(**kwargs)
                return render(request,'404.html',context)
            else:
                post.view_times +=1
                post.save()
                visited_ips.append(ip)
                self.set_lru_read(ip,post)

            cache.set(alias,visited_ips,FIF_MIN)

        return super(PostDetailView,self).get(request,*args,**kwargs)

    def set_lru_read(self, ip, post):
        #保存别人正在读
        lru_views = cache.get('lru_views')
        print("保存别人正在读取%s"%lru_views)
        if not lru_views:
            lru_views = LRUCacheDict(max_size=10, expiration=FIF_MIN)

        if post not in lru_views.values():
            lru_views[ip] = post

        cache.set('lru_views', lru_views, FIF_MIN)
        print("set 完成后的%s"%cache.get('lru_views'))


    def get_context_data(self, **kwargs):
        context = super(PostDetailView,self).get_context_data(**kwargs)
        post = self.get_object()
        next_id = post.id +1
        prev_id = post.id -1

        try:
            next_post = self.queryset.get(id=next_id)
        except Post.DoesNotExist:
            next_post = None

        try:
            prev_pst = self.queryset.get(id=prev_id)
        except Post.DoesNotExist:
            prev_pst = None
        context['next_post'] = next_post
        context['prev_post'] = prev_pst
        if cache.get('lru_views') != None:
            context['lru_views'] = cache.get('lru_views').items()

        context['cur_user_ip'] = self.cur_user_ip
        context['related_posts'] = post.related_posts

        return context


class PagedetailView(BaseMixin,DetailView):
    template_name = "page.html"
    queryset = Page.objects.filter(status=0)
    slug_field = 'alias'
    object = None
    def get(self,request,*args,**kwargs):
        alias=self.kwargs.get('slug')
        try:
            self.object=self.queryset.get(alias=alias)
            context=self.get_context_data(object=self.object)
        except Page.DoesNotExist:
            logger.error(u'该界面不存在:[%s'%alias)
            context = self.get_context_data(**kwargs)
            return render(request,'404.html',context)

        return self.render_to_response(context)



















