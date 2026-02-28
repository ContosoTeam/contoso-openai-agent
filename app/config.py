"""
Azure OpenAI Configuration
"""

# VULNERABILITY: Hardcoded Azure OpenAI credentials
AZURE_OPENAI_CONFIG = {
    "api_key": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
    "endpoint": "https://contoso-openai-prod.openai.azure.com/",
    "deployment_name": "gpt-4-turbo",
    "api_version": "2024-02-01",
    "max_tokens": 4096,
    "temperature": 0.7,
}

# VULNERABILITY: Hardcoded Azure Cognitive Search credentials
AZURE_SEARCH_CONFIG = {
    "endpoint": "https://contoso-search-prod.search.windows.net",
    "api_key": "mR4nD0mS3aRcHk3y1234567890aBcDeF",
    "index_name": "contoso-documents",
}

# VULNERABILITY: Hardcoded Redis credentials
REDIS_CONFIG = {
    "url": "redis://:ContosoRedis!Pass2024@contoso-redis-prod.redis.cache.windows.net:6380/0",
    "ssl": True,
}

# VULNERABILITY: Weak CORS configuration
CORS_ORIGINS = ["*"]

# VULNERABILITY: No rate limiting configuration
RATE_LIMIT = None
