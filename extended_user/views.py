from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django_tables2 import SingleTableView

from extended_user.models import Profile
from extended_user.tables import UserTable


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'


class UsersListView(SingleTableView):
    model = Profile
    table_class = UserTable
    template_name = 'profiles/list.html'


class UserDetailView(DetailView):
    model = Profile
    template_name = 'profiles/detail.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user = User.objects.get(pk=self.request.user.profile.id)
            profile_user = User.objects.get(pk=context['object'].id)
            context['is_profile_staff'] = profile_user.groups.filter(name__in=['worker', ]).exists()
            context['is_staff'] = user.groups.filter(name__in=['worker', ]).exists()
        else:
            context['is_profile_staff'] = False
            context['is_staff'] = False

        return context


class ProfileDetailView(UserDetailView):
    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        user = User.objects.get(pk=self.request.user.profile.id)
        context['is_profile_staff'] = user.groups.filter(name__in=['worker', ]).exists()
        context['is_staff'] = user.groups.filter(name__in=['worker', ]).exists()

        return context

    def get_object(self, queryset=None):
        return self.request.user.profile


class UserUpdateView(UpdateView):
    model = Profile
    template_name = 'profiles/update.html'
    context_object_name = 'mentor'
    fields = ('surname', 'name', 'patronymic', 'bio', 'photo')

    def get_success_url(self):
        self.object.time_edit = timezone.now()
        self.object.save()
        return reverse_lazy('profile-detail', kwargs={'pk': self.object.id})
