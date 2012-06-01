from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.views.generic.base import View

from gargoyle import gargoyle


class SwitchActiveMixin(View):
    """
    Verify that the switch given in gargoyle_switch is active, otherwise return 
    a 404.
    """
    
    gargoyle_switch = None
    gargoyle_redirect_to = None
    
    def dispatch(self, request, *args, **kwargs):
        if not self.gargoyle_switch:
            raise ImproperlyConfigured(
                    'SwitchActiveMixin requires gargoyle_switch setting')
        if not gargoyle.is_active(self.gargoyle_switch, request):
            if not self.gargoyle_redirect_to:
                raise Http404('Switch \'%s\' is not active' % self.gargoyle_switch)
            elif self.gargoyle_redirect_to.startswith('/'):
                return HttpResponseRedirect(self.gargoyle_redirect_to)
            else:
                return HttpResponseRedirect(reverse(self.gargoyle_redirect_to))
        return super(SwitchActiveMixin, self).dispatch(request, *args, **kwargs)
