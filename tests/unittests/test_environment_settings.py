import pytest
from environment_settings import ImproperylConfigured, EnvironmentSettings
from .testconf import settings


class TestSettings:
    def test_context_access(self):
        with settings.environment('unittest'):
            assert settings.GREETING == 'Hello!'

    def test_no_context_access(self):
        with pytest.raises(ImproperylConfigured):
            settings.GREETING

    def test_active(self):
        assert settings.active == False
        with settings.environment('unittest'):
            assert settings.active == True

    def test_no_lowercase_settings_access(self):
        with settings.environment('unittest'), pytest.raises(ImproperylConfigured):
            settings.greeting


class TestEnvironmentSettings:
    def test_import(self):
        instance = EnvironmentSettings(settings_module='unittest', package='tests.unittests.testconf')
        assert instance.GREETING == 'Hello!'