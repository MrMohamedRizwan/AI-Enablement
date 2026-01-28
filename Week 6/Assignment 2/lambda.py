"""
AWS Lambda function for web scraping
Handles Bedrock Agent action group requests
"""

import json
import boto3
from scraper import WebScraper
from cleaner import ContentCleaner

# Initialize
scraper = WebScraper(
    max_size_mb=10,
    timeout_seconds=60,
    max_redirects=5
)
cleaner = ContentCleaner()
bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')


def lambda_handler(event, context):
    """
    Main Lambda handler for Bedrock Agent
    """
    print(f"Received event: {json.dumps(event)}")
    
    # Parse Bedrock Agent event
    action_group = event.get('actionGroup', '')
    function = event.get('function', '')
    parameters = event.get('parameters', [])
    
    # Extract URL from parameters
    url = None
    for param in parameters:
        if param.get('name') == 'url':
            url = param.get('value')
            break
    
    if not url:
        return format_response(
            400,
            "Missing required parameter: url",
            action_group,
            function
        )
    
    try:
        # Step 1: Fetch the web page
        print(f"Fetching URL: {url}")
        html_content, final_url, content_type = scraper.fetch(url)
        
        # Step 2: Clean and extract text
        print(f"Cleaning content from: {final_url}")
        cleaned_text = cleaner.clean_html(html_content)
        
        # Step 3: Summarize if too long
        if len(cleaned_text) > 5000:
            print("Content too long, summarizing...")
            summary = summarize_text(cleaned_text)
            result = {
                "url": final_url,
                "content_length": len(cleaned_text),
                "summary": summary,
                "full_text_truncated": cleaned_text[:2000] + "..."
            }
        else:
            result = {
                "url": final_url,
                "content_length": len(cleaned_text),
                "text": cleaned_text
            }
        
        return format_response(200, result, action_group, function)
        
    except Exception as e:
        print(f"Error processing URL: {str(e)}")
        return format_response(
            500,
            f"Failed to crawl URL: {str(e)}",
            action_group,
            function
        )


def summarize_text(text):
    """
    Use Claude to summarize long text
    """
    try:
        prompt = f"""Please provide a concise summary of the following web page content:

{text[:8000]}

Provide a clear, structured summary highlighting the main points."""

        response = bedrock_runtime.invoke_model(
            modelId='us.anthropic.claude-3-5-sonnet-20241022-v2:0',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "temperature": 0.3,
                "messages": [{
                    "role": "user",
                    "content": prompt
                }]
            })
        )
        
        response_body = json.loads(response['body'].read())
        summary = response_body['content'][0]['text']
        return summary
        
    except Exception as e:
        print(f"Summarization failed: {e}")
        return text[:2000] + "... (summarization failed)"


def format_response(status_code, body, action_group, function):
    """
    Format response for Bedrock Agent
    """
    if isinstance(body, dict):
        body_text = json.dumps(body, indent=2)
    else:
        body_text = str(body)
    
    return {
        'messageVersion': '1.0',
        'response': {
            'actionGroup': action_group,  # Echo back the action group from event
            'function': function,          # Echo back the function from event
            'functionResponse': {
                'responseBody': {
                    'TEXT': {
                        'body': body_text
                    }
                }
            }
        }
    }