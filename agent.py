"""
Meeting Summarizer Agent
Your production-ready AI agent!

Version: 1.0.0
"""

import sys
import os
from datetime import datetime
from typing import Optional
from openai import OpenAI

from config import Config
from prompts import Prompts
from utils import (
    read_file, write_file, generate_filename,
    count_words, estimate_tokens, truncate_text,
    print_success, print_error, print_info, print_warning,
    format_output_separator
)

__version__ = "1.0.0"
__author__ = "Oleg"


class MeetingSummarizer:
    """
    AI-powered meeting summarizer
    
    Takes rough meeting notes and generates:
    - Structured meeting summary
    - Follow-up email draft
    - Optional executive brief
    """
    
    def __init__(self, model: str = None, verbose: bool = True):
        """
        Initialize the Meeting Summarizer
        
        Args:
            model: AI model to use (default from config)
            verbose: Whether to print progress messages
        """
        self.model = model or Config.DEFAULT_MODEL
        self.verbose = verbose
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        
        # Cost tracking
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.api_calls = 0
        
        # Pricing (per 1K tokens) - Updated prices as of 2024
        self.pricing = {
            'gpt-3.5-turbo': {'input': 0.0015, 'output': 0.002},
            'gpt-4': {'input': 0.03, 'output': 0.06},
            'gpt-4-turbo': {'input': 0.01, 'output': 0.03}
        }
        
        if self.verbose:
            print_info(f"Initialized Meeting Summarizer with model: {self.model}")
    
    def _call_llm(self, prompt: str, system_prompt: str = None) -> str:
        """
        Call the LLM with a prompt
        
        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
            
        Returns:
            LLM response text
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        if self.verbose:
            tokens = estimate_tokens(prompt)
            print_info(f"Calling {self.model} (~{tokens} input tokens)...")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=Config.TEMPERATURE,
                max_tokens=Config.MAX_OUTPUT_TOKENS
            )
            
            # Track usage
            usage = response.usage
            self.total_input_tokens += usage.prompt_tokens
            self.total_output_tokens += usage.completion_tokens
            self.api_calls += 1
            
            return response.choices[0].message.content
            
        except Exception as e:
            print_error(f"API call failed: {e}")
            raise
    
    def summarize_meeting(self, notes: str, date: str = None) -> str:
        """
        Generate meeting summary from notes
        
        Args:
            notes: Raw meeting notes
            date: Meeting date (optional, defaults to today)
            
        Returns:
            Formatted meeting summary
        """
        if self.verbose:
            words = count_words(notes)
            print_info(f"Processing meeting notes ({words} words)...")
        
        # Check and truncate if needed
        notes, was_truncated = truncate_text(notes, Config.MAX_INPUT_TOKENS)
        if was_truncated and self.verbose:
            print_warning("Input notes were truncated due to length")
        
        # Generate date if not provided
        if date is None:
            date = datetime.now().strftime("%B %d, %Y")
        
        # Create prompt
        prompt = Prompts.format_meeting_summary(notes, date)
        
        # Call LLM
        summary = self._call_llm(prompt, Prompts.SYSTEM_PROMPT)
        
        if self.verbose:
            print_success("Meeting summary generated!")
        
        return summary
    
    def generate_email(self, summary: str) -> str:
        """
        Generate follow-up email from summary
        
        Args:
            summary: Meeting summary
            
        Returns:
            Email draft
        """
        if self.verbose:
            print_info("Generating follow-up email...")
        
        prompt = Prompts.format_email_followup(summary)
        email = self._call_llm(prompt, Prompts.SYSTEM_PROMPT)
        
        if self.verbose:
            print_success("Follow-up email generated!")
        
        return email
    
    def generate_exec_brief(self, summary: str) -> str:
        """
        Generate executive brief from summary
        
        Args:
            summary: Meeting summary
            
        Returns:
            Executive brief
        """
        if self.verbose:
            print_info("Generating executive brief...")
        
        prompt = Prompts.format_executive_brief(summary)
        brief = self._call_llm(prompt, Prompts.SYSTEM_PROMPT)
        
        if self.verbose:
            print_success("Executive brief generated!")
        
        return brief
    
    def get_cost_summary(self) -> dict:
        """Get cost summary for this session"""
        model_pricing = self.pricing.get(self.model, {'input': 0, 'output': 0})
        
        input_cost = (self.total_input_tokens / 1000) * model_pricing['input']
        output_cost = (self.total_output_tokens / 1000) * model_pricing['output']
        total_cost = input_cost + output_cost
        
        return {
            'api_calls': self.api_calls,
            'input_tokens': self.total_input_tokens,
            'output_tokens': self.total_output_tokens,
            'total_tokens': self.total_input_tokens + self.total_output_tokens,
            'input_cost': input_cost,
            'output_cost': output_cost,
            'total_cost': total_cost,
            'model': self.model
        }
    
    def print_cost_summary(self):
        """Print cost summary"""
        summary = self.get_cost_summary()
        
        print(format_output_separator())
        print("💰 COST SUMMARY")
        print(format_output_separator())
        print(f"Model:        {summary['model']}")
        print(f"API Calls:    {summary['api_calls']}")
        print(f"Tokens:       {summary['total_tokens']:,} ({summary['input_tokens']:,} in + {summary['output_tokens']:,} out)")
        print(f"Cost:         ${summary['total_cost']:.4f}")
        print(format_output_separator())
    
    def process_meeting(
        self,
        notes: str,
        date: str = None,
        generate_email: bool = None,
        generate_brief: bool = None,
        output_dir: str = None
    ) -> dict:
        """
        Complete meeting processing workflow
        
        Args:
            notes: Raw meeting notes
            date: Meeting date (optional)
            generate_email: Whether to generate email (default from config)
            generate_brief: Whether to generate brief (default from config)
            output_dir: Where to save outputs (default from config)
            
        Returns:
            Dictionary with all outputs and file paths
        """
        if self.verbose:
            print(format_output_separator())
            print("🚀 MEETING SUMMARIZER - Starting Processing")
            print(format_output_separator())
        
        # Use config defaults if not specified
        generate_email = generate_email if generate_email is not None else Config.GENERATE_EMAIL
        generate_brief = generate_brief if generate_brief is not None else Config.GENERATE_EXEC_BRIEF
        output_dir = output_dir or Config.OUTPUT_DIR
        
        results = {}
        
        # Step 1: Generate meeting summary
        summary = self.summarize_meeting(notes, date)
        results['summary'] = summary
        
        # Save summary
        summary_path = generate_filename("meeting_summary", "md", output_dir)
        write_file(summary_path, summary)
        results['summary_file'] = summary_path
        
        if self.verbose:
            print_success(f"Summary saved: {summary_path}")
        
        # Step 2: Generate email (if requested)
        if generate_email:
            email = self.generate_email(summary)
            results['email'] = email
            
            # Save email
            email_path = generate_filename("meeting_followup_email", "txt", output_dir)
            write_file(email_path, email)
            results['email_file'] = email_path
            
            if self.verbose:
                print_success(f"Email saved: {email_path}")
        
        # Step 3: Generate executive brief (if requested)
        if generate_brief:
            brief = self.generate_exec_brief(summary)
            results['brief'] = brief
            
            # Save brief
            brief_path = generate_filename("executive_brief", "txt", output_dir)
            write_file(brief_path, brief)
            results['brief_file'] = brief_path
            
            if self.verbose:
                print_success(f"Brief saved: {brief_path}")
        
        # Print cost summary
        if self.verbose:
            self.print_cost_summary()
        
        if self.verbose:
            print(format_output_separator())
            print("✅ PROCESSING COMPLETE!")
            print(format_output_separator())
        
        return results


def interactive_mode():
    """
    Interactive mode for quick summaries
    """
    print(format_output_separator())
    print("🎤 INTERACTIVE MODE")
    print("Enter your meeting notes (press Ctrl+D when done, Ctrl+C to cancel):")
    print(format_output_separator())
    
    # Read multi-line input
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
    except KeyboardInterrupt:
        print("\n")
        print_warning("Cancelled")
        return
    
    notes = '\n'.join(lines)
    
    if not notes.strip():
        print_error("No notes entered!")
        return
    
    print(format_output_separator())
    
    # Ask for options
    print("Options:")
    print("  [1] Summary only")
    print("  [2] Summary + Email")
    print("  [3] Summary + Email + Brief")
    
    choice = input("\nChoice (1-3): ").strip()
    
    generate_email = choice in ['2', '3']
    generate_brief = choice == '3'
    
    # Ask for model
    print("\nModel:")
    print("  [1] GPT-3.5-turbo (fast, cheap)")
    print("  [2] GPT-4 (slower, better)")
    
    model_choice = input("\nChoice (1-2, default 1): ").strip() or '1'
    model = "gpt-4" if model_choice == '2' else "gpt-3.5-turbo"
    
    # Process
    summarizer = MeetingSummarizer(model=model)
    results = summarizer.process_meeting(
        notes=notes,
        generate_email=generate_email,
        generate_brief=generate_brief
    )
    
    # Display results
    print(format_output_separator())
    print("📄 SUMMARY:")
    print(format_output_separator())
    print(results['summary'])
    
    if 'email' in results:
        print(format_output_separator())
        print("📧 EMAIL:")
        print(format_output_separator())
        print(results['email'])
    
    print(format_output_separator())
    print_success("Done! Files saved to output/")


def batch_process(input_dir: str, output_dir: str = None, model: str = None):
    """
    Process multiple meeting notes files
    
    Args:
        input_dir: Directory containing meeting notes files
        output_dir: Where to save outputs
        model: AI model to use
    """
    import glob
    
    output_dir = output_dir or Config.OUTPUT_DIR
    
    # Find all text files
    pattern = os.path.join(input_dir, "*.txt")
    files = glob.glob(pattern)
    
    if not files:
        print_error(f"No .txt files found in {input_dir}")
        return
    
    print_info(f"Found {len(files)} files to process")
    print(format_output_separator())
    
    summarizer = MeetingSummarizer(model=model, verbose=False)
    
    results = []
    for i, filepath in enumerate(files, 1):
        filename = os.path.basename(filepath)
        print(f"[{i}/{len(files)}] Processing {filename}...")
        
        try:
            notes = read_file(filepath)
            result = summarizer.process_meeting(
                notes=notes,
                output_dir=output_dir
            )
            result['source_file'] = filename
            results.append(result)
            print_success(f"  Done: {result['summary_file']}")
            
        except Exception as e:
            print_error(f"  Failed: {e}")
            continue
    
    print(format_output_separator())
    print_success(f"Processed {len(results)}/{len(files)} files")
    
    # Print cost summary
    summarizer.print_cost_summary()
    
    return results


def main():
    """
    Command-line interface for Meeting Summarizer
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description="AI-Powered Meeting Summarizer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Summarize from file:
  python agent.py --input notes.txt
  
  # Summarize from text:
  python agent.py --text "Meeting notes here..."
  
  # Interactive mode:
  python agent.py --interactive
  
  # Batch process directory:
  python agent.py --batch ./meetings/
  
  # Use GPT-4 (higher quality):
  python agent.py --input notes.txt --model gpt-4
  
  # Generate email only (no brief):
  python agent.py --input notes.txt --email --no-brief
  
  # Custom output directory:
  python agent.py --input notes.txt --output ./my_summaries/
        """
    )
    
    # Version
    parser.add_argument(
        '--version',
        action='version',
        version=f'Meeting Summarizer v{__version__}'
    )
    
    # Interactive mode flag
    parser.add_argument(
        '--interactive', '-I',
        action='store_true',
        help='Interactive mode (enter notes directly)'
    )
    
    # Batch processing
    parser.add_argument(
        '--batch', '-b',
        type=str,
        help='Batch process all .txt files in directory'
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=False)
    input_group.add_argument(
        '--input', '-i',
        type=str,
        help='Path to file containing meeting notes'
    )
    input_group.add_argument(
        '--text', '-t',
        type=str,
        help='Meeting notes as text'
    )
    
    # Optional arguments
    parser.add_argument(
        '--date', '-d',
        type=str,
        help='Meeting date (default: today)',
        default=None
    )
    
    parser.add_argument(
        '--model', '-m',
        type=str,
        choices=['gpt-3.5-turbo', 'gpt-4', 'gpt-4-turbo'],
        help=f'AI model to use (default: {Config.DEFAULT_MODEL})',
        default=Config.DEFAULT_MODEL
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help=f'Output directory (default: {Config.OUTPUT_DIR})',
        default=Config.OUTPUT_DIR
    )
    
    parser.add_argument(
        '--email',
        action='store_true',
        help='Generate follow-up email'
    )
    
    parser.add_argument(
        '--no-email',
        action='store_true',
        help='Skip email generation'
    )
    
    parser.add_argument(
        '--brief',
        action='store_true',
        help='Generate executive brief'
    )
    
    parser.add_argument(
        '--no-brief',
        action='store_true',
        help='Skip brief generation'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Quiet mode (minimal output)'
    )
    
    args = parser.parse_args()
    
    # Check if interactive mode
    if args.interactive:
        interactive_mode()
        sys.exit(0)
    
    # Check if batch mode
    if args.batch:
        batch_process(args.batch, args.output, args.model)
        sys.exit(0)
    
    # If not interactive or batch, require input
    if not (args.input or args.text):
        parser.print_help()
        print_error("\nError: Either --input, --text, --interactive, or --batch is required")
        sys.exit(1)
    
    try:
        # Get meeting notes
        if args.input:
            notes = read_file(args.input)
        else:
            notes = args.text
        
        if not notes or not notes.strip():
            print_error("Meeting notes are empty!")
            sys.exit(1)
        
        # Determine what to generate
        generate_email = not args.no_email if args.no_email else (args.email or Config.GENERATE_EMAIL)
        generate_brief = not args.no_brief if args.no_brief else (args.brief or Config.GENERATE_EXEC_BRIEF)
        
        # Create summarizer
        summarizer = MeetingSummarizer(
            model=args.model,
            verbose=not args.quiet
        )
        
        # Process meeting
        results = summarizer.process_meeting(
            notes=notes,
            date=args.date,
            generate_email=generate_email,
            generate_brief=generate_brief,
            output_dir=args.output
        )
        
        # Print file locations
        if not args.quiet:
            print("\n📁 Output Files:")
            print(f"   Summary: {results['summary_file']}")
            if 'email_file' in results:
                print(f"   Email:   {results['email_file']}")
            if 'brief_file' in results:
                print(f"   Brief:   {results['brief_file']}")
            print()
        
        print_success("Meeting summarized successfully!")
        
    except FileNotFoundError as e:
        print_error(str(e))
        print_info("Make sure the file path is correct")
        print_info(f"Current directory: {os.getcwd()}")
        sys.exit(1)
    
    except ValueError as e:
        print_error(str(e))
        print_info("Check your configuration in config.py")
        sys.exit(1)
    
    except KeyboardInterrupt:
        print_warning("\nInterrupted by user")
        sys.exit(130)
    
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        print_info("This might be an API issue. Check:")
        print_info("  1. Internet connection")
        print_info("  2. API key is valid")
        print_info("  3. API service status: https://status.openai.com/")
        if not args.quiet:
            print("\n🐛 Full error details:")
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()