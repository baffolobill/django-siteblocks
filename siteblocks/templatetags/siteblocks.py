from django import template
from django.template.base import FilterExpression

from ..siteblocksapp import SiteBlocks

register = template.Library()

# Utility methods are implemented in SiteBlocks class
siteblocks = SiteBlocks()


@register.simple_tag(takes_context=True)
def siteblock(context, block_alias):
    """Two notation types are acceptable:

        1. Two arguments:
           {% siteblock "myblock" %}
           Used to render "myblock" site block.

        2. Four arguments:
           {% siteblock "myblock" as myvar %}
           Used to put "myblock" site block into "myvar" template variable.

    """

    if isinstance(block_alias, FilterExpression):
        block_alias = block_alias.resolve(context)

    contents = siteblocks.get(block_alias, context)

    django_engine = template.engines['django']

    # Dirty hack to convert RequestContext to initial context, passed in a View.
    # This is necessary, because `Template.render(...)` requires that
    # `context` to be a dict. It don't check if `context` is already a RequestContext,
    # just always converts the dict to RequestContext.
    initial_context = context.dicts[3]

    contents = django_engine.from_string(contents)\
                            .render(initial_context, context.request)
    return contents
