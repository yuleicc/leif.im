import mistune
from django import template
from pygments import highlight
from django.utils.safestring import mark_safe
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from django.template.defaultfilters import stringfilter


register = template.Library()


class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                   mistune.escape(code)
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()
        return highlight(code, lexer, formatter)


renderer = HighlightRenderer()
markdown = mistune.Markdown(renderer=renderer)


@register.filter(is_safe=True)
@stringfilter
def md1(value):
    markdown = mistune.Markdown(renderer=renderer)
    return mark_safe(markdown(value))
