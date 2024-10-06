from enum import Enum


class Mode(Enum):
    URL = "Url"
    FIND_URL = "Find url"


class ChatModel(Enum):
    GTP4oMini = "gpt-4o-mini"
    GTP4o = "gpt-4o"
    GTP35Turbo = "gtp-3.5-turbo"
