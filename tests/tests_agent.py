"""
Unit tests for Meeting Summarizer
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent import MeetingSummarizer
from utils import count_words, estimate_tokens, truncate_text


def test_basic_summarization():
    """Test basic meeting summarization"""
    notes = """
    Quick team sync.
    Discussed project timeline.
    John will handle backend.
    Sarah on frontend.
    Need to launch by March.
    """
    
    summarizer = MeetingSummarizer(verbose=False)
    summary = summarizer.summarize_meeting(notes)
    
    assert summary is not None
    assert len(summary) > 100  # Should be substantial
    assert "ACTION ITEMS" in summary or "action" in summary.lower()
    
    print("✅ Basic summarization test passed")


def test_utils():
    """Test utility functions"""
    text = "This is a test sentence with several words in it."
    
    # Test word count
    words = count_words(text)
    assert words == 10
    
    # Test token estimation
    tokens = estimate_tokens(text)
    assert tokens > 0
    assert tokens < 100
    
    # Test truncation
    long_text = "word " * 2000
    truncated, was_truncated = truncate_text(long_text, max_tokens=100)
    assert was_truncated
    assert len(truncated) < len(long_text)
    
    print("✅ Utility functions test passed")


def test_cost_tracking():
    """Test cost tracking"""
    notes = "Quick meeting. John will do task A. Sarah will do task B."
    
    summarizer = MeetingSummarizer(verbose=False)
    summarizer.summarize_meeting(notes)
    
    cost_summary = summarizer.get_cost_summary()
    
    assert cost_summary['api_calls'] > 0
    assert cost_summary['total_tokens'] > 0
    assert cost_summary['total_cost'] >= 0
    
    print("✅ Cost tracking test passed")
    print(f"   Cost for test: ${cost_summary['total_cost']:.4f}")


if __name__ == "__main__":
    print("🧪 Running tests...\n")
    
    try:
        test_utils()
        test_basic_summarization()
        test_cost_tracking()
        
        print("\n" + "="*50)
        print("✅ ALL TESTS PASSED!")
        print("="*50)
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)