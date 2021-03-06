from django import template
from django.conf import settings

register = template.Library()

SCRIPT_TAG = '<script src="%sjs/bootstrap-%s.js" type="text/javascript"></script>'

class BootstrapJSNode(template.Node):

    def __init__(self, args):
        self.args = set(args)

    def render_all_scripts(self):
        results = [
            SCRIPT_TAG % (settings.STATIC_URL, 'alert'),
            SCRIPT_TAG % (settings.STATIC_URL, 'button'),
            SCRIPT_TAG % (settings.STATIC_URL, 'carousel'),
            SCRIPT_TAG % (settings.STATIC_URL, 'collapse'),
            SCRIPT_TAG % (settings.STATIC_URL, 'dropdown'),
            SCRIPT_TAG % (settings.STATIC_URL, 'modal'),
            SCRIPT_TAG % (settings.STATIC_URL, 'popover'),
            SCRIPT_TAG % (settings.STATIC_URL, 'scrollspy'),
            SCRIPT_TAG % (settings.STATIC_URL, 'tab'),
            SCRIPT_TAG % (settings.STATIC_URL, 'tooltip'),
            SCRIPT_TAG % (settings.STATIC_URL, 'transition'),
            SCRIPT_TAG % (settings.STATIC_URL, 'typeahead')
        ]
        return '\n'.join(results)

    def render(self, context):
        if 'all' in self.args:
            return self.render_all_scripts()
        else:
            # popover requires twipsy
            if 'popover' in self.args:
                self.args.add('twipsy')
            tags = [SCRIPT_TAG % (settings.STATIC_URL,tag) for tag in self.args]
            return '\n'.join(tags)


@register.tag(name='bootstrap_js')
def do_bootstrap_js(parser, token):
    return BootstrapJSNode(token.split_contents()[1:])


@register.simple_tag
def bootstrap_less():
    if settings.DEVELOPMENT:
        LESS_TAG = '<link rel="stylesheet/less" type="text/css" href="%sless/%s">'

        output = [LESS_TAG % (settings.STATIC_URL, "bootstrap.less"),
                  '<script src="%sjs/less-1.3.0.min.js" type="text/javascript"></script>' % settings.STATIC_URL,
                  ]
        output = '\n'.join(output)

    else:
        output = '<link charset="utf-8" rel="stylesheet" type="text/css" href="%scss/styl.css">' % (settings.STATIC_URL)

    return output

