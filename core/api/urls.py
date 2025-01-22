from django.urls import include, path
from django.urls.resolvers import URLResolver

urlpatterns: list[URLResolver] = [
    path("auth/",include(("core.authentication.urls", "authentication"), namespace="authentication")),
    path("departments/",include(("core.departments.urls", "departmetns"), namespace="departments")),
    # path("users/", include(("core.users.urls", "users"), namespace="users")),
    path("ledgers/", include(("core.ledgers.urls", "ledgers"), namespace="ledgers")),
]
