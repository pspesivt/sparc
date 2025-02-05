import os
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_aws import ChatBedrockConverse
from langchain_core.language_models import BaseChatModel

def map_anthropic_to_bedrock_model(model_name: str) -> str:
    """Map Anthropic model names to their Bedrock equivalents.
    
    Args:
        model_name: The Anthropic model name (e.g., 'claude-3-5-sonnet-20241022')
        
    Returns:
        str: The corresponding Bedrock model name
    """
    # Map to Bedrock model IDs
    # Reference: https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids-arns.html
    if "sonnet" in model_name.lower():
        return "anthropic.claude-3-5-sonnet-20241022-v2:0"
    elif "haiku" in model_name.lower():
        return "anthropic.claude-3-5-haiku-20241022-v1:0"
    elif "opus" in model_name.lower():
        return "anthropic.claude-3-opus-20240229-v1:0"
    elif "claude-2" in model_name.lower():
        return "anthropic.claude-v2:1"
    elif "claude-instant" in model_name.lower():
        return "anthropic.claude-instant-v1"
    else:
        # Default to Claude 3 Sonnet if model type is unclear
        return "anthropic.claude-3-sonnet-20240229-v1:0"

def initialize_llm(provider: str, model_name: str) -> BaseChatModel:
    """Initialize a language model client based on the specified provider and model.

    Note: Environment variables must be validated before calling this function.
    Use validate_environment() to ensure all required variables are set.

    Args:
        provider: The LLM provider to use ('openai', 'anthropic', 'openrouter', 'openai-compatible')
        model_name: Name of the model to use

    Returns:
        BaseChatModel: Configured language model client

    Raises:
        ValueError: If the provider is not supported
    """

    if provider == "openai":
        print(f"Using openai model: {model_name}")
        return ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            model=model_name,
        )
    elif provider == "anthropic":
        return ChatAnthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            model_name=model_name,
        )
    elif provider == "openrouter":
        return ChatOpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
            model=model_name,
        )
    elif provider == "openai-compatible":
        return ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE"),
            model=model_name,
        )
    elif provider == "bedrock":
        # For Bedrock, if it's an Anthropic model, map it to the Bedrock format
        bedrock_model = map_anthropic_to_bedrock_model(model_name)
            
        return ChatBedrockConverse(
            model=bedrock_model,
            region_name=os.getenv("BEDROCK_AWS_REGION"),
            aws_access_key_id=os.getenv("BEDROCK_AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("BEDROCK_AWS_SECRET_ACCESS_KEY")
        )
    else:
        raise ValueError(f"Unsupported provider: {provider}")

def initialize_expert_llm(provider: str = "openai", model_name: str = "o1-preview") -> BaseChatModel:
    """Initialize an expert language model client based on the specified provider and model.

    Note: Environment variables must be validated before calling this function.
    Use validate_environment() to ensure all required variables are set.

    Args:
        provider: The LLM provider to use ('openai', 'anthropic', 'openrouter', 'openai-compatible').
                 Defaults to 'openai'.
        model_name: Name of the model to use. Defaults to 'o1-preview'.

    Returns:
        BaseChatModel: Configured expert language model client

    Raises:
        ValueError: If the provider is not supported
    """
    if provider == "openai":
        return ChatOpenAI(
            api_key=os.getenv("EXPERT_OPENAI_API_KEY"),
            model=model_name,
        )
    elif provider == "anthropic":
        return ChatAnthropic(
            api_key=os.getenv("EXPERT_ANTHROPIC_API_KEY"),
            model_name=model_name,
        )
    elif provider == "openrouter":
        return ChatOpenAI(
            api_key=os.getenv("EXPERT_OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
            model=model_name,
        )
    elif provider == "openai-compatible":
        return ChatOpenAI(
            api_key=os.getenv("EXPERT_OPENAI_API_KEY"),
            base_url=os.getenv("EXPERT_OPENAI_API_BASE"),
            model=model_name,
        )
    elif provider == "bedrock":
        # For Bedrock expert mode, use the same credentials as non-expert mode
        if "claude" in model_name.lower():
            bedrock_model = map_anthropic_to_bedrock_model(model_name)
        else:
            bedrock_model = model_name
            
        return ChatBedrockConverse(
            model=bedrock_model,
            region_name=os.getenv("BEDROCK_AWS_REGION"),
            aws_access_key_id=os.getenv("BEDROCK_AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("BEDROCK_AWS_SECRET_ACCESS_KEY")
        )
    else:
        raise ValueError(f"Unsupported provider: {provider}")
