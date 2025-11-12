"""
AvilaOps | Windows Dev Optimizer
FastAPI + HTMX Web Framework
Privacy-First Telemetry & ON Platform Integration
"""

import asyncio
import json
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path

# FastAPI and web framework imports
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import uvicorn

# HTMX support
from fastapi.responses import Response as FastAPIResponse

# Privacy and security
from cryptography.fernet import Fernet
import hashlib
import hmac

# Local imports
from ..core.on_integration import get_on_integration, OptimizationRequest, OptimizationResult
from ..services.telemetry_service import PrivacyTelemetry
from ..services.auth_service import AuthService
from ..services.session_service import SessionService

class FastAPIFramework:
    """
    Privacy-first FastAPI framework with HTMX integration and ON platform connectivity
    """
    
    def __init__(self, 
                 title: str = "Windows Dev Optimizer",
                 version: str = "1.0.0",
                 enable_on_integration: bool = True):
        
        # Initialize FastAPI app
        self.app = FastAPI(
            title=title,
            version=version,
            description="Privacy-first Windows optimization with ON platform integration",
            docs_url="/api/docs" if enable_on_integration else None,
            redoc_url="/api/redoc" if enable_on_integration else None
        )
        
        # Configuration
        self.enable_on_integration = enable_on_integration
        self.base_dir = Path(__file__).resolve().parents[2]
        self.templates_dir = self.base_dir / "templates"
        self.static_dir = self.base_dir / "framework" / "output"
        
        # Initialize services
        self.telemetry = PrivacyTelemetry()
        self.auth = AuthService()
        self.sessions = SessionService()
        
        # ON Platform integration
        if enable_on_integration:
            self.on_integration = get_on_integration()
        else:
            self.on_integration = None
        
        # Setup middleware and routes
        self._setup_middleware()
        self._setup_templates()
        self._setup_routes()
        
        # Active optimization tracking
        self.active_optimizations: Dict[str, Dict] = {}
        
    def _setup_middleware(self):
        """Configure middleware stack"""
        
        # CORS for development
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE"],
            allow_headers=["*"],
        )
        
        # Compression
        self.app.add_middleware(GZipMiddleware, minimum_size=1000)
        
        # Custom privacy middleware
        @self.app.middleware("http")
        async def privacy_middleware(request: Request, call_next):
            # Generate request ID
            request_id = str(uuid.uuid4())
            request.state.request_id = request_id
            
            # Record request telemetry (privacy-safe)
            start_time = datetime.now(timezone.utc)
            
            try:
                response = await call_next(request)
                
                # Record successful request
                duration = (datetime.now(timezone.utc) - start_time).total_seconds()
                await self.telemetry.record_request(
                    request_id=request_id,
                    endpoint=request.url.path,
                    method=request.method,
                    status_code=response.status_code,
                    duration=duration,
                    user_agent_hash=self._hash_user_agent(request.headers.get("user-agent", ""))
                )
                
                return response
                
            except Exception as e:
                # Record error
                duration = (datetime.now(timezone.utc) - start_time).total_seconds()
                await self.telemetry.record_error(
                    request_id=request_id,
                    endpoint=request.url.path,
                    error_type=type(e).__name__,
                    duration=duration
                )
                raise
    
    def _setup_templates(self):
        """Configure Jinja2 templates with HTMX support"""
        self.templates = Jinja2Templates(directory=str(self.templates_dir))
        
        # Add HTMX helper functions
        self.templates.env.globals.update({
            'htmx_request': self._is_htmx_request,
            'htmx_partial': self._render_htmx_partial,
            'optimization_status': self._get_optimization_status,
            'format_duration': self._format_duration
        })
    
    def _setup_routes(self):
        """Setup all application routes"""
        
        # Static files
        self.app.mount("/static", StaticFiles(directory=str(self.static_dir)), name="static")
        
        # Main routes
        self._setup_main_routes()
        self._setup_api_routes()
        self._setup_htmx_routes()
        
        if self.enable_on_integration:
            self._setup_on_routes()
    
    def _setup_main_routes(self):
        """Main application routes"""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def dashboard(request: Request):
            """Main dashboard"""
            session_id = await self.sessions.get_or_create_session(request)
            
            # Get system status
            system_status = await self._get_system_status()
            
            # Get recent optimizations
            recent_optimizations = list(self.active_optimizations.values())[-5:]
            
            return self.templates.TemplateResponse("dashboard.html", {
                "request": request,
                "session_id": session_id,
                "system_status": system_status,
                "recent_optimizations": recent_optimizations,
                "on_integration_enabled": self.enable_on_integration
            })
        
        @self.app.get("/optimize", response_class=HTMLResponse)
        async def optimize_page(request: Request):
            """Optimization selection page"""
            session_id = await self.sessions.get_or_create_session(request)
            
            optimization_types = [
                {
                    "id": "edge",
                    "name": "Edge Browser Optimization",
                    "description": "Analyze and optimize Microsoft Edge configuration",
                    "icon": "🌐",
                    "estimated_time": "2-5 minutes"
                },
                {
                    "id": "bloatware", 
                    "name": "Bloatware Removal",
                    "description": "Remove unnecessary pre-installed software",
                    "icon": "🗑️",
                    "estimated_time": "5-10 minutes"
                },
                {
                    "id": "developer",
                    "name": "Developer Environment",
                    "description": "Optimize for development workflows",
                    "icon": "💻",
                    "estimated_time": "3-7 minutes"
                },
                {
                    "id": "programs",
                    "name": "Program Analysis",
                    "description": "Analyze installed programs and recommendations",
                    "icon": "📊",
                    "estimated_time": "1-3 minutes"
                }
            ]
            
            return self.templates.TemplateResponse("optimize.html", {
                "request": request,
                "session_id": session_id,
                "optimization_types": optimization_types
            })
        
        @self.app.get("/status", response_class=HTMLResponse)
        async def status_page(request: Request):
            """System status and monitoring"""
            session_id = await self.sessions.get_or_create_session(request)
            
            # Get telemetry summary
            telemetry_summary = await self.telemetry.get_summary()
            
            # Get ON platform status
            on_status = None
            if self.enable_on_integration and self.on_integration:
                on_status = {
                    "connected": self.on_integration.on_available,
                    "active_optimizations": len(self.on_integration.get_active_optimizations()),
                    "registered_modules": len(self.on_integration.modules)
                }
            
            return self.templates.TemplateResponse("status.html", {
                "request": request,
                "session_id": session_id,
                "telemetry": telemetry_summary,
                "on_status": on_status
            })
    
    def _setup_api_routes(self):
        """API routes for optimization operations"""
        
        @self.app.post("/api/optimize")
        async def start_optimization(
            request: Request,
            background_tasks: BackgroundTasks,
            optimization_data: Dict[str, Any]
        ):
            """Start optimization process"""
            
            try:
                # Validate session
                session_id = await self.sessions.get_or_create_session(request)
                
                # Create optimization request
                optimization_id = str(uuid.uuid4())
                opt_request = OptimizationRequest(
                    request_id=optimization_id,
                    user_id=session_id,
                    optimization_type=optimization_data.get("type", "full"),
                    parameters=optimization_data.get("parameters", {}),
                    priority=optimization_data.get("priority", "normal")
                )
                
                # Track optimization
                self.active_optimizations[optimization_id] = {
                    "request": opt_request,
                    "status": "queued",
                    "start_time": datetime.now(),
                    "progress": 0
                }
                
                # Start optimization in background
                if self.enable_on_integration and self.on_integration:
                    background_tasks.add_task(
                        self._execute_optimization_with_on,
                        opt_request
                    )
                else:
                    background_tasks.add_task(
                        self._execute_optimization_standalone,
                        opt_request
                    )
                
                return JSONResponse({
                    "success": True,
                    "optimization_id": optimization_id,
                    "message": "Optimization started",
                    "estimated_time": "5-10 minutes"
                })
                
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/optimize/{optimization_id}/status")
        async def get_optimization_status(optimization_id: str):
            """Get optimization status"""
            
            optimization = self.active_optimizations.get(optimization_id)
            if not optimization:
                raise HTTPException(status_code=404, detail="Optimization not found")
            
            return JSONResponse({
                "optimization_id": optimization_id,
                "status": optimization["status"],
                "progress": optimization.get("progress", 0),
                "start_time": optimization["start_time"].isoformat(),
                "duration": (datetime.now() - optimization["start_time"]).total_seconds(),
                "result": optimization.get("result")
            })
        
        @self.app.get("/api/system/status")
        async def get_system_status():
            """Get system status"""
            return JSONResponse(await self._get_system_status())
        
        @self.app.get("/api/telemetry/summary") 
        async def get_telemetry_summary():
            """Get privacy-safe telemetry summary"""
            return JSONResponse(await self.telemetry.get_summary())
    
    def _setup_htmx_routes(self):
        """HTMX-specific routes for dynamic content"""
        
        @self.app.get("/htmx/optimization-status/{optimization_id}")
        async def htmx_optimization_status(request: Request, optimization_id: str):
            """HTMX partial for optimization status"""
            
            optimization = self.active_optimizations.get(optimization_id)
            if not optimization:
                return HTMLResponse("<div class='error'>Optimization not found</div>")
            
            return self.templates.TemplateResponse("partials/optimization_status.html", {
                "request": request,
                "optimization": optimization,
                "optimization_id": optimization_id
            })
        
        @self.app.get("/htmx/system-status")
        async def htmx_system_status(request: Request):
            """HTMX partial for system status"""
            
            system_status = await self._get_system_status()
            
            return self.templates.TemplateResponse("partials/system_status.html", {
                "request": request,
                "system_status": system_status
            })
        
        @self.app.post("/htmx/start-optimization")
        async def htmx_start_optimization(request: Request, background_tasks: BackgroundTasks):
            """HTMX endpoint to start optimization"""
            
            form_data = await request.form()
            optimization_type = form_data.get("optimization_type")
            
            if not optimization_type:
                return HTMLResponse("<div class='error'>No optimization type specified</div>")
            
            # Create and start optimization
            optimization_id = str(uuid.uuid4())
            session_id = await self.sessions.get_or_create_session(request)
            
            opt_request = OptimizationRequest(
                request_id=optimization_id,
                user_id=session_id,
                optimization_type=optimization_type,
                parameters=dict(form_data)
            )
            
            self.active_optimizations[optimization_id] = {
                "request": opt_request,
                "status": "starting",
                "start_time": datetime.now(),
                "progress": 0
            }
            
            # Start background task
            if self.enable_on_integration and self.on_integration:
                background_tasks.add_task(self._execute_optimization_with_on, opt_request)
            else:
                background_tasks.add_task(self._execute_optimization_standalone, opt_request)
            
            # Return HTMX partial with status
            return self.templates.TemplateResponse("partials/optimization_started.html", {
                "request": request,
                "optimization_id": optimization_id,
                "optimization_type": optimization_type
            })
    
    def _setup_on_routes(self):
        """ON Platform integration routes"""
        
        @self.app.get("/api/on/agents")
        async def get_on_agents():
            """Get connected ON agents"""
            if not self.on_integration or not self.on_integration.on_available:
                return JSONResponse({"error": "ON Platform not available"})
            
            # This would query the ON platform for available agents
            agents = [
                "atlas", "helix", "sigma", "vox", "lumen", 
                "forge", "lex", "echo", "orchestrator"
            ]
            
            return JSONResponse({"agents": agents})
        
        @self.app.post("/api/on/request-assistance")
        async def request_on_assistance(assistance_data: Dict[str, Any]):
            """Request assistance from ON agent"""
            if not self.on_integration or not self.on_integration.on_available:
                raise HTTPException(status_code=503, detail="ON Platform not available")
            
            agent_name = assistance_data.get("agent")
            task = assistance_data.get("task")
            data = assistance_data.get("data", {})
            
            if not agent_name or not task:
                raise HTTPException(status_code=400, detail="Agent name and task required")
            
            await self.on_integration.request_agent_assistance(agent_name, task, data)
            
            return JSONResponse({
                "success": True,
                "message": f"Assistance requested from {agent_name}"
            })
    
    async def _execute_optimization_with_on(self, request: OptimizationRequest):
        """Execute optimization using ON platform"""
        
        try:
            # Update status
            self.active_optimizations[request.request_id]["status"] = "running"
            
            # Route through ON integration
            result = await self.on_integration.route_optimization(request)
            
            # Update final status
            self.active_optimizations[request.request_id].update({
                "status": "completed" if result.success else "failed",
                "result": result,
                "progress": 100,
                "end_time": datetime.now()
            })
            
        except Exception as e:
            self.active_optimizations[request.request_id].update({
                "status": "failed",
                "error": str(e),
                "end_time": datetime.now()
            })
    
    async def _execute_optimization_standalone(self, request: OptimizationRequest):
        """Execute optimization in standalone mode"""
        
        try:
            # Update status
            self.active_optimizations[request.request_id]["status"] = "running"
            
            # Simulate optimization (replace with actual module calls)
            for i in range(0, 101, 10):
                await asyncio.sleep(0.5)  # Simulate work
                self.active_optimizations[request.request_id]["progress"] = i
            
            # Create mock result
            result = OptimizationResult(
                request_id=request.request_id,
                success=True,
                message=f"Standalone optimization completed: {request.optimization_type}",
                data={"items_processed": 42, "improvements_found": 7},
                execution_time=5.0
            )
            
            # Update final status
            self.active_optimizations[request.request_id].update({
                "status": "completed",
                "result": result,
                "progress": 100,
                "end_time": datetime.now()
            })
            
        except Exception as e:
            self.active_optimizations[request.request_id].update({
                "status": "failed", 
                "error": str(e),
                "end_time": datetime.now()
            })
    
    async def _get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return {
            "timestamp": datetime.now().isoformat(),
            "framework_version": "1.0.0",
            "on_integration": {
                "enabled": self.enable_on_integration,
                "connected": self.on_integration.on_available if self.on_integration else False,
                "active_optimizations": len(self.on_integration.get_active_optimizations()) if self.on_integration else 0
            },
            "telemetry": {
                "privacy_mode": True,
                "data_retention_days": 7
            },
            "system": {
                "active_optimizations": len(self.active_optimizations),
                "uptime": "running"
            }
        }
    
    def _hash_user_agent(self, user_agent: str) -> str:
        """Create privacy-safe hash of user agent"""
        return hashlib.sha256(user_agent.encode()).hexdigest()[:16]
    
    def _is_htmx_request(self, request: Request) -> bool:
        """Check if request is from HTMX"""
        return request.headers.get("HX-Request") == "true"
    
    def _render_htmx_partial(self, template_name: str, context: Dict) -> str:
        """Render HTMX partial template"""
        # This would be used in templates
        pass
    
    def _get_optimization_status(self, optimization_id: str) -> Optional[Dict]:
        """Template helper for optimization status"""
        return self.active_optimizations.get(optimization_id)
    
    def _format_duration(self, seconds: float) -> str:
        """Format duration for display"""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}m"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}h"
    
    def run(self, host: str = "127.0.0.1", port: int = 8000, debug: bool = False):
        """Run the FastAPI application"""
        uvicorn.run(
            self.app,
            host=host,
            port=port,
            reload=debug,
            log_level="info" if not debug else "debug"
        )

# Factory function
def create_app(enable_on_integration: bool = True) -> FastAPIFramework:
    """Create FastAPI framework instance"""
    return FastAPIFramework(enable_on_integration=enable_on_integration)

# Example usage
if __name__ == "__main__":
    app = create_app(enable_on_integration=True)
    app.run(debug=True)