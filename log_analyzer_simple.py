#!/usr/bin/env python3
"""
Log Analysis & Troubleshooting Assistant (Python 3.7 Compatible)
Uses Claude API via direct HTTP requests (no complex dependencies)

Author: Vaibhav Pawar
Purpose: Demonstrate LLM API integration for technical troubleshooting
"""

import requests
import json
import os
import sys
from datetime import datetime

def read_log_file(filepath):
    """
    Read and return contents of a log file
    
    Args:
        filepath (str): Path to the log file
    
    Returns:
        str: Contents of the log file
    """
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        print("✓ Successfully read {}".format(filepath))
        return content
    except IOError as e:
        print("✗ Error: File '{}' not found".format(filepath))
        sys.exit(1)

def analyze_logs_with_claude(log_content):
    """
    Send logs to Claude API for analysis using direct HTTP request
    
    Args:
        log_content (str): The log file content to analyze
    
    Returns:
        str: Claude's analysis and recommendations
    """
    # Get API key from environment variable
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("✗ Error: ANTHROPIC_API_KEY environment variable not set")
        print("\nTo set it:")
        print("  export ANTHROPIC_API_KEY='your-api-key-here'")
        sys.exit(1)
    
    # API endpoint
    url = "https://api.anthropic.com/v1/messages"
    
    # Headers
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    
    # Create the analysis prompt
    prompt = """You are an expert systems engineer analyzing application logs. 

Analyze the following log entries and provide:

1. **Summary of Issues Found**
   - List all errors, warnings, and anomalies
   - Group similar issues together
   - Count occurrences of each issue type

2. **Root Cause Analysis**
   - Identify the most likely root cause(s)
   - Explain the chain of events leading to failures
   - Note any patterns or correlations

3. **Troubleshooting Steps** (in priority order)
   - Step-by-step actions to diagnose and fix
   - Include specific commands or checks where applicable
   - Indicate which steps are urgent vs optional

4. **Prevention Recommendations**
   - How to prevent this issue from recurring
   - Monitoring improvements
   - Configuration or code changes needed

Format your response clearly with headers and bullet points.

LOG CONTENT:
{}

ANALYSIS:""".format(log_content)
    
    # Request body
    data = {
        "model": "claude-3-sonnet-20240229",  # Using Claude 3 Sonnet (stable)
        "max_tokens": 2000,
        "temperature": 0.3,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    try:
        print("\n⏳ Analyzing logs with Claude AI...")
        
        # Make API request
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        # Check if request was successful
        if response.status_code != 200:
            print("✗ API Error: {} - {}".format(response.status_code, response.text))
            sys.exit(1)
        
        # Parse response
        result = response.json()
        
        # Extract text from response
        analysis = result['content'][0]['text']
        
        print("✓ Analysis complete!")
        return analysis
    
    except requests.exceptions.Timeout:
        print("✗ Error: Request timed out. Please try again.")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print("✗ Network error: {}".format(e))
        sys.exit(1)
    except (KeyError, IndexError) as e:
        print("✗ Error parsing API response: {}".format(e))
        print("Response: {}".format(response.text))
        sys.exit(1)

def save_analysis(analysis, output_file):
    """
    Save analysis results to a file
    
    Args:
        analysis (str): The analysis text to save
        output_file (str): Path to output file
    """
    try:
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        with open(output_file, 'w') as f:
            f.write("Log Analysis Report\n")
            f.write("Generated: {}\n".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            f.write("=" * 80 + "\n\n")
            f.write(analysis)
        
        print("✓ Analysis saved to: {}".format(output_file))
    except IOError as e:
        print("✗ Error saving analysis: {}".format(e))

def main():
    """
    Main function - orchestrates the log analysis workflow
    """
    # Print banner
    print("\n" + "=" * 80)
    print("  LOG ANALYSIS & TROUBLESHOOTING ASSISTANT")
    print("  Using Claude API for Intelligent Analysis")
    print("=" * 80 + "\n")
    
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python log_analyzer_simple.py <log_file_path>")
        print("\nExample:")
        print("  python log_analyzer_simple.py sample_application.log")
        print("\nMake sure to set ANTHROPIC_API_KEY environment variable first:")
        print("  export ANTHROPIC_API_KEY='your-api-key-here'")
        sys.exit(1)
    
    # Get log file path from command line
    log_file = sys.argv[1]
    
    print("📄 Reading log file: {}".format(log_file))
    log_content = read_log_file(log_file)
    
    print("📊 Log file size: {} characters".format(len(log_content)))
    print("📊 Log file lines: {} lines".format(len(log_content.splitlines())))
    
    # Analyze logs with Claude
    analysis = analyze_logs_with_claude(log_content)
    
    # Display results
    print("\n" + "=" * 80)
    print("  ANALYSIS RESULTS")
    print("=" * 80 + "\n")
    print(analysis)
    
    # Save results to file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = "analysis_results_{}.txt".format(timestamp)
    save_analysis(analysis, output_file)
    
    print("\n" + "=" * 80)
    print("✓ Analysis complete! Check the output file for full results.")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()