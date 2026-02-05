# Log Analysis & Troubleshooting Assistant

A Python tool that leverages Claude AI API to analyze application logs and provide intelligent troubleshooting recommendations.

##  Overview

As a Solutions Architect with 10+ years of troubleshooting experience, I built this tool to accelerate the initial triage phase of incident response. Instead of manually scanning through hundreds of log lines, this tool uses Claude AI to provide structured analysis, identify root causes, and suggest prioritized troubleshooting steps.

**Author:** Vaibhav Pawar  
**Purpose:** Demonstrate practical LLM API integration for technical troubleshooting workflows

## Use Case

When investigating production incidents, the first step is often analyzing logs to understand what went wrong. This tool automates that initial analysis by:
- Identifying errors, warnings, and patterns
- Suggesting root causes based on log evidence
- Providing prioritized troubleshooting steps
- Recommending preventive measures

## Requirements

- **Python 3.7+**
- **Anthropic API key** (Claude)

## Installation

### 1. Clone or Download This Project

```bash
mkdir log-analyzer
cd log-analyzer
```

### 2. Install Dependencies

```bash
pip install anthropic
```

Or create a `requirements.txt`:
```bash
echo "anthropic>=0.39.0" > requirements.txt
pip install -r requirements.txt
```

### 3. Get Your Anthropic API Key

1. Go to [https://console.anthropic.com/](https://console.anthropic.com/)
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key
5. Copy the key (it starts with `sk-ant-...`)

### 4. Set Environment Variable

**Linux/Mac:**
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

**Windows (Command Prompt):**
```cmd
set ANTHROPIC_API_KEY=your-api-key-here
```

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY="your-api-key-here"
```

To make it permanent, add to your `.bashrc`, `.zshrc`, or system environment variables.

## Usage

### Basic Usage

```bash
python log_analyzer.py sample_application.log
```

### What Happens:

1. **Reads the log file** - Validates file exists and is readable
2. **Sends to Claude API** - Uploads log content for analysis
3. **Receives analysis** - Claude provides structured troubleshooting report
4. **Displays results** - Shows analysis in terminal
5. **Saves to file** - Creates timestamped output file

### Example Output

```
================================================================================
  LOG ANALYSIS & TROUBLESHOOTING ASSISTANT
  Using Claude API for Intelligent Analysis
================================================================================

📄 Reading log file: sample_application.log
✓ Successfully read sample_application.log
📊 Log file size: 2847 characters
📊 Log file lines: 28 lines

⏳ Analyzing logs with Claude AI...
✓ Analysis complete!

================================================================================
  ANALYSIS RESULTS
================================================================================

1. **Summary of Issues Found**

   - Database Connection Failures (3 occurrences)
     - Timeouts after 30000ms
     - Connection refused errors
     - Led to service being marked unhealthy

   - API Request Failures (3 occurrences)
     - All returned 503 Service Unavailable
     - Caused by database connectivity issues

   - Memory Issues (2 occurrences)
     - OutOfMemoryError: Java heap space
     - GC overhead limit exceeded (98% time in GC)

   - Connection Pool Exhaustion (1 occurrence)
     - All 20 connections depleted (0/20 available)

2. **Root Cause Analysis**

   Primary Issue: Database connection timeout leading to cascade failure
   
   Chain of Events:
   - Initial database connection timeout at 10:24:12
   - Retry attempts failed (3 attempts over 66 seconds)
   - Connection pool became exhausted (all connections stuck waiting)
   - API requests started failing with 503 errors
   - Memory pressure from accumulating failed requests
   - GC thrashing trying to free memory

   Contributing Factor: Possible memory leak or insufficient heap size
   compounded the database connectivity issue.

3. **Troubleshooting Steps** (Priority Order)

   URGENT:
   
   Step 1: Verify database availability
   ```bash
   # Check if database is accessible
   telnet <db-host> <db-port>
   # Check database logs for errors
   ```

   Step 2: Check network connectivity
   ```bash
   # Verify network path to database
   ping <db-host>
   traceroute <db-host>
   # Check firewall rules
   ```

   Step 3: Analyze database connection settings
   - Review connection timeout configuration (currently 30000ms)
   - Check max connections limit on database side
   - Verify connection pool settings (size: 20)

   FOLLOW-UP:

   Step 4: Investigate memory issues
   ```bash
   # Get heap dump for analysis
   jmap -dump:live,format=b,file=heap.bin <pid>
   # Analyze with tools like VisualVM or Eclipse MAT
   ```

   Step 5: Review application logs on database server
   - Check for connection limit exceeded
   - Look for authentication failures
   - Review slow query logs

4. **Prevention Recommendations**

   Configuration:
   - Increase JVM heap size (currently insufficient for load)
   - Tune GC settings for better performance
   - Implement connection timeout with circuit breaker pattern
   - Increase connection pool size if database can handle it

   Monitoring:
   - Add alerts for database connection pool usage (>80%)
   - Monitor database response times
   - Alert on heap usage >85%
   - Track GC overhead percentage

   Code Improvements:
   - Implement connection retry with exponential backoff
   - Add circuit breaker to fail fast when database is down
   - Ensure proper connection cleanup in error paths
   - Add connection pool monitoring metrics

   Infrastructure:
   - Review database capacity and performance
   - Consider database connection pooler (PgBouncer, etc.)
   - Implement health checks with faster timeout
   - Add database read replica for read traffic

================================================================================
✓ Analysis complete! Check the output file for full results.
================================================================================
```

## 📁 Project Structure

```
log-analyzer/
├── log_analyzer.py           # Main Python script
├── sample_application.log    # Sample log file for testing
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── analysis_results_*.txt    # Output files (generated)
```

## 🔧 How It Works

### Code Walkthrough

**1. Reading Log Files**
```python
def read_log_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    return content
```
Simple file reading with error handling for missing files.

**2. Calling Claude API**
```python
client = anthropic.Anthropic(api_key=api_key)

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=2000,
    temperature=0.3,  # Lower = more focused
    messages=[
        {"role": "user", "content": prompt}
    ]
)

analysis = message.content[0].text
```

Key parameters:
- `model`: Claude Sonnet 4 (latest, best for analysis)
- `max_tokens`: Maximum response length
- `temperature`: 0.3 for focused, analytical responses (0.0 = deterministic, 1.0 = creative)
- `messages`: Conversation format (user/assistant turns)

**3. Prompt Engineering**
The prompt instructs Claude to:
- Summarize issues by type and count
- Identify root causes and correlations
- Provide prioritized troubleshooting steps
- Suggest prevention measures

**4. Structured Output**
Claude returns analysis with:
- Clear sections (Summary, Root Cause, Steps, Prevention)
- Bullet points for readability
- Specific commands where applicable
- Priority ordering

## 🎓 Learning Points

### What This Demonstrates

**LLM API Integration:**
- Making HTTP API calls to Anthropic
- Handling API authentication
- Request/response processing
- Error handling

**Prompt Engineering:**
- Crafting effective system prompts
- Structuring output format
- Getting consistent, useful responses

**Practical Application:**
- Real-world use case (log analysis)
- Automation of manual tasks
- Integration into troubleshooting workflows

### Key Concepts

**Temperature Setting:**
- `0.0-0.3`: Focused, deterministic (good for analysis, facts)
- `0.4-0.7`: Balanced (general purpose)
- `0.8-1.0`: Creative (writing, brainstorming)

**Token Limits:**
- Input + output cannot exceed model's context window
- Sonnet 4 supports up to 200k tokens
- We set `max_tokens=2000` for responses

**Error Handling:**
- Check for API key before making calls
- Handle network errors gracefully
- Provide clear error messages to user

## 🔍 Testing

### Test with Sample Log

```bash
python log_analyzer.py sample_application.log
```

### Test with Your Own Logs

```bash
python log_analyzer.py /path/to/your/logfile.log
```

### Expected Behavior

✅ Should read the log file  
✅ Should analyze within 5-10 seconds  
✅ Should produce structured output  
✅ Should save results to timestamped file  

## Troubleshooting

**Error: "ANTHROPIC_API_KEY environment variable not set"**
- Solution: Set the environment variable as shown in Installation

**Error: "File not found"**
- Solution: Check file path is correct
- Use absolute path if relative path not working

**Error: "API Error: 401 Unauthorized"**
- Solution: Check your API key is valid
- Regenerate key if needed from console.anthropic.com

**Error: "API Error: 429 Rate Limit"**
- Solution: You've hit the rate limit
- Wait a minute and try again
- Consider upgrading your API plan

## Future Enhancements

- [ ] Support for multiple log formats (JSON, syslog, etc.)
- [ ] Batch processing (analyze multiple files)
- [ ] Pattern detection across multiple log files
- [ ] Integration with monitoring tools (Grafana, Splunk)
- [ ] Real-time log streaming analysis
- [ ] Custom prompt templates for different log types
- [ ] Cost tracking (API token usage)

## Notes

**API Costs:**
- Claude Sonnet 4: ~$3 per million input tokens, ~$15 per million output tokens
- Sample log analysis: ~0.5 cents per run
- Very affordable for occasional use

**Privacy:**
- Logs are sent to Anthropic's API
- Don't use with logs containing sensitive data (PII, secrets, passwords)
- For sensitive logs, use Claude locally or sanitize first

**Performance:**
- Analysis takes 5-10 seconds typically
- Depends on log file size and API response time
- Network latency affects total time

## Contributing

This is a demonstration project for interview purposes. Feel free to fork and adapt for your needs!

## License

This is a personal project for educational and demonstration purposes.

## Author

**Vaibhav Pawar**  
Solutions Architect | 10+ years in technical troubleshooting and escalation engineering

Built as part of exploring practical applications of LLM APIs in technical support and troubleshooting workflows.

---

**Questions or feedback?** Feel free to reach out!
