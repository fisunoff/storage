from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin


class OnlyCreatorMixin(UserPassesTestMixin):
    def test_func(self):

        if self.request.user.profile.id == self.model.objects.get(pk=int(self.kwargs['pk'])).creator_id or \
                self.request.user.is_superuser or self.request.user.is_staff:
            return True
        return False


class OnlyParentCreatorMixin(UserPassesTestMixin):
    def test_func(self):
        parent_model = self.model.parent_class()
        if parent_model.objects.get(pk=self.kwargs['from']).is_parent_creator(self.request.user.profile.id) or \
                self.request.user.is_superuser or self.request.user.is_staff:
            return True
        return False
