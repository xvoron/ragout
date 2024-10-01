from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal

import openai


@dataclass
class ChatMessage:
    role: Literal["user", "assistant"]
    timestamp: datetime
    text: str


@dataclass
class Conversation:
    messages: list[ChatMessage] = field(default_factory=list)

    async def respond(self, client: openai.AsyncOpenAI) -> ChatMessage:

        # Make sure the last message was by the user
        if not self.messages or self.messages[-1].role != "user":
            raise ValueError("The most recent message must be by the user")

        # Convert all messages to the format needed by the API
        api_messages: list[Any] = [
            {
                "role": "system",
                "content": "You are a helpful assistant. Format your response in markdown, for example by using **bold**, and _italic_ amongst others.",
            }
        ] + [
            {
                "role": message.role,
                "content": message.text,
            }
            for message in self.messages
        ]

        # Generate a response
        api_response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=api_messages,
            max_tokens=500,
        )

        assert isinstance(api_response.choices[0].message.content, str)

        response = ChatMessage(
            role="assistant",
            timestamp=datetime.now(tz=timezone.utc),
            text=api_response.choices[0].message.content,
        )

        self.messages.append(response)

        return response
