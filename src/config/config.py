import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_URL: str = os.getenv("BASE_URL", "https://the-internet.herokuapp.com")
    BROWSER: str = os.getenv("BROWSER", "chromium")  # chromium | firefox | webkit
    HEADLESS: bool = os.getenv("HEADLESS", "false").lower() == "true"
    SLOW_MO: int = int(os.getenv("SLOW_MO", "0"))
    TIMEOUT: int = int(os.getenv("TIMEOUT", "30000"))  # milliseconds
    SCREENSHOT_ON_FAIL: bool = os.getenv("SCREENSHOT_ON_FAIL", "true").lower() == "true"
    TRACE_ON_FAIL: bool = os.getenv("TRACE_ON_FAIL", "true").lower() == "true"

    LOGIN_USERNAME: str = os.getenv("LOGIN_USERNAME", "tomsmith")
    LOGIN_PASSWORD: str = os.getenv("LOGIN_PASSWORD", "SuperSecretPassword!")
