"""
AvilaOps | Windows Dev Optimizer
ON Platform Integration Core
Integrates Windows Dev Optimizer with ON Multi-Agent System
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime
import sys

# Add ON core to path
ON_CORE_PATH = Path.home() / "OneDrive" / "Avila" / "AvilaOps" / "ai" / "On" / "core"
if str(ON_CORE_PATH) not in sys.path:
    sys.path.insert(0, str(ON_CORE_PATH))

try:
    from _bootstrap import ensure_on_namespace
    ensure_on_namespace()
    from on.core.on_logger import AgentLogger
    from on.core.on_message import Message, MessageType, MessagePriority
    from on.core.on_telemetry import tracer, meter
    ON_AVAILABLE = True
except ImportError:
    ON_AVAILABLE = False
    print("⚠️ ON Platform not available - running in standalone mode")

@dataclass
class OptimizationRequest:
    """Optimization request structure"""
    request_id: str
    user_id: str
    optimization_type: str  # edge, bloatware, developer, full
    parameters: Dict[str, Any]
    priority: str = "normal"
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

@dataclass
class OptimizationResult:
    """Optimization result structure"""
    request_id: str
    success: bool
    message: str
    data: Dict[str, Any] = None
    execution_time: float = 0.0
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

class ONIntegrationCore:
    """
    Core integration layer between Windows Dev Optimizer and ON Platform
    Handles agent communication, telemetry, and intelligent routing
    """
    
    def __init__(self, bus=None):
        self.name = "WindowsDevOptimizer"
        self.bus = bus
        self.on_available = ON_AVAILABLE and bus is not None
        
        # Initialize logging
        if self.on_available:
            self.logger = AgentLogger(self.name)
        else:
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger(self.name)
            
        # Telemetry setup
        if self.on_available:
            self.requests_counter = meter.create_counter(
                name="windows_optimizer_requests_total",
                description="Total optimization requests processed"
            )
            self.optimization_time = meter.create_histogram(
                name="windows_optimizer_duration_seconds",
                description="Time spent on optimization operations"
            )
        
        # Register with ON bus if available
        if self.on_available:
            self.node = self.bus.register_agent(self.name, self.handle_message)
            self._log("🔗 Integrated with ON Platform")
        else:
            self._log("🔧 Running in standalone mode")
        
        # Optimization modules mapping
        self.modules = {}
        self.active_optimizations = {}
        
    def _log(self, message: str, level: str = "info"):
        """Unified logging"""
        if self.on_available:
            self.logger.log(message)
        else:
            getattr(self.logger, level)(message)
    
    def register_module(self, module_name: str, module_instance):
        """Register optimization module"""
        self.modules[module_name] = module_instance
        self._log(f"📦 Module registered: {module_name}")
    
    async def handle_message(self, message: Message):
        """Handle messages from ON platform"""
        if not self.on_available:
            return
            
        self._log(f"📨 Message from {message.sender}: {message.message_type.value}")
        
        try:
            # Parse message content
            if message.message_type == MessageType.REQUEST:
                await self._handle_optimization_request(message)
            elif message.message_type == MessageType.INFO:
                await self._handle_info_message(message)
            else:
                self._log(f"⚠️ Unhandled message type: {message.message_type}")
                
        except Exception as e:
            self._log(f"❌ Error handling message: {e}", "error")
            if hasattr(self, 'node'):
                self.node.reply(message, f"Error: {str(e)}")
    
    async def _handle_optimization_request(self, message: Message):
        """Handle optimization requests from other agents"""
        try:
            # Parse request
            request_data = json.loads(message.content)
            request = OptimizationRequest(**request_data)
            
            # Route to appropriate module
            result = await self.route_optimization(request)
            
            # Send response back
            if hasattr(self, 'node'):
                response = json.dumps(asdict(result))
                self.node.reply(message, response)
                
        except Exception as e:
            self._log(f"❌ Error processing optimization request: {e}", "error")
            error_result = OptimizationResult(
                request_id=getattr(request, 'request_id', 'unknown'),
                success=False,
                message=f"Error: {str(e)}"
            )
            if hasattr(self, 'node'):
                self.node.reply(message, json.dumps(asdict(error_result)))
    
    async def _handle_info_message(self, message: Message):
        """Handle informational messages"""
        self._log(f"ℹ️ Info from {message.sender}: {message.content}")
    
    async def route_optimization(self, request: OptimizationRequest) -> OptimizationResult:
        """Route optimization request to appropriate module"""
        
        if self.on_available:
            # Record telemetry
            self.requests_counter.add(1, {
                "optimization_type": request.optimization_type,
                "priority": request.priority
            })
        
        start_time = datetime.now()
        
        try:
            # Determine target module
            module_mapping = {
                "edge": "edge_analyzer",
                "bloatware": "bloatware_remover", 
                "developer": "developer_optimizer",
                "programs": "program_analyzer",
                "full": "full_optimization"
            }
            
            target_module = module_mapping.get(request.optimization_type, "full_optimization")
            
            if target_module not in self.modules:
                raise ValueError(f"Module not available: {target_module}")
            
            # Execute optimization
            self._log(f"🎯 Routing {request.optimization_type} to {target_module}")
            
            # Store active optimization
            self.active_optimizations[request.request_id] = {
                "request": request,
                "start_time": start_time,
                "status": "running"
            }
            
            # Execute through module
            module = self.modules[target_module]
            
            if hasattr(module, 'execute_async'):
                result_data = await module.execute_async(request.parameters)
            else:
                # Fallback to sync execution
                result_data = await asyncio.get_event_loop().run_in_executor(
                    None, module.execute, request.parameters
                )
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Record telemetry
            if self.on_available:
                self.optimization_time.record(execution_time, {
                    "optimization_type": request.optimization_type,
                    "success": "true"
                })
            
            # Create result
            result = OptimizationResult(
                request_id=request.request_id,
                success=True,
                message=f"Optimization completed: {request.optimization_type}",
                data=result_data,
                execution_time=execution_time
            )
            
            # Update status
            self.active_optimizations[request.request_id]["status"] = "completed"
            self._log(f"✅ Optimization completed: {request.request_id} ({execution_time:.2f}s)")
            
            return result
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            
            if self.on_available:
                self.optimization_time.record(execution_time, {
                    "optimization_type": request.optimization_type,
                    "success": "false"
                })
            
            self._log(f"❌ Optimization failed: {e}", "error")
            
            return OptimizationResult(
                request_id=request.request_id,
                success=False,
                message=f"Optimization failed: {str(e)}",
                execution_time=execution_time
            )
    
    async def request_agent_assistance(self, agent_name: str, task: str, data: Dict = None):
        """Request assistance from specific ON agent"""
        if not self.on_available:
            self._log("⚠️ ON Platform not available for agent assistance")
            return None
            
        try:
            request_data = {
                "task": task,
                "data": data or {},
                "requester": self.name,
                "timestamp": datetime.now().isoformat()
            }
            
            self.node.send(
                recipient=agent_name,
                content=json.dumps(request_data),
                message_type=MessageType.REQUEST,
                priority=MessagePriority.NORMAL
            )
            
            self._log(f"📤 Requested assistance from {agent_name}: {task}")
            
        except Exception as e:
            self._log(f"❌ Error requesting assistance from {agent_name}: {e}", "error")
    
    async def broadcast_status(self, status: str, data: Dict = None):
        """Broadcast status to all ON agents"""
        if not self.on_available:
            return
            
        try:
            status_data = {
                "agent": self.name,
                "status": status,
                "data": data or {},
                "timestamp": datetime.now().isoformat()
            }
            
            self.node.broadcast(
                content=json.dumps(status_data),
                priority=MessagePriority.LOW
            )
            
            self._log(f"📡 Broadcasted status: {status}")
            
        except Exception as e:
            self._log(f"❌ Error broadcasting status: {e}", "error")
    
    def get_optimization_status(self, request_id: str) -> Optional[Dict]:
        """Get status of active optimization"""
        return self.active_optimizations.get(request_id)
    
    def get_active_optimizations(self) -> List[Dict]:
        """Get all active optimizations"""
        return list(self.active_optimizations.values())
    
    async def shutdown(self):
        """Graceful shutdown"""
        if self.on_available and hasattr(self, 'node'):
            await self.broadcast_status("shutting_down")
        
        self._log("👋 ON Integration shutting down")

# Singleton instance
_integration_instance = None

def get_on_integration(bus=None) -> ONIntegrationCore:
    """Get singleton ON integration instance"""
    global _integration_instance
    if _integration_instance is None:
        _integration_instance = ONIntegrationCore(bus)
    return _integration_instance

# Example usage
if __name__ == "__main__":
    async def main():
        # Test integration
        integration = get_on_integration()
        
        # Test optimization request
        test_request = OptimizationRequest(
            request_id="test_001",
            user_id="test_user",
            optimization_type="edge",
            parameters={"deep_scan": True}
        )
        
        print("Testing optimization routing...")
        # This would normally be called by a registered module
        # result = await integration.route_optimization(test_request)
        # print(f"Result: {result}")
        
    asyncio.run(main())