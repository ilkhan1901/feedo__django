from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.views.generic import ListView
from taggit.models import Tag

from .models import Post
from .forms import EmailPostForm, CommentForm


class PostListView(ListView):
	paginate_by = 3
	template_name = 'blog/index.html' 

	def get_queryset(self):
		queryset = Post.published.all()
		if self.kwargs.get('tag_slug'):
			tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
			queryset = queryset.filter(tags__in=[tag])
		return queryset 

	def get(self,request,*args,**kwargs):
		context = locals()
		context['tag'] = self.kwargs.get('tag_slug')
		context['posts'] = self.get_queryset()
		if request.GET.get('from'):
			context['from'] = get_object_or_404(Post,id=request.GET['from'],status='published') 

		return render(request,self.template_name,context)



def post(request,post,year,month,day):

	post = get_object_or_404(
		Post,
		slug=post,
		status='published',
		publish__year=year,
		publish__month=month,
		publish__day=day
	) 

	post_tag_ids = post.tags.values_list('id',flat=True)
	similar_posts = Post.published.filter(tags__in=post_tag_ids)\
		.exclude(id=post.id).annotate(same_tags=Count('tags'))\
		.order_by('-same_tags','-publish')[:4]

	comments = post.comments.filter(active=True)
	new_comment = None

	if request.method == 'POST':
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False)
			new_comment.post = post
			new_comment.save()
	else:
		comment_form = CommentForm()

	return render(
		request, 
		'blog/post.html', 
		{
			'id':id,
			'post':post,
			'comments':comments,
			'new_comment':new_comment,
			'comment_form':comment_form,
			'similar_posts':similar_posts
		}
	)


def post_share(request, post_id):

	post = get_object_or_404(Post,id=post_id,status='published')
	sent = False

	if request.method == 'POST':
		form = EmailPostForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subject = f'{cd["name"]} reccomends you read "{post.title}"'
			message = f'Read "{post.title} at {post_url}"\n\n' \
				f'{cd["name"]}\'s comments: {cd["comments"]}'
			send_mail(
				subject,message,
				from_email=getattr(settings,'DFAULT_FROM_EMAIL','nsit2002@gmail.com'),
				recipient_list=[cd['to']]
			)
			sent = True
	else:
		form = EmailPostForm()

	return render(request, 'blog/post_share.html', {'post':post,'form':form,'sent':sent})


def page_not_found(request, exception=None):

    # return render(request, '404.html')
    return redirect('/')