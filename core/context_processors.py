from accounts.models import Section, ROLE


def add_variable_to_context(request):
    sections = Section.objects.all()

    ctx = {
        "sections": sections,
        'roles': ROLE
    }

    return ctx
