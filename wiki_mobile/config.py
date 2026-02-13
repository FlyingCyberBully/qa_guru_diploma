from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class LocalConfig(BaseSettings):
    """Configuration for local Appium (emulator or real device)."""

    model_config = SettingsConfigDict(
        env_file='.env.local',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    platform_name: str = 'Android'
    device_name: str = 'emulator-5554'
    app: str = ''
    app_wait_activity: str = 'org.wikipedia.*'
    remote_url: str = 'http://localhost:4723'
    timeout: float = 10.0


class BStackConfig(BaseSettings):
    """Configuration for BrowserStack remote execution."""

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    platform_name: str = 'Android'
    platform_version: str = Field(default='13.0', alias='PLATFORM_VERSION')
    device_name: str = Field(default='Google Pixel 7', alias='DEVICE_NAME')
    app_url: str = Field(default='', alias='BROWSERSTACK_APP_URL')
    bstack_user: str = Field(default='', alias='BROWSERSTACK_USERNAME')
    bstack_key: str = Field(default='', alias='BROWSERSTACK_ACCESS_KEY')
    timeout: float = 10.0

    @property
    def remote_url(self) -> str:
        return (
            f'https://{self.bstack_user}:{self.bstack_key}'
            f'@hub-cloud.browserstack.com/wd/hub'
        )

    def to_capabilities(self) -> dict:
        return {
            'platformName': self.platform_name,
            'platformVersion': self.platform_version,
            'deviceName': self.device_name,
            'app': self.app_url,
            'bstack:options': {
                'projectName': 'Wikipedia Mobile Tests',
                'buildName': 'diploma-mobile-build',
                'sessionName': 'Wikipedia Test',
            },
        }


def get_mobile_config(context: str = 'bstack'):
    if context == 'local':
        return LocalConfig()
    return BStackConfig()
