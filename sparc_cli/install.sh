#!/bin/bash

echo "Welcome to SPARC CLI Installation"
echo "================================"
echo

# Function to prompt for a secret
prompt_secret() {
    local secret_name=$1
    local required=$2
    local current_value=${!secret_name}
    
    local prompt_text
    if [ -n "$current_value" ]; then
        prompt_text="Enter value for ${secret_name} (current: ${current_value}) or press Enter to keep: "
    else
        prompt_text="Enter value for ${secret_name} (press Enter to skip): "
    fi
    
    # Print prompt and read input
    printf "%s" "$prompt_text"
    read input_value
    
    # Return the appropriate value
    if [ -n "$input_value" ]; then
        # Return new value if provided
        printf "%s" "$input_value"
    elif [ -n "$current_value" ]; then
        # Return existing value if available
        printf "%s" "$current_value"
    elif [ "$required" = "true" ]; then
        # Error if required but no value available
        printf "Error: %s is required\n" "$secret_name" >&2
        return 1
    else
        # Return empty string if optional
        printf ""
    fi
    return 0
}

# Function to setup environment variables
setup_environment() {
    echo "Setting up API keys..."
    echo "----------------------"
    echo "Press Enter to keep existing values or input new ones."
    echo "For required keys, you must provide a value."
    echo
    
    # Create exports file
    local exports_file="$HOME/.sparc_exports"
    
    echo "Setting up LLM Provider Keys..."
    echo "-----------------------------"
    echo "Press Enter to skip any provider you don't plan to use."
    echo
    
    # Optional keys
    echo "Anthropic Configuration:"
    ANTHROPIC_API_KEY=$(prompt_secret "ANTHROPIC_API_KEY" "false")
    
    echo
    echo "OpenAI Configuration:"
    OPENAI_API_KEY=$(prompt_secret "OPENAI_API_KEY" "false")
    
    echo
    echo "OpenRouter Configuration:"
    OPENROUTER_KEY=$(prompt_secret "OPENROUTER_KEY" "false")
    
    echo
    echo "AWS Bedrock Configuration:"
    echo "------------------------"
    echo "If you plan to use AWS Bedrock, please provide your AWS credentials."
    echo "Press Enter to skip if not using Bedrock."
    echo
    echo "AWS Region (e.g., us-west-2):"
    BEDROCK_AWS_REGION=$(prompt_secret "BEDROCK_AWS_REGION" "false")
    
    if [ -n "$BEDROCK_AWS_REGION" ]; then
        echo
        echo "AWS Access Key ID:"
        BEDROCK_AWS_ACCESS_KEY_ID=$(prompt_secret "BEDROCK_AWS_ACCESS_KEY_ID" "false")
        
        echo
        echo "AWS Secret Access Key:"
        BEDROCK_AWS_SECRET_ACCESS_KEY=$(prompt_secret "BEDROCK_AWS_SECRET_ACCESS_KEY" "false")
    fi
    
    echo
    echo "Other Configuration:"
    echo "------------------"
    ENCRYPTION_KEY=$(prompt_secret "ENCRYPTION_KEY" "false")
    GEMINI_API_KEY=$(prompt_secret "GEMINI_API_KEY" "false")
    VERTEXAI_PROJECT=$(prompt_secret "VERTEXAI_PROJECT" "false")
    VERTEXAI_LOCATION=$(prompt_secret "VERTEXAI_LOCATION" "false")
    
    # Create exports file with only non-empty values
    {
        echo "# SPARC CLI Environment Variables"
        echo
        
        # LLM Provider Keys section
        local has_llm_keys=false
        if [ -n "$ANTHROPIC_API_KEY" ] || [ -n "$OPENAI_API_KEY" ] || [ -n "$OPENROUTER_KEY" ]; then
            echo "# LLM Provider Keys"
            [ -n "$ANTHROPIC_API_KEY" ] && echo "export ANTHROPIC_API_KEY='$ANTHROPIC_API_KEY'"
            [ -n "$OPENAI_API_KEY" ] && echo "export OPENAI_API_KEY='$OPENAI_API_KEY'"
            [ -n "$OPENROUTER_KEY" ] && echo "export OPENROUTER_KEY='$OPENROUTER_KEY'"
            echo
            has_llm_keys=true
        fi
        
        # AWS Bedrock Configuration section
        local has_bedrock=false
        if [ -n "$BEDROCK_AWS_ACCESS_KEY_ID" ] || [ -n "$BEDROCK_AWS_SECRET_ACCESS_KEY" ] || [ -n "$BEDROCK_AWS_REGION" ]; then
            echo "# AWS Bedrock Configuration"
            [ -n "$BEDROCK_AWS_ACCESS_KEY_ID" ] && echo "export BEDROCK_AWS_ACCESS_KEY_ID='$BEDROCK_AWS_ACCESS_KEY_ID'"
            [ -n "$BEDROCK_AWS_SECRET_ACCESS_KEY" ] && echo "export BEDROCK_AWS_SECRET_ACCESS_KEY='$BEDROCK_AWS_SECRET_ACCESS_KEY'"
            [ -n "$BEDROCK_AWS_REGION" ] && echo "export BEDROCK_AWS_REGION='$BEDROCK_AWS_REGION'"
            echo
            has_bedrock=true
        fi
        
        # Other Configuration section
        local has_other=false
        if [ -n "$ENCRYPTION_KEY" ] || [ -n "$GEMINI_API_KEY" ] || [ -n "$VERTEXAI_PROJECT" ] || [ -n "$VERTEXAI_LOCATION" ]; then
            echo "# Other Configuration"
            [ -n "$ENCRYPTION_KEY" ] && echo "export ENCRYPTION_KEY='$ENCRYPTION_KEY'"
            [ -n "$GEMINI_API_KEY" ] && echo "export GEMINI_API_KEY='$GEMINI_API_KEY'"
            [ -n "$VERTEXAI_PROJECT" ] && echo "export VERTEXAI_PROJECT='$VERTEXAI_PROJECT'"
            [ -n "$VERTEXAI_LOCATION" ] && echo "export VERTEXAI_LOCATION='$VERTEXAI_LOCATION'"
            has_other=true
        fi
        
        # Add a note if no values were provided
        if [ "$has_llm_keys" = false ] && [ "$has_bedrock" = false ] && [ "$has_other" = false ]; then
            echo "# No configuration values provided"
            echo "# Run ./install.sh again to configure providers"
        fi
    } > "$exports_file"
    
    # Make exports file executable
    chmod +x "$exports_file"
    
    # Source the exports file
    source "$exports_file"
    
    # Add to shell rc file if not already there
    local rc_file="$HOME/.bashrc"
    if [[ "$SHELL" == *"zsh"* ]]; then
        rc_file="$HOME/.zshrc"
    fi
    
    if ! grep -q "source.*\.sparc_exports" "$rc_file" 2>/dev/null; then
        echo "# SPARC CLI Environment Variables" >> "$rc_file"
        echo "source $exports_file" >> "$rc_file"
    fi
    
    echo
    echo "Environment variables have been set and will be loaded in new shell sessions"
    echo "To use them in the current session, run: source $exports_file"
    echo
}

# Function to install local dependencies
install_local() {
    echo "Installing SPARC CLI locally..."
    echo "-------------------------------"
    
    # Check if Python is installed
    if ! command -v python3 &> /dev/null; then
        echo "Error: Python 3 is required but not installed."
        exit 1
    fi
    
    # Install pip if not present
    if ! command -v pip3 &> /dev/null; then
        echo "Installing pip..."
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        python3 get-pip.py
        rm get-pip.py
    fi
    
    # Install dependencies
    echo "Installing Python dependencies..."
    pip3 install --upgrade pip
    
    # Install in development mode with all dependencies
    echo "Installing SPARC CLI in development mode..."
    cd "$(dirname "$0")/.." && pip3 install -e ".[dev]"
    
    # Install Playwright browsers
    echo "Installing Playwright browsers..."
    python3 -m playwright install
    
    # Create an empty __init__.py if it doesn't exist
    touch "$(dirname "$0")/__init__.py"
    
    echo
    echo "Local installation complete!"
    echo "Run 'which sparc' to verify installation"
    echo "Then run 'sparc --help' to see available commands"
}

# Function to install Docker version
install_docker() {
    echo "Installing SPARC CLI via Docker..."
    echo "--------------------------------"
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        echo "Error: Docker is required but not installed."
        echo "Please install Docker first: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    # Make entrypoint script executable
    chmod +x docker-entrypoint.sh
    
    # Build Docker image
    echo "Building Docker image..."
    ./docker-entrypoint.sh
    
    echo
    echo "Docker installation complete!"
    echo "Run './docker-entrypoint.sh' to start using the CLI"
}

# Main installation flow
setup_environment

echo "Installation Options"
echo "-------------------"
echo "1) Local installation (requires Python 3)"
echo "2) Docker installation (requires Docker)"
echo
read -p "Choose installation method [1/2]: " choice

case $choice in
    1)
        install_local
        ;;
    2)
        install_docker
        ;;
    *)
        echo "Invalid choice. Please run the script again and select 1 or 2."
        exit 1
        ;;
esac

echo
echo "Installation completed successfully!"
echo "-----------------------------------"
echo "Your environment variables are saved in $HOME/.sparc_exports"
if [ "$choice" = "1" ]; then
    echo "Run 'source $HOME/.sparc_exports' then 'sparc' to start using the CLI"
else
    echo "Run 'source $HOME/.sparc_exports' then './docker-entrypoint.sh' to start using the CLI"
fi
