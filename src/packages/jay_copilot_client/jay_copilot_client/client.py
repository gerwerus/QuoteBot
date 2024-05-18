from functools import cached_property
from urllib.parse import urljoin

import requests  # type: ignore
from pydantic import TypeAdapter

from .entities import (
    AppIdList,
    AppModel,
    Conversation,
    ConversationHistory,
    ConversationIdList,
    QuoteKeywordList,
)
from .settings import JayCopilotSettings


class JayCopilotClient:
    """
    More info about API:  https://help.jaycopilot.com/api
    """

    BASE_URL = "https://app.jaycopilot.com/api/appsAdapter/"

    def __init__(self, settings: JayCopilotSettings | None = None):
        self.settings = settings or JayCopilotSettings.initialize_from_environment()

    def get_apps(self) -> list[AppModel]:
        """
        Retrieves a list of AppModel objects representing the available apps.
        """
        response = requests.get(
            url=urljoin(self.BASE_URL, "apps"),
            headers=self.default_headers,
        )
        response.raise_for_status()

        return TypeAdapter(list[AppModel]).validate_python(response.json()["apps"])

    def get_conversations(self) -> list[Conversation]:
        """
        Retrieves a list of Conversation objects representing the available conversations.
        """
        response = requests.get(
            url=urljoin(self.BASE_URL, "conversations"),
            headers=self.default_headers,
        )
        response.raise_for_status()
        return TypeAdapter(list[Conversation]).validate_python(response.json()["conversations"])

    def create_conversation(self, conversation_name: str, *, app_id: AppIdList | None = None) -> Conversation:
        """
        Creates a new conversation with the given name and optional app ID.

        If no app ID is provided, the default GPT-4 app will be used.
        """
        app_id = app_id or AppIdList.GPT_4
        headers = self.default_headers
        headers["Content-Type"] = "application/json"

        response = requests.post(
            url=urljoin(self.BASE_URL, "conversations"),
            json={"name": conversation_name, "app": {"id": app_id.value}},
            headers=headers,
        )
        response.raise_for_status()
        return Conversation.model_validate(response.json())

    def send_message(self, message: str, *, conversation_id: ConversationIdList) -> ConversationHistory:
        """
        Sends a message to the given conversation.
        """
        response = requests.post(
            url=urljoin(self.BASE_URL, f"conversations/{conversation_id.value}/message"),
            json={"text": message},
            headers=self.default_headers,
        )
        response.raise_for_status()
        return ConversationHistory.model_validate(response.json())

    def get_quote_keywords(self, quote: str, keywords_amount: int = 1) -> QuoteKeywordList:
        """
        Retrieves a list of quote keywords.
        """
        conversation_history = self.send_message(
            f"Выдели {keywords_amount} ключевых слова из цитаты '{quote}'. Формат вывода: KeywordsRu: ... Затем переведи ключевые слова на английский. Формат вывода: KeywordsEn: ...",
            conversation_id=ConversationIdList.quotes_conversation_id,
        )
        text = conversation_history.content[0].text.split("\n")
        return QuoteKeywordList(
            ru=text[0].replace("KeywordsRu: ", "").split(", "),
            en=text[1].replace("KeywordsEn: ", "").split(", "),
        )

    @cached_property
    def default_headers(self) -> dict[str, str]:
        return {"X-API-KEY": self.settings.API_KEY}
