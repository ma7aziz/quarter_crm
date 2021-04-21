from accounts.models import Section, ROLE, User


def add_variable_to_context(request):
    sections = Section.objects.all()
    users = User.objects.all()

    ctx = {
        "sections": sections,
        'roles': ROLE,
        'users': users
    }

    return ctx
