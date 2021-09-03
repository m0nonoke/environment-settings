# Environment Settings
The `environment_settings` package allows applications to manage multiple runtime environment configurations
in a central location using settings stored as normal python modules. Inspired by the Django settings framework 
(see https://docs.djangoproject.com/en/3.2/topics/settings/), the settings are loaded dynamically using a 
context manager at the application entry point. Additionally, the environment_settings module provides a decorator
that can be used to load the correct settings for automated tests.

## Usage
The following guide shows a typical application structure with support for multiple environment configurations. 
The `conf` package contains configuration files for each environment.
```
my-app
|--my_app
|  |--conf
|  |  |--__init__.py
|  |  |--dev.py
|  |  |--uat.py
|  |  |--unittest.py
|  |  `--prod.py
|  |--app.py
|  `--lib.py
|--tests
|  `--unittests
|     `--test_lib.py
|--pyproject.toml
|--README.md
`--setup.py
```

### Settings package configuration
Add the following code to the packge `__init__.py` to mark it as "settings enabled"
```python
# my_app/conf/__init__.py
from environment_settings import Settings

settings = Settings(package=__name__)
```

### Settings file layout
Each settings file are implemented as normal python modules. Settings should be UPPERCASE as per the example below. Any
other python code will not be visible in the settings context.

```python
# my_app/conf/dev.py
GOOD_SETTING_EXAMPLE = 'I am visible'
bad_setting_example = 'I am not visible'
```

### Initialising the settings context at the application entry point
Before any setting can be used, the settings context needs to be activated. Failure to active the context
will result in an `ImproperlyConfigured` exception
```python
# my_app/app.py
from my_app.conf import settings

with settings.environment('dev'):
    print(settings.GOOD_SETTINGS_EXAMPLE)

# Out[0]: 
# I am visible

print(settings.GOOD_SETTINGS_EXAMPLE)

# Out[1]:
# Traceback (most recent call last):
# ...
# ImproperlyConfigured: Requested GOOD_SETTINGS_EXAMPLE, but settings are not configured. You must define the settings.environment(name)

```
### Using settings throughout the application
The centralised settings object can be imported anywhere throughout the application: 
```python
# my_app/lib.py
from my_app.conf import settings

def my_func():
    return settings.GOOD_SETTINGS_EXAMPLE
```

## Testing
`environment_settings` also provides a decorator that can be used to provide test specific settings in test cases:
```python
# my_app/conf/unittest.py
GOOD_SETTINGS_EXAMPLE = 'unittest example'

# tests/unittests/test_lib.py
from my_app.conf import settings
from my_app import lib

@settings.environment('unittest')
class TestLib:
    def test_lib(self):
        assert lib.my_func() == 'unittest example'
```