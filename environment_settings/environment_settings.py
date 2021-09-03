import importlib
from functools import wraps


class ImproperylConfigured(Exception):
    """Improperly configured settings."""


class Settings:
    _wrapped = None
    _wrapped_counter = 0

    def __init__(self, package=None):
        self.package = package

    def __getattr__(self, name):
        if not self._wrapped:
            desc = f'settings {name}'
            raise ImproperylConfigured(
                f'Requested {desc}, but settings are not configured. You must define the settings.environment(name)'
            )

        if not name.isupper():
            raise ImproperylConfigured(f'Setting {name} should be uppercase')

        else:
            val = getattr(self._wrapped, name)
            return val

    def environment(self, name):
        self.name = name
        return self

    def _decorate_fn(self, fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            with self:
                return fn(*args, **kwargs)

        return wrapped

    def __call__(self, decorated):
        if isinstance(decorated, type):
            for attr in decorated.__dict__:
                if callable(getattr(decorated, attr)):
                    setattr(
                        decorated, attr, self._decorate_fn(getattr(decorated, attr))
                    )
            return decorated
        else:
            return self._decorate_fn(decorated)


    def __enter__(self):
        if not self._wrapped:
            self._wrapped = EnvironmentSettings(self.name, self.package)
            self._wrapped_counter += 1
            return self

        elif self._wrapped.settings_module == self.name:
            self._wrapped_counter += 1
            return self

        else:
            raise ImproperylConfigured(
                f'Requested settings {self.name}, but settings {self._wrapped.settings_module} are already configured.'
            )

    def __exit__(self, *exc):
        self._wrapped_counter -= 1
        if self._wrapped_counter == 0:
            self._wrapped = None
        return False

    @property
    def active(self):
        return bool(self._wrapped)


class EnvironmentSettings:
    def __init__(self, settings_module, package=None):
        self.settings_module = settings_module
        package = package or __name__
        mod = importlib.import_module(f'.{self.settings_module}', package=package)

        self._explicit_settings = set()
        for setting in dir(mod):
            if setting.isupper():
                settings_value = getattr(mod, setting)
                setattr(self, setting, settings_value)
                self._explicit_settings.add(setting)

    def is_overridden(self, settings):
        return settings in self._explicit_settings

    def __repr__(self):
        return f'<{self.__class__.__name__} "{self.settings_module}"'

    def __iter__(self):
        return (setting for setting in dir(self) if setting.isupper())

