from enum import Enum
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppEnvTypes(str, Enum):
    production = "production"
    development = "development"
    test = "test"

class AppSettings(BaseSettings):
    sender_tenant_id: str = ""
    sender_client_id: str = ""
    sender_client_secret: str = ""
    sender_user_email: str = ""

    email_subject: str = ""
    email_body: str = ""
    email_recipients: str = ""

    app_env: AppEnvTypes = AppEnvTypes.development

    model_config = SettingsConfigDict(
        env_file=".env",
    )

class DevAppSettings(AppSettings):
    app_env: AppEnvTypes = AppEnvTypes.development
    
    model_config = SettingsConfigDict(
        env_file=".env.development",
    )

class ProdAppSettings(AppSettings):
    app_env: AppEnvTypes = AppEnvTypes.production
    
    model_config = SettingsConfigDict(
        env_file=".env.production",
    )

class TestAppSettings(AppSettings):
    app_env: AppEnvTypes = AppEnvTypes.test
    
    model_config = SettingsConfigDict(
        env_file=".env.test",
    )

def get_app_settings():
    base_settings = AppSettings()
    
    if base_settings.app_env == AppEnvTypes.production:
        return ProdAppSettings()
    elif base_settings.app_env == AppEnvTypes.test:
        return TestAppSettings()
    return DevAppSettings()

settings = get_app_settings()
