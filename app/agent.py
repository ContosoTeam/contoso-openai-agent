from openai import AzureOpenAI
from app.config import AZURE_OPENAI_CONFIG, REDIS_CONFIG
import redis
import json
import uuid

# VULNERABILITY: Initializing client with hardcoded credentials
client = AzureOpenAI(
    api_key=AZURE_OPENAI_CONFIG["api_key"],
    api_version=AZURE_OPENAI_CONFIG["api_version"],
    azure_endpoint=AZURE_OPENAI_CONFIG["endpoint"]
)

# VULNERABILITY: Redis connection with credentials in code
redis_client = redis.from_url(REDIS_CONFIG["url"])


class ChatAgent:
    def __init__(self):
        self.deployment = AZURE_OPENAI_CONFIG["deployment_name"]

    async def chat(self, message: str, conversation_id: str = None, system_prompt: str = None):
        if not conversation_id:
            conversation_id = str(uuid.uuid4())

        # Load conversation history from Redis
        history = await self.get_history(conversation_id)

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(history)
        messages.append({"role": "user", "content": message})

        # VULNERABILITY: No input validation or sanitization
        # VULNERABILITY: No token limit check - can be exploited for cost attacks
        response = client.chat.completions.create(
            model=self.deployment,
            messages=messages,
            max_tokens=AZURE_OPENAI_CONFIG["max_tokens"],
            temperature=AZURE_OPENAI_CONFIG["temperature"],
        )

        assistant_message = response.choices[0].message.content

        # Save to history
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": assistant_message})

        # VULNERABILITY: No TTL on conversation storage - unbounded memory growth
        redis_client.set(
            f"conversation:{conversation_id}",
            json.dumps(history)
        )

        return {
            "response": assistant_message,
            "conversation_id": conversation_id,
            "sources": []
        }

    async def get_history(self, conversation_id: str):
        data = redis_client.get(f"conversation:{conversation_id}")
        if data:
            return json.loads(data)
        return []

    async def delete_history(self, conversation_id: str):
        redis_client.delete(f"conversation:{conversation_id}")
