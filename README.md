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

### 2. Get Your Anthropic API Key

1. Go to [https://console.anthropic.com/](https://console.anthropic.com/)
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key
5. Copy the key (it starts with `sk-ant-...`)

### 3. Set Environment Variable

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
python log_analyzer_fixed.py your_logfile.log
```

### What Happens:

1. **Reads the log file** - Validates file exists and is readable
2. **Sends to Claude API** - Uploads log content for analysis
3. **Receives analysis** - Claude provides structured troubleshooting report
4. **Displays results** - Shows analysis in terminal
5. **Saves to file** - Creates timestamped output file

### Example Output

```
======================================================================
  LOG ANALYZER - Fixed Version
======================================================================

📋 API Key: sk-ant-api03-b......
📦 requests version: 2.21.0

📄 Log file: sample_application.log
✓ Read sample_application.log (2359 chars, 27 lines)

⏳ Calling Claude API...
   Endpoint: https://api.anthropic.com/v1/messages
   Model: claude-sonnet-4-20250514
   Payload size: 2584 bytes
✓ Response received (status: 200)
✓ Analysis complete (3291 chars)

======================================================================
  RESULTS
======================================================================

## Log Analysis Results

### 1. Main Errors

**Database Connectivity Issues:**
- Connection timeouts after 30 seconds
- `java.sql.SQLException: Unable to acquire JDBC Connection`
- Connection refused errors
- Database connection pool exhaustion (0/20 available)

**Application Performance Issues:**
- OutOfMemoryError: Java heap space
- GC overhead limit exceeded (98% time spent in garbage collection)
- Request timeouts (60 seconds)

**Service Availability:**
- Multiple API endpoints returning 503 Service Unavailable
- Health check failures
- Service marked as unhealthy

### 2. Root Cause Analysis

**Primary Root Cause: Database Connection Pool Mismanagement**

The issue appears to stem from:
- **Connection leaks**: Connections not being properly returned to the pool
- **Inadequate pool sizing**: 20 connections may be insufficient for the workload
- **Missing connection validation**: No proper health checks for idle connections
- **Cascading failure**: Database issues leading to memory problems due to:
  - Accumulating request objects waiting for connections
  - Retry mechanisms consuming additional resources
  - Failed requests being held in memory

**Secondary Issues:**
- Insufficient heap memory allocation
- Lack of circuit breaker pattern implementation
- No connection timeout handling at application level

### 3. Fix Suggestions

#### Immediate Fixes (Hot Fixes)
1. **Increase JVM heap size**: `-Xmx4g -Xms2g`
2. **Implement connection leak detection**:
   ```properties
   spring.datasource.hikari.leak-detection-threshold=60000
   ```
3. **Add circuit breaker pattern** to prevent cascading failures

#### Short-term Fixes
1. **Optimize connection pool configuration**:
   ```properties
   spring.datasource.hikari.maximum-pool-size=50
   spring.datasource.hikari.minimum-idle=10
   spring.datasource.hikari.connection-timeout=20000
   spring.datasource.hikari.idle-timeout=300000
   spring.datasource.hikari.max-lifetime=600000
   ```

2. **Implement proper connection management**:
   - Use try-with-resources for all database operations
   - Add connection validation queries
   - Set appropriate statement and connection timeouts

3. **Add monitoring and alerting**:
   - Connection pool metrics
   - Memory usage alerts
   - Database connectivity monitoring

#### Long-term Fixes
1. **Database Performance Optimization**:
   - Review and optimize slow queries
   - Implement connection pooling at database level
   - Consider database clustering/replication

2. **Application Architecture Improvements**:
   - Implement database connection retry with exponential backoff
   - Add request queuing and rate limiting
   - Consider microservices pattern to isolate database failures

3. **Infrastructure Enhancements**:
   - Implement database health monitoring
   - Add automated failover mechanisms
   - Set up proper load balancing

#### Monitoring Recommendations
- Set up alerts for connection pool utilization >80%
- Monitor GC frequency and duration
- Track API response times and error rates
- Implement distributed tracing for database calls

The successful recovery after manual intervention confirms that the connection pool reset resolved the immediate issue, but implementing these preventive measures will help avoid similar incidents in the future.

✓ Saved to: analysis_20260205_205320.txt
======================================================================

```

## 📁 Project Structure

```
log-analyzer/
├── log_analyzer_fixed.py           # Main Python script
├── sample_application.log    # Sample log file for testing
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
