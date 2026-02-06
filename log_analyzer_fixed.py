#!/usr/bin/env python3
"""
Log Analysis & Troubleshooting Assistant
Fixed version - matches working curl command exactly

Author: Vaibhav Pawar
"""

import requests
import json
import os
import sys
from datetime import datetime

def read_log_file(filepath):
    """Read log file"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        print("✓ Read {} ({} chars, {} lines)".format(
            filepath, len(content), len(content.splitlines())
        ))
        return content
    except IOError as e:
        print("✗ Error reading file: {}".format(e))
        sys.exit(1)

def analyze_logs(log_content, api_key):
    """Call Claude API - matching the working curl command exactly"""
    
    url = "https://api.anthropic.com/v1/messages"
    
    # Headers - exactly like curl
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    
    # Simple prompt
    prompt = """Analyze these logs and identify:
1. Main errors
2. Root cause
3. Fix suggestions

LOGS:
{}""".format(log_content)
    
    # Request body
    payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1024,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    print("\n⏳ Calling Claude API...")
    print("   Endpoint: {}".format(url))
    print("   Model: claude-sonnet-4-20250514")
    print("   Payload size: {} bytes".format(len(json.dumps(payload))))
    
    try:
        # Disable SSL verification if that's causing issues
        # and set a very long timeout
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(payload),  # Use data instead of json
            timeout=180,  # 3 minutes
            verify=True  # Try with True first
        )
        
        print("✓ Response received (status: {})".format(response.status_code))
        
        if response.status_code != 200:
            print("\n✗ API Error:")
            print(response.text)
            sys.exit(1)
        
        result = response.json()
        text = result['content'][0]['text']
        
        print("✓ Analysis complete ({} chars)".format(len(text)))
        return text
        
    except requests.exceptions.SSLError as e:
        print("\n✗ SSL Error: {}".format(e))
        print("\nTrying without SSL verification...")
        
        # Retry without SSL verification
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(payload),
            timeout=180,
            verify=False
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['content'][0]['text']
        else:
            print("Still failed: {}".format(response.text))
            sys.exit(1)
            
    except requests.exceptions.Timeout:
        print("\n✗ Timeout after 180 seconds")
        print("\nDebugging info:")
        print("  - curl works fine")
        print("  - Python requests timing out")
        print("  - Possible proxy or firewall blocking Python")
        print("\nTry:")
        print("  1. Check if you're behind a corporate proxy")
        print("  2. Try: export HTTP_PROXY= ; export HTTPS_PROXY=")
        print("  3. Check requests version: pip show requests")
        sys.exit(1)
        
    except Exception as e:
        print("\n✗ Unexpected error: {}".format(type(e).__name__))
        print("   Details: {}".format(e))
        
        # Try to get more info
        import traceback
        traceback.print_exc()
        sys.exit(1)

def main():
    """Main"""
    print("\n" + "="*70)
    print("  LOG ANALYZER - Fixed Version")
    print("="*70)
    
    if len(sys.argv) < 2:
        print("\nUsage: python {} <logfile>".format(sys.argv[0]))
        sys.exit(1)
    
    # Get API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("\n✗ Set ANTHROPIC_API_KEY first")
        sys.exit(1)
    
    print("\n📋 API Key: {}...{}".format(api_key[:20], api_key[-10:]))
    
    # Check requests library version
    print("📦 requests version: {}".format(requests.__version__))
    
    # Read file
    log_file = sys.argv[1]
    print("\n📄 Log file: {}".format(log_file))
    log_content = read_log_file(log_file)
    
    # Analyze
    analysis = analyze_logs(log_content, api_key)
    
    # Show results
    print("\n" + "="*70)
    print("  RESULTS")
    print("="*70 + "\n")
    print(analysis)
    
    # Save
    output = "analysis_{}.txt".format(datetime.now().strftime('%Y%m%d_%H%M%S'))
    with open(output, 'w') as f:
        f.write(analysis)
    print("\n✓ Saved to: {}".format(output))
    print("="*70 + "\n")

if __name__ == "__main__":
    main()