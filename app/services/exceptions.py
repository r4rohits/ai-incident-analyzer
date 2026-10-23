
class AIConfigurationError(Exception):
    """AI provider configuration is missing or invalid."""


class AIProviderError(Exception):
    """The AI provider could not complete the request."""


class AIResponseError(Exception):
    """The AI response was missing or unusable."""
