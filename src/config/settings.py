import os

# Path to apiKey and result file
API_KEY_PATH = os.path.join(os.path.dirname(__file__), "apiKey.txt")
RESULT_FILE_PATH = "result.txt"


# Scraper settings
DEFAULT_SCRAPER_MODEL = "openai/gpt-4o-mini"
SUPPORTED_SCRAPER_MODELS = ["gpt-4o-mini", "gpt-4o", "gtp-3.5-turbo"]

# Prompt settings
PROMPT_SUFFIX = "Please provide the data as flat JSON objects without nesting under any keys or names."
PROMPT_PREFIX = "Base on search results: "
