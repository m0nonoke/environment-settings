import pickle
import pytest
from environment_settings import ImproperlyConfigured, EnvironmentSettings
from .testconf import settings


class TestSettings:
    def test_context_access(self):
        with settings.environment('unittest'):
            assert settings.GREETING == 'Hello!'

    def test_no_context_access(self):
        with pytest.raises(ImproperlyConfigured):
            settings.GREETING

    def test_active(self):
        assert settings.active == False
        with settings.environment('unittest'):
            assert settings.active == True

    def test_no_lowercase_settings_access(self):
        with settings.environment('unittest'), pytest.raises(ImproperlyConfigured):
            settings.greeting


class TestEnvironmentSettings:
    def test_import(self):
        instance = EnvironmentSettings(settings_module='unittest', package='tests.unittests.testconf')
        assert instance.GREETING == 'Hello!'


class TestPickle:
    def test_pickle(self):
        instance = EnvironmentSettings(settings_module='unittest', package='tests.unittests.testconf')
        data = pickle.dumps(obj=instance, protocol=pickle.HIGHEST_PROTOCOL)

        instance2 = pickle.loads(data=data)

        assert instance.GREETING == instance2.GREETING

