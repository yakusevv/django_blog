from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.views.generic import View
from django.urls import reverse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.contrib.auth import login

from .models import Post, Tag, Profile
from .utils import *
from .forms import TagForm, PostForm, SignUpForm, UserForm, ProfileForm
from .tokens import account_activation_token

def posts_list(request):
    search_query = request.GET.get('search', '')

    if search_query:
        posts = Post.objects.filter(
        Q(title__icontains=search_query)|
        Q(body__icontains=search_query)
        )
        if not posts.count():
            no_results = True
            return render(request, 'blog/index.html', context={
                                                        'no_results': no_results,
                                                        'search_query': search_query
                                                        })
        else:
            no_results = False
    else:
        posts = Post.objects.all()

    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
        'search_query': search_query,
        'page_object': page,
        'is_paginated': is_paginated,
        'prev_url': prev_url,
        'next_url': next_url
    }

    return render(request, 'blog/index.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your Blog account'
            message = render_to_string('registration/account_activation_email.html',
                        {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user)
                        })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', context={'form': form})


def account_activation_sent(request):
    return render(request, 'registration/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.groups.add(Group.objects.get(name__icontains='Members'))
        user.save()
        login(request, user)
        return redirect('posts_list_url')
    else:
        return render(request, 'registration/account_activation_invalid.html')


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'


class PostCreate(PermissionRequiredMixin, ObjectCreateMixin, View):
    model_form = PostForm
    template = 'blog/post_create_form.html'
    permission_required = 'blog.can_create'
    raise_exception = True


class PostUpdate(PermissionRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'blog/post_update_form.html'
    permission_required = 'blog.can_update'
    raise_exception = True


class PostDelete(PermissionRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    template = 'blog/post_delete_form.html'
    redirect_url = 'posts_list_url'
    permission_required = 'blog.can_delete'
    raise_exception = True


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag_detail.html'


class TagCreate(PermissionRequiredMixin, ObjectCreateMixin, View):
    model_form = TagForm
    template = 'blog/tag_create.html'
    permission_required = 'blog.can_create'
    raise_exception = True


class TagUpdate(PermissionRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'blog/tag_update_form.html'
    permission_required = 'blog.can_update'
    raise_exception = True


class TagDelete(PermissionRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'blog/tag_delete_form.html'
    redirect_url = 'tags_list_url'
    permission_required = 'blog.can_delete'
    raise_exception = True


class UserProfileDetail(View):
    model = User
    template = 'blog/profile_detail.html'

    def get(self, request, pk):
        user = get_object_or_404(self.model, pk=pk)
        return render(request, self.template, context={'user': user})


class UserProfileUpdate(View):
    model1 = User
    model2 = Profile
    model_form1 = UserForm
    model_form2 = ProfileForm
    template = 'blog/profile_edit.html'

    def get(self, request, pk):
        obj1 = self.model1.objects.get(pk=pk)
        obj2 = self.model2.objects.get(user=obj1)
        bound_form1 = self.model_form1(instance=obj1)
        bound_form2 = self.model_form2(instance=obj2)
        return render(request, self.template, context={
         'form1': bound_form1,
         'form2': bound_form2,
         })

    def post(self, request, pk):
        obj1 = self.model1.objects.get(pk=pk)
        obj2 = self.model2.objects.get(user=obj1)
        bound_form1 = self.model_form1(request.POST, instance=obj1)
        bound_form2 = self.model_form2(request.POST, instance=obj2)

        if bound_form1.is_valid() and bound_form2.is_valid():
            new_obj1 = bound_form1.save()
            new_obj2 = bound_form2.save()
            return redirect(new_obj2.get_absolute_url())
        return render(request, self.template, context={'form1': bound_form1, 'form2': bound_form2})
