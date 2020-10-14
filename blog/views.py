from django.contrib.messages.api import success
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin   # we cant't use decorators for classes so we use mixing instead
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

def home(request):
	context = { 'post':Post.objects.all() }
	return render(request, 'blog/home.html',context)

def about(request):
	return render(request, 'blog/about.html')

class PostListView(ListView):                       # Creates a list view of posts on the home page
	model = Post
	template_name = 'blog/home.html'
	context_object_name = 'post'
	ordering = ['-date_posted']
	paginate_by = 5

class UserPostListView(ListView):                       # Creates a list view of posts by a particular user
	model = Post
	template_name = 'blog/user_posts.html'
	context_object_name = 'post'
	paginate_by = 5

	def get_queryset(self):                             # filter out post according to user passed through url
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):                  # Detail view for post/blog          
	model = Post

# postcreateview and postupdate view both use same template post_form.html which is according to naming convention
# for create and update view i.e. <model name >_form.html
class PostCreateView(LoginRequiredMixin, CreateView):                           
	model = Post
	fields = ['title', 'content']

	def form_valid(self,form):                    # overriding form_valid method so that before form is submitted set
		form.instance.author = self.request.user  # author of the instance of form to current logged in user 
		return super().form_valid(form)      # this line runs form valid method on parent class


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):                           
	model = Post
	fields = ['title', 'content']

	def form_valid(self,form):                    
		form.instance.author = self.request.user  
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		else:
			return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):                        
	model = Post 
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		else:
			return False