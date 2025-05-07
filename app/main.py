# app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
import socket
import os

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
        
        # Get environment information
        env_info = {
            "HOST": os.getenv("HOST", "0.0.0.0"),
            "PORT": os.getenv("PORT", "8051"),
            "PYTHONPATH": os.getenv("PYTHONPATH", ""),
        }
        
        logger.info(f"Client host: {client_host}")
        logger.info(f"Headers: {headers}")
        logger.info(f"Server hostname: {hostname}")
        logger.info(f"Server IP: {ip_address}")
        logger.info(f"Environment: {env_info}")
        
        return {
            "message": "Hello from FastAPI2!",
            "client_host": client_host,
            "headers": headers,
            "server_info": {
                "hostname": hostname,
                "ip_address": ip_address,
                "environment": env_info
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
    # Get port from environment variable or use default
    port = int(os.getenv("PORT", "8051"))
    
    # Log startup information
    logger.info(f"Starting FastAPI application on port {port}")
    logger.info(f"Host: 0.0.0.0")
    logger.info(f"Environment: {dict(os.environ)}")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        proxy_headers=True,
        forwarded_allow_ips="*",
        log_level="debug",
        reload=True
    )
