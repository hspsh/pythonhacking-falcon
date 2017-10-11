from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

TEMPLATE_FOLDER = (Path(__file__) / '..' / 'templates').resolve()

env = Environment(
    loader=FileSystemLoader(str(TEMPLATE_FOLDER)),
    autoescape=select_autoescape(['html'])
)


def render_template(name, context=None):
    if not context:
        context = {}

    template = env.get_template(name)
    rendered_template = template.render(context)

    return rendered_template
