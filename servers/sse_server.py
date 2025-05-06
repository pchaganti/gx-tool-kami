from typing import List, Optional
import logging
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Mount, Route
from starlette.responses import JSONResponse
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_starlette_app(
    mcp_server: Server,
    *,
    debug: bool = False,
    health_check: bool = True,
    cors_origins: Optional[List[str]] = None
) -> Starlette:
    """Create a Starlette application that can serve the provided mcp server with SSE.
    
    Args:
        mcp_server: The MCP server instance to serve
        debug: Whether to run in debug mode
        health_check: Whether to add a health check endpoint
        cors_origins: List of allowed CORS origins, or None to disable CORS
    """
    sse = SseServerTransport("/messages/")

    async def handle_sse(request: Request) -> None:
        async with sse.connect_sse(
                request.scope,
                request.receive,
                request._send,  # noqa: SLF001
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )

    # Add CORS middleware if origins are specified
    middleware = []
    if cors_origins is not None:
        middleware.append(
            Middleware(
                CORSMiddleware,
                allow_origins=cors_origins,
                allow_methods=["*"],
                allow_headers=["*"],
            )
        )

    # Define routes
    routes = [
        Route("/sse", endpoint=handle_sse),
        Mount("/messages/", app=sse.handle_post_message),
    ]

    # Add health check if requested
    if health_check:
        async def health_check_endpoint(request: Request) -> JSONResponse:
            return JSONResponse({"status": "healthy"})
        routes.insert(0, Route("/health", endpoint=health_check_endpoint))

    return Starlette(
        debug=debug,
        middleware=middleware,
        routes=routes,
    ) 