import pytest
import os
from unittest.mock import patch
from sparc_cli.env import validate_environment, BEDROCK_REQUIRED_VARS

def test_validate_environment():
    """Test environment validation."""
    class Args:
        provider = "anthropic"
        expert_provider = "openai"
    
    with patch.dict('os.environ', {
        'ANTHROPIC_API_KEY': 'test-key',
        'OPENAI_API_KEY': 'test-key'
    }):
        expert_enabled, missing = validate_environment(Args())
        assert isinstance(expert_enabled, bool)
        assert isinstance(missing, list)
        assert len(missing) == 0

def test_validate_environment_missing_keys():
    """Test environment validation with missing keys."""
    class Args:
        provider = "anthropic"
        expert_provider = "openai"
    
    with patch.dict('os.environ', {}, clear=True):
        with pytest.raises(SystemExit):
            validate_environment(Args())

def test_validate_environment_openai_compatible():
    """Test environment validation for openai-compatible provider."""
    class Args:
        provider = "openai-compatible"
        expert_provider = "openai"
    
    with patch.dict('os.environ', {
        'OPENAI_API_KEY': 'test-key',
        'OPENAI_API_BASE': 'test-url',
        'EXPERT_OPENAI_API_KEY': 'test-key'
    }):
        expert_enabled, missing = validate_environment(Args())
        assert isinstance(expert_enabled, bool)
        assert isinstance(missing, list)
        assert len(missing) == 0

def test_validate_environment_expert_fallback():
    """Test expert provider fallback to base keys."""
    class Args:
        provider = "anthropic"
        expert_provider = "anthropic"
    
    with patch.dict('os.environ', {
        'ANTHROPIC_API_KEY': 'test-key'
    }):
        expert_enabled, missing = validate_environment(Args())
        assert isinstance(expert_enabled, bool)
        assert isinstance(missing, list)
        assert len(missing) == 0

def test_validate_environment_bedrock():
    """Test environment validation for Bedrock provider."""
    class Args:
        provider = "bedrock"
        expert_provider = "openai"
    
    with patch.dict('os.environ', {
        'BEDROCK_AWS_ACCESS_KEY_ID': 'test-key',
        'BEDROCK_AWS_SECRET_ACCESS_KEY': 'test-secret',
        'BEDROCK_AWS_REGION': 'us-west-2',
        'EXPERT_OPENAI_API_KEY': 'test-key'
    }):
        expert_enabled, missing = validate_environment(Args())
        assert isinstance(expert_enabled, bool)
        assert len(missing) == 0

def test_validate_environment_bedrock_missing_vars():
    """Test environment validation for Bedrock with missing variables."""
    class Args:
        provider = "bedrock"
        expert_provider = "openai"
    
    with patch.dict('os.environ', {}, clear=True):
        with pytest.raises(SystemExit):
            validate_environment(Args())

def test_validate_environment_bedrock_partial_vars():
    """Test environment validation for Bedrock with partial variables."""
    class Args:
        provider = "bedrock"
        expert_provider = "openai"
    
    with patch.dict('os.environ', {
        'BEDROCK_AWS_ACCESS_KEY_ID': 'test-key',
        # Missing SECRET_ACCESS_KEY and REGION
    }):
        with pytest.raises(SystemExit):
            validate_environment(Args())
