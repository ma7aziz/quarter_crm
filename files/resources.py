from import_export import resources, fields
from accounts.models import User, Section
from import_export.widgets import ManyToManyWidget


class UsersResource(resources.ModelResource):
    role = fields.Field(
        attribute="get_role_display", column_name="role"
    )

    class Meta:
        model = User
        fields = ('id', 'name', 'phone', 'email', 'role', 'last_login',
                  'completed_tasks', 'submitted_orders', 'username')
        export_order = ('id', 'username',  'name', 'phone', 'email', 'role', 'last_login',
                        'completed_tasks', 'submitted_orders')


class CurrentTasksResource(resources.ModelResource):
    class Meta:
        pass
