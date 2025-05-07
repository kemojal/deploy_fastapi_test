# app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
import socket

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    logger.info(f"Headers: {request.headers}")
    try:
        response = await call_next(request)
        logger.info(f"Response status: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@app.get("/")
async def read_root(request: Request):
    try:
        # Get client IP and headers for debugging
        client_host = request.client.host if request.client else "unknown"
        headers = dict(request.headers)
        
        # Get server information
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        
        logger.info(f"Client host: {client_host}")
        logger.info(f"Headers: {headers}")
        logger.info(f"Server hostname: {hostname}")
        logger.info(f"Server IP: {ip_address}")
        
        return {
            "message": "Hello from FastAPI2!",
            "client_host": client_host,
            "headers": headers,
            "server_info": {
                "hostname": hostname,
                "ip_address": ip_address
            },
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error in root endpoint: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8051,  # Changed to match the port we're using
        proxy_headers=True,
        forwarded_allow_ips="*",
        log_level="debug",
        reload=True  # Enable auto-reload for debugging
    )
