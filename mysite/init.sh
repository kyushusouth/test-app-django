#!/bin/zsh


/Users/minami/dev/python/test-app-django/.venv/bin/python /Users/minami/dev/python/test-app-django/mysite/delete_all_migrations.py
/Users/minami/dev/python/test-app-django/.venv/bin/python /Users/minami/dev/python/test-app-django/mysite/manage.py makemigrations
/Users/minami/dev/python/test-app-django/.venv/bin/python /Users/minami/dev/python/test-app-django/mysite/manage.py migrate

# sample_meta_data.pyはなぜかバグる
/Users/minami/dev/python/test-app-django/.venv/bin/python /Users/minami/dev/python/test-app-django/mysite/main_app/fixtures/intelligibility_items.py
/Users/minami/dev/python/test-app-django/.venv/bin/python /Users/minami/dev/python/test-app-django/mysite/main_app/fixtures/naturalness_items.py
# /Users/minami/dev/python/test-app-django/.venv/bin/python /Users/minami/dev/python/test-app-django/mysite/main_app/fixtures/respondents.py
# /Users/minami/dev/python/test-app-django/.venv/bin/python /Users/minami/dev/python/test-app-django/mysite/main_app/fixtures/sample_meta_data.py
/Users/minami/dev/python/test-app-django/.venv/bin/python /Users/minami/dev/python/test-app-django/mysite/main_app/fixtures/sex.py

/Users/minami/dev/python/test-app-django/.venv/bin/python /Users/minami/dev/python/test-app-django/mysite/manage.py loaddata intelligibility_items
/Users/minami/dev/python/test-app-django/.venv/bin/python /Users/minami/dev/python/test-app-django/mysite/manage.py loaddata naturalness_items
# /Users/minami/dev/python/test-app-django/.venv/bin/python /Users/minami/dev/python/test-app-django/mysite/manage.py loaddata respondents
/Users/minami/dev/python/test-app-django/.venv/bin/python /Users/minami/dev/python/test-app-django/mysite/manage.py loaddata sample_meta_data
/Users/minami/dev/python/test-app-django/.venv/bin/python /Users/minami/dev/python/test-app-django/mysite/manage.py loaddata sex
