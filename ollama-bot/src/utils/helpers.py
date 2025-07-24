def format_response(response):
    """Format the response from the Ollama model for better readability."""
    return response.strip()

def log_message(message, level='INFO'):
    """Log messages with different severity levels."""
    levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    if level not in levels:
        raise ValueError(f"Invalid log level: {level}")
    print(f"{level}: {message}")

def validate_input(user_input):
    """Validate user input to ensure it meets certain criteria."""
    if not user_input or len(user_input) < 1:
        raise ValueError("Input cannot be empty.")
    return True