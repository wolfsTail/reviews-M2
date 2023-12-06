from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin



class AuthorRequiredMixin(AccessMixin):
    """
    разграничение доступа при изменении опубликованного поста
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.is_authenticated:
            if (request.user != self.get_object().author) or not request.user.is_staff:
                messages.info(request, 'Изменение статьи недоступно!')
                return redirect('home')
        return super().dispatch(request, *args, **kwargs)