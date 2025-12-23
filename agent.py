"""
Meeting Summarizer Agent
Your production-ready AI agent!
"""

import sys
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
        
        if self.verbose:
            print(format_output_separator())
            print("✅ PROCESSING COMPLETE!")
            print(format_output_separator())
        
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
  
  # Use GPT-4 (higher quality):
  python agent.py --input notes.txt --model gpt-4
  
  # Generate email only (no brief):
  python agent.py --input notes.txt --email --no-brief
  
  # Custom output directory:
  python agent.py --input notes.txt --output ./my_summaries/
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
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
        sys.exit(1)
    
    except KeyboardInterrupt:
        print_warning("\nInterrupted by user")
        sys.exit(130)
    
    except Exception as e:
        print_error(f"Error: {e}")
        if not args.quiet:
            import traceback
            print("\nFull error:")
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()