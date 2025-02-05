import pytest
from unittest.mock import Mock, patch
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_aws import ChatBedrockConverse
from sparc_cli.env import validate_environment
from sparc_cli.llm import initialize_llm, initialize_expert_llm, map_anthropic_to_bedrock_model

def test_initialize_llm_openai():
    """Test OpenAI LLM initialization."""
    with patch('sparc_cli.llm.ChatOpenAI') as mock:
        mock.return_value = Mock(spec=ChatOpenAI)
        try:
            model = initialize_llm('openai', 'gpt-4')
            assert isinstance(model, Mock)
            mock.assert_called_once()
        except Exception as e:
            pytest.fail(f"Failed to initialize OpenAI LLM: {e}")

def test_initialize_llm_anthropic():
    """Test Anthropic LLM initialization."""
    with patch('sparc_cli.llm.ChatAnthropic') as mock:
        mock.return_value = Mock(spec=ChatAnthropic)
        try:
            model = initialize_llm('anthropic', 'claude-2')
            assert isinstance(model, Mock)
            mock.assert_called_once()
        except Exception as e:
            pytest.fail(f"Failed to initialize Anthropic LLM: {e}")

def test_map_anthropic_to_bedrock_model():
    """Test Anthropic model name mapping for Bedrock."""
    # Test sonnet model mapping
    sonnet_name = "claude-3-sonnet-20240229"
    sonnet_bedrock = map_anthropic_to_bedrock_model(sonnet_name)
    assert sonnet_bedrock == "anthropic.claude-3-5-sonnet-20241022-v2:0"

    # Test haiku model mapping
    haiku_name = "claude-3-haiku-20240229"
    haiku_bedrock = map_anthropic_to_bedrock_model(haiku_name)
    assert haiku_bedrock == "anthropic.claude-3-5-haiku-20241022-v1:0"

    # Test default fallback
    other_name = "claude-3-other-20240229"
    other_bedrock = map_anthropic_to_bedrock_model(other_name)
    assert other_bedrock == "anthropic.claude-3-5-sonnet-20241022-v2:0"

def test_initialize_llm_bedrock():
    """Test Bedrock LLM initialization."""
    with patch('sparc_cli.llm.ChatBedrockConverse') as mock:
        mock.return_value = Mock(spec=ChatBedrockConverse)
        with patch.dict('os.environ', {
            'BEDROCK_AWS_REGION': 'us-west-2',
            'BEDROCK_AWS_ACCESS_KEY_ID': 'test-key',
            'BEDROCK_AWS_SECRET_ACCESS_KEY': 'test-secret'
        }):
            model = initialize_llm('bedrock', 'claude-3-sonnet-20240229')
            assert isinstance(model, Mock)
            mock.assert_called_once_with(
                model="anthropic.claude-3-5-sonnet-20241022-v2:0",
                region_name="us-west-2",
                credentials={
                    "accessKeyId": "test-key",
                    "secretAccessKey": "test-secret"
                }
            )

def test_initialize_expert_llm_bedrock():
    """Test Bedrock expert LLM initialization."""
    with patch('sparc_cli.llm.ChatBedrockConverse') as mock:
        mock.return_value = Mock(spec=ChatBedrockConverse)
        with patch.dict('os.environ', {
            'BEDROCK_AWS_REGION': 'us-west-2',
            'BEDROCK_AWS_ACCESS_KEY_ID': 'test-key',
            'BEDROCK_AWS_SECRET_ACCESS_KEY': 'test-secret'
        }):
            model = initialize_expert_llm('bedrock', 'claude-3-sonnet-20240229')
            assert isinstance(model, Mock)
            mock.assert_called_once_with(
                model="anthropic.claude-3-5-sonnet-20241022-v2:0",
                region_name="us-west-2",
                credentials={
                    "accessKeyId": "test-key",
                    "secretAccessKey": "test-secret"
                }
            )

def test_initialize_llm_invalid_provider():
    """Test invalid provider handling."""
    with pytest.raises(ValueError):
        initialize_llm('invalid', 'model')

def test_initialize_llm_case_insensitive():
    """Test case-insensitive provider names."""
    with patch('sparc_cli.llm.ChatOpenAI'):
        with pytest.raises(ValueError):
            initialize_llm('INVALID', 'model')

def test_initialize_expert_llm():
    """Test expert LLM initialization."""
    with patch('sparc_cli.llm.ChatOpenAI') as mock:
        mock.return_value = Mock(spec=ChatOpenAI)
        try:
            model = initialize_expert_llm('openai', 'gpt-4')
            assert isinstance(model, Mock)
            mock.assert_called_once()
        except Exception as e:
            pytest.fail(f"Failed to initialize expert LLM: {e}")

def test_environment_variables():
    """Test environment variable precedence and fallback."""
    from sparc_cli.env import validate_environment
    from dataclasses import dataclass

    @dataclass
    class Args:
        provider: str
        expert_provider: str

    args = Args(provider='anthropic', expert_provider='openai')
    
    with patch.dict('os.environ', {
        'ANTHROPIC_API_KEY': 'test-key',
        'OPENAI_API_KEY': 'test-key'
    }):
        expert_enabled, missing = validate_environment(args)
        assert isinstance(expert_enabled, bool)
        assert isinstance(missing, list)
        assert len(missing) == 0
