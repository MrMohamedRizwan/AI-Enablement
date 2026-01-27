from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os
import pickle
import io
import re
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from PyPDF2 import PdfReader

# Create FastAPI app
app = FastAPI()

# MCP instance
mcp = FastMCP("Presidio Insurance MCP")

# Global variable to store document content
INSURANCE_DOCS_CONTENT = ""

# Scopes required for Google Drive access
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def load_google_drive_docs():
    """Load and extract text from Google Drive (supports PDF, Google Docs, text files)"""
    global INSURANCE_DOCS_CONTENT
    
    creds = None
    token_path = 'token.pickle'
    credentials_path = './credentials.json'
    
    # Check if credentials.json exists
    if not os.path.exists(credentials_path):
        return False
    
    try:
        # Load saved credentials if they exist
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
        
        # If no valid credentials, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("🔄 Refreshing expired credentials...")
                creds.refresh(Request())
            else:
                print("🔐 Starting OAuth authentication flow...")
                print("📱 A browser window will open for authentication...")
                
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        credentials_path, 
                        SCOPES,
                        redirect_uri='http://localhost:8080/'
                    )
                    creds = flow.run_local_server(
                        port=8080,
                        success_message='Authentication successful! You can close this window.',
                        open_browser=True
                    )
                    print("Authentication successful!")
                except Exception as auth_error:
                    print(f"Authentication failed: {auth_error}")
                    return False
            
            # Save credentials for next time
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
        
        # Build Google Drive service
        service = build('drive', 'v3', credentials=creds)
        
        # Your file ID from the URL
        file_id = "1ffawzXfUOuIzoLS5hlrk-1L4UNjDUq3I"
        
        # Get file metadata
        print("Fetching file metadata...")
        file_metadata = service.files().get(fileId=file_id, fields='name,mimeType,size').execute()
        file_name = file_metadata.get('name')
        mime_type = file_metadata.get('mimeType')
        file_size = file_metadata.get('size', 'Unknown')
        
        print(f"File: {file_name}")
        print(f"Type: {mime_type}")
        print(f"Size: {file_size} bytes")
        
        if 'google-apps.document' in mime_type:
            print("Exporting Google Doc as text...")
            request = service.files().export_media(fileId=file_id, mimeType='text/plain')
            file_content = io.BytesIO()
            downloader = MediaIoBaseDownload(file_content, request)
            
            done = False
            while not done:
                status, done = downloader.next_chunk()
                if status:
                    print(f"\r Downloading... {int(status.progress() * 100)}%", end='')
            print("\rDownload complete!       ")
            
            file_content.seek(0)
            INSURANCE_DOCS_CONTENT = file_content.read().decode('utf-8', errors='ignore')
            
        elif 'pdf' in mime_type.lower():
            # Handle PDF files
            print("Downloading PDF file...")
            request = service.files().get_media(fileId=file_id)
            pdf_content = io.BytesIO()
            downloader = MediaIoBaseDownload(pdf_content, request)
            
            done = False
            while not done:
                status, done = downloader.next_chunk()
                if status:
                    print(f"\rDownloading... {int(status.progress() * 100)}%", end='')
            print("\rDownload complete!")
            
            # Extract text from PDF
            print("Extracting text from PDF...")
            pdf_content.seek(0)
            pdf_reader = PdfReader(pdf_content)
            
            text_content = []
            total_pages = len(pdf_reader.pages)
            print(f"Total pages: {total_pages}")
            
            for page_num, page in enumerate(pdf_reader.pages, 1):
                print(f"\r📖 Processing page {page_num}/{total_pages}...", end='')
                page_text = page.extract_text()
                if page_text:
                    text_content.append(f"--- Page {page_num} ---\n{page_text}\n")
            
            print("Text extraction complete!      ")
            INSURANCE_DOCS_CONTENT = "\n".join(text_content)
            
        else:
            # Download as regular file (text, etc.)
            print("Downloading file...")
            request = service.files().get_media(fileId=file_id)
            file_content = io.BytesIO()
            downloader = MediaIoBaseDownload(file_content, request)
            
            done = False
            while not done:
                status, done = downloader.next_chunk()
                if status:
                    print(f"\r Downloading... {int(status.progress() * 100)}%", end='')
            print("\rDownload complete!       ")
            
            file_content.seek(0)
            INSURANCE_DOCS_CONTENT = file_content.read().decode('utf-8', errors='ignore')
        
        print("Successfully loaded document")
        print(f"Total content: {len(INSURANCE_DOCS_CONTENT)} characters")
        
        # Show preview
        if INSURANCE_DOCS_CONTENT:
            preview = INSURANCE_DOCS_CONTENT[:300].replace('\n', ' ')
            print(f"\nPreview: {preview}...\n")
        
        return True
        
    except Exception as e:
        print(f"Error loading docs: {e}")
        import traceback
        traceback.print_exc()
        return False

# MCP Tool - Search insurance documents
@mcp.tool()
def search_insurance_docs(query: str) -> str:
    """
    Search Presidio insurance documents stored in Google Drive.
    Performs keyword-based search on the loaded document content.
    """
    # Fallback to mock data if Google Drive isn't loaded
    if not INSURANCE_DOCS_CONTENT:
        print(" Using mock data - Google Drive content not loaded")
        return _mock_search(query)
    
    # Simple keyword search
    query_lower = query.lower()
    
    # Find sentences containing query terms
    sentences = re.split(r'[.!?\n]+', INSURANCE_DOCS_CONTENT)
    relevant_sentences = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence and any(word in sentence.lower() for word in query_lower.split()):
            relevant_sentences.append(sentence)
    
    if relevant_sentences:
        # Return top 5 most relevant sentences
        result = "\n\n".join(relevant_sentences[:5])
        return f"Found in insurance documents:\n\n{result}"
    else:
        return "No relevant information found in the insurance documents for your query."

def _mock_search(query: str) -> str:
    """Fallback mock search when Google Drive isn't available"""
    query_lower = query.lower()
    
    if "dependent" in query_lower:
        return "Presidio health insurance covers dependents including spouse and children under 26 years of age."
    elif "hospital" in query_lower:
        return "Hospitalization expenses are fully covered under Presidio's health insurance plan with no deductible for in-network facilities."
    elif "health insurance" in query_lower or "benefits" in query_lower or "options" in query_lower:
        return """Presidio offers three health insurance plan options:
        
1. PPO (Preferred Provider Organization): Flexible provider choice with $500 deductible
2. HMO (Health Maintenance Organization): Lower premiums with $250 deductible  
3. HDHP (High Deductible Health Plan): HSA-eligible with $1,500 deductible

All plans include medical, dental, vision coverage, and full hospitalization expense coverage."""
    else:
        return "Presidio provides comprehensive health and life insurance coverage. Please refine your query for specific information."

# FastAPI HTTP Endpoints
class QueryRequest(BaseModel):
    query: str

@app.post("/search")
async def search_endpoint(request: QueryRequest):
    """HTTP endpoint for querying insurance docs"""
    result = search_insurance_docs(request.query)
    return {"result": result}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "docs_loaded": bool(INSURANCE_DOCS_CONTENT),
        "content_length": len(INSURANCE_DOCS_CONTENT)
    }


@app.on_event("startup")
async def startup_event():
    """Load documents on startup"""
    print("=" * 70)
    print("Starting Presidio Insurance MCP Server")
    print("=" * 70)
    load_google_drive_docs()
    print("=" * 70)
    print("Server ready at http://127.0.0.1:8000")
    print(f"Documents loaded: {'Yes' if INSURANCE_DOCS_CONTENT else 'No (using mock data)'}")
    print("=" * 70)

if __name__ == "__main__":
    # Run with uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)