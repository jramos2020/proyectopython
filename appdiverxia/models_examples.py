from django.db import models


class Dashboards(models.Model):
    name = models.CharField(max_length=191)
    enabled = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'dashboards'


class Disks(models.Model):
    code = models.BigAutoField(primary_key=True)
    id = models.CharField(max_length=191)
    user_id = models.PositiveIntegerField()
    access_token = models.TextField()
    token_type = models.CharField(max_length=20)
    alias = models.CharField(max_length=191)
    driver = models.CharField(max_length=191)
    path = models.TextField()
    phash = models.CharField(max_length=20)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'disks'


class FailedJobs(models.Model):
    id = models.BigAutoField(primary_key=True)
    connection = models.TextField()
    queue = models.TextField()
    payload = models.TextField()
    exception = models.TextField()
    failed_at = models.DateTimeField()

    class Meta:
        db_table = 'failed_jobs'


class Jobs(models.Model):
    id = models.BigAutoField(primary_key=True)
    queue = models.CharField(max_length=191)
    payload = models.TextField()
    attempts = models.PositiveIntegerField()
    reserved_at = models.PositiveIntegerField(blank=True, null=True)
    available_at = models.PositiveIntegerField()
    created_at = models.PositiveIntegerField()

    class Meta:
        db_table = 'jobs'


class Media(models.Model):
    disk = models.CharField(max_length=32)
    directory = models.CharField(max_length=68)
    filename = models.CharField(max_length=121)
    extension = models.CharField(max_length=28)
    mime_type = models.CharField(max_length=128)
    aggregate_type = models.CharField(max_length=32)
    size = models.PositiveIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'media'
        unique_together = (('disk', 'directory', 'filename', 'extension', 'deleted_at'),)


class Mediables(models.Model):
    media = models.OneToOneField(Media, models.DO_NOTHING, primary_key=True)
    mediable_type = models.CharField(max_length=152)
    mediable_id = models.PositiveIntegerField()
    tag = models.CharField(max_length=68)
    order = models.PositiveIntegerField()

    class Meta:
        db_table = 'mediables'
        unique_together = (('media', 'mediable_type', 'mediable_id', 'tag'),)


class Migrations(models.Model):
    migration = models.CharField(max_length=191)
    batch = models.IntegerField()

    class Meta:
        db_table = 'migrations'


class ModuleHistories(models.Model):
    module_id = models.IntegerField()
    category = models.CharField(max_length=191)
    version = models.CharField(max_length=191)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'module_histories'


class Modules(models.Model):
    alias = models.CharField(max_length=191)
    enabled = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'modules'
        unique_together = (('alias', 'deleted_at'),)


class Notifications(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    type = models.CharField(max_length=191)
    notifiable_type = models.CharField(max_length=191)
    notifiable_id = models.PositiveBigIntegerField()
    data = models.TextField()
    read_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'notifications'


class OauthAccessTokens(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    user_id = models.PositiveBigIntegerField(blank=True, null=True)
    client_id = models.PositiveBigIntegerField()
    name = models.CharField(max_length=191, blank=True, null=True)
    scopes = models.TextField(blank=True, null=True)
    revoked = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'oauth_access_tokens'


class OauthAuthCodes(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    user_id = models.PositiveBigIntegerField()
    client_id = models.PositiveBigIntegerField()
    scopes = models.TextField(blank=True, null=True)
    revoked = models.IntegerField()
    expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'oauth_auth_codes'


class OauthClients(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.PositiveBigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=191)
    secret = models.CharField(max_length=100, blank=True, null=True)
    provider = models.CharField(max_length=191, blank=True, null=True)
    redirect = models.TextField()
    personal_access_client = models.IntegerField()
    password_client = models.IntegerField()
    revoked = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'oauth_clients'


class OauthPersonalAccessClients(models.Model):
    id = models.BigAutoField(primary_key=True)
    client_id = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'oauth_personal_access_clients'


class OauthRefreshTokens(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    access_token_id = models.CharField(max_length=100)
    revoked = models.IntegerField()
    expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'oauth_refresh_tokens'


class PasswordResets(models.Model):
    email = models.CharField(max_length=191)
    token = models.CharField(max_length=191)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'password_resets'


class Permissions(models.Model):
    name = models.CharField(unique=True, max_length=191)
    display_name = models.CharField(max_length=191)
    description = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'permissions'


class RolePermissions(models.Model):
    role = models.OneToOneField('Roles', models.DO_NOTHING, primary_key=True)
    permission = models.ForeignKey(Permissions, models.DO_NOTHING)

    class Meta:
        db_table = 'role_permissions'
        unique_together = (('role', 'permission'),)


class Roles(models.Model):
    name = models.CharField(unique=True, max_length=191)
    display_name = models.CharField(max_length=191)
    description = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'roles'


class Sessions(models.Model):
    id = models.CharField(unique=True, max_length=191)
    user_id = models.PositiveIntegerField(blank=True, null=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    payload = models.TextField()
    last_activity = models.IntegerField()

    class Meta:
        db_table = 'sessions'


class Settings(models.Model):
    key = models.CharField(unique=True, max_length=191)
    value = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'settings'


class Shortcuts(models.Model):
    id = models.BigAutoField(primary_key=True)
    host = models.CharField(max_length=191)
    path = models.TextField()
    shortcut = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'shortcuts'


class UserDashboards(models.Model):
    user_id = models.PositiveIntegerField(primary_key=True)
    dashboard_id = models.PositiveIntegerField()
    user_type = models.CharField(max_length=20)

    class Meta:
        db_table = 'user_dashboards'
        unique_together = (('user_id', 'dashboard_id', 'user_type'),)


class UserPermissions(models.Model):
    user_id = models.PositiveIntegerField(primary_key=True)
    permission = models.ForeignKey(Permissions, models.DO_NOTHING)
    user_type = models.CharField(max_length=191)

    class Meta:
        db_table = 'user_permissions'
        unique_together = (('user_id', 'permission', 'user_type'),)


class UserRoles(models.Model):
    user_id = models.PositiveIntegerField(primary_key=True)
    role = models.ForeignKey(Roles, models.DO_NOTHING)
    user_type = models.CharField(max_length=191)

    class Meta:
        db_table = 'user_roles'
        unique_together = (('user_id', 'role', 'user_type'),)


class Users(models.Model):
    name = models.CharField(max_length=191)
    username = models.CharField(max_length=191, blank=True, null=True)
    phone = models.CharField(max_length=191, blank=True, null=True)
    pwd = models.CharField(max_length=191)
    email = models.CharField(max_length=191)
    password = models.CharField(max_length=191)
    dni = models.CharField(max_length=191, blank=True, null=True)
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    last_logged_in_at = models.DateTimeField(blank=True, null=True)
    locale = models.CharField(max_length=191)
    landing_page = models.CharField(max_length=70, blank=True, null=True)
    enabled = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'users'
        unique_together = (('email', 'deleted_at'), ('pwd', 'deleted_at'),)


class Widgets(models.Model):
    dashboard_id = models.IntegerField()
    class_field = models.CharField(db_column='class',
                                   max_length=191)  # Field renamed because it was a Python reserved word.
    name = models.CharField(max_length=191)
    sort = models.IntegerField()
    settings = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'widgets'
