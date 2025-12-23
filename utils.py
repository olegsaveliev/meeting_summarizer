"""
Utility functions for Meeting Summarizer
"""

import os
from datetime import datetime
from typing import Optional

def read_file(filepath: str) -> str:
    """
    Read content from a file
    
    Args:
        filepath: Path to file to read
        
    Returns:
        File contents as string
        
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(filepath: str, content: str) -> str:
    """
    Write content to a file
    
    Args:
        filepath: Path to write to
        content: Content to write
        
    Returns:
        The filepath that was written to
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath


def generate_filename(base_name: str, extension: str, output_dir: str = "output") -> str:
    """
    Generate a timestamped filename
    
    Args:
        base_name: Base name for file (e.g., "meeting_summary")
        extension: File extension (e.g., "md", "txt")
        output_dir: Directory to save file in
        
    Returns:
        Full filepath
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{base_name}_{timestamp}.{extension}"
    return os.path.join(output_dir, filename)


def count_words(text: str) -> int:
    """
    Count words in text
    
    Args:
        text: Text to count words in
        
    Returns:
        Number of words
    """
    return len(text.split())


def estimate_tokens(text: str) -> int:
    """
    Rough estimate of token count
    (Actual tokenization is more complex, but this is good enough)
    
    Args:
        text: Text to estimate tokens for
        
    Returns:
        Estimated token count
    """
    # Rough estimate: 1 token ≈ 4 characters or 0.75 words
    return int(len(text) / 4)


def truncate_text(text: str, max_tokens: int = 6000) -> tuple[str, bool]:
    """
    Truncate text if it exceeds max tokens
    
    Args:
        text: Text to potentially truncate
        max_tokens: Maximum tokens allowed
        
    Returns:
        Tuple of (text, was_truncated)
    """
    estimated_tokens = estimate_tokens(text)
    
    if estimated_tokens <= max_tokens:
        return text, False
    
    # Truncate to roughly max_tokens
    max_chars = max_tokens * 4
    truncated = text[:max_chars]
    
    # Try to truncate at a sentence boundary
    last_period = truncated.rfind('.')
    if last_period > max_chars * 0.8:  # If we found a period in the last 20%
        truncated = truncated[:last_period + 1]
    
    truncated += "\n\n[Note: Input was truncated due to length]"
    
    return truncated, True


def format_output_separator() -> str:
    """Return a nice separator for output"""
    return "\n" + "="*70 + "\n"


def print_success(message: str):
    """Print a success message"""
    print(f"✅ {message}")


def print_error(message: str):
    """Print an error message"""
    print(f"❌ {message}")


def print_info(message: str):
    """Print an info message"""
    print(f"ℹ️  {message}")


def print_warning(message: str):
    """Print a warning message"""
    print(f"⚠️  {message}")