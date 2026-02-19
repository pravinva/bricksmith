"""FastAPI application entry point for Bricksmith web interface."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .api import sessions_router, chat_router, cli_router, results_router
from .services.session_store import get_session_store


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler - initialize and cleanup resources."""
    # Initialize session store (creates tables if needed)
    store = get_session_store()
    await store.initialize()
    yield
    # Cleanup
    await store.close()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Bricksmith Architect",
        description="Web interface for collaborative architecture diagram design",
        version="0.1.0",
        lifespan=lifespan,
    )

    # Configure CORS for local development
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",  # Vite dev server
            "http://localhost:8080",  # Production
            "http://127.0.0.1:5173",
            "http://127.0.0.1:8080",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register API routers
    app.include_router(sessions_router, prefix="/api/sessions", tags=["sessions"])
    app.include_router(chat_router, prefix="/api/sessions", tags=["chat"])
    app.include_router(cli_router, prefix="/api/cli", tags=["cli"])
    app.include_router(results_router, prefix="/api/results", tags=["results"])

    # Serve generated images from outputs directory
    outputs_dir = Path("outputs")
    outputs_dir.mkdir(exist_ok=True)
    app.mount("/api/images", StaticFiles(directory=outputs_dir), name="generated_images")

    # Health check endpoint
    @app.get("/api/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "service": "bricksmith-architect"}

    @app.get("/logo.png")
    async def serve_logo():
        """Serve the Bricksmith app logo."""
        logo_path = Path("logo.png")
        if logo_path.exists():
            return FileResponse(logo_path)
        raise HTTPException(status_code=404, detail="Logo not found")

    # Serve static files (React build) in production
    frontend_dist = Path(__file__).parent.parent.parent.parent / "frontend" / "dist"
    if frontend_dist.exists():
        app.mount("/assets", StaticFiles(directory=frontend_dist / "assets"), name="assets")

        @app.get("/")
        async def serve_index():
            """Serve the React app index.html."""
            return FileResponse(frontend_dist / "index.html")

        @app.get("/{path:path}")
        async def serve_spa(path: str):
            """Serve React app for all non-API routes (SPA fallback)."""
            file_path = frontend_dist / path
            if file_path.exists() and file_path.is_file():
                return FileResponse(file_path)
            return FileResponse(frontend_dist / "index.html")

    return app


# Create app instance for uvicorn
app = create_app()
