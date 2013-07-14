from functools import wraps
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

def template(template_name=None):
    """Render the returned dict through a template, given by either the
    '__template__' key of the dict, or by the argument given to this decorator.
    Always uses RequestContext.
    """
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            retval = func(request, *args, **kwargs)

            # some views might still make their own response in some conditions
            if isinstance(retval, HttpResponse):
                return retval

            print retval
            _template_name = retval.get('__template__', template_name)
            if _template_name is None:
                raise UnidentifiedTemplateException()
            return render_to_response(_template_name, retval,
                    context_instance=RequestContext(request))
        return inner
    return decorator

class UnidentifiedTemplateException (Exception):
    def __init__(self):
        super(UnidentifiedTemplateException, self).__init__(
            "No template was supplied to the @template() decorator, and no "
            "template was given in the context dictionary."
        )
