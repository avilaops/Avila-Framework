"""
AvilaOps | Windows Dev Optimizer
Main Application Entry Point
FastAPI + HTMX + ON Platform Integration
"""

import asyncio
import sys
from pathlib import Path

# Add framework modules to path
FRAMEWORK_DIR = Path(__file__).resolve().parent / "framework"
sys.path.insert(0, str(FRAMEWORK_DIR))

from app.fastapi_framework import create_app
from core.on_integration import get_on_integration

# Import optimization modules
from modules.edge_analyzer import EdgeAnalyzer
from modules.bloatware_remover import BloatwareRemover
from modules.developer_optimizer import DeveloperOptimizer
from modules.program_analyzer import ProgramAnalyzer

def setup_optimization_modules(integration):
    """Register optimization modules with ON integration"""
    
    # Initialize modules
    edge_analyzer = EdgeAnalyzer()
    bloatware_remover = BloatwareRemover()
    developer_optimizer = DeveloperOptimizer()
    program_analyzer = ProgramAnalyzer()
    
    # Register with integration
    integration.register_module("edge_analyzer", edge_analyzer)
    integration.register_module("bloatware_remover", bloatware_remover)
    integration.register_module("developer_optimizer", developer_optimizer)
    integration.register_module("program_analyzer", program_analyzer)
    
    # Full optimization combines all modules
    class FullOptimizationModule:
        async def execute_async(self, parameters):
            results = {}
            
            # Run all optimizations
            if parameters.get("include_edge", True):
                results["edge"] = await edge_analyzer.execute_async(parameters)
            
            if parameters.get("include_bloatware", True):
                results["bloatware"] = await bloatware_remover.execute_async(parameters)
            
            if parameters.get("include_developer", True):
                results["developer"] = await developer_optimizer.execute_async(parameters)
            
            if parameters.get("include_programs", True):
                results["programs"] = await program_analyzer.execute_async(parameters)
            
            return {
                "total_items_processed": sum(r.get("items_processed", 0) for r in results.values()),
                "modules_run": len(results),
                "results_by_module": results
            }
    
    integration.register_module("full_optimization", FullOptimizationModule())
    
    return integration

async def main():
    """Main application entry point"""
    
    print("🚀 Starting Windows Dev Optimizer...")
    print("📊 AvilaOps Framework | Privacy-First Optimization")
    
    try:
        # Attempt to initialize ON integration
        try:
            # Try to connect to ON platform
            on_integration = get_on_integration()
            
            if on_integration.on_available:
                print("🔗 ON Platform connected successfully")
                enable_on_integration = True
            else:
                print("⚠️ ON Platform not available - running in standalone mode")
                enable_on_integration = False
                
        except Exception as e:
            print(f"⚠️ ON Platform initialization failed: {e}")
            print("🔧 Continuing in standalone mode")
            enable_on_integration = False
            on_integration = get_on_integration(bus=None)  # Standalone mode
        
        # Setup optimization modules
        setup_optimization_modules(on_integration)
        print("📦 Optimization modules registered")
        
        # Create FastAPI application
        app = create_app(enable_on_integration=enable_on_integration)
        print("🌐 FastAPI application initialized")
        
        # Print startup information
        print("\n" + "="*60)
        print("🎯 Windows Dev Optimizer Ready!")
        print("="*60)
        print(f"🔧 Framework Version: 1.0.0")
        print(f"🤖 ON Integration: {'Enabled' if enable_on_integration else 'Disabled'}")
        print(f"🛡️ Privacy Mode: Always Active")
        print(f"📡 Web Interface: http://127.0.0.1:8000")
        print(f"📚 API Docs: http://127.0.0.1:8000/api/docs")
        print("="*60)
        print("\n🎮 Available optimizations:")
        print("  • Edge Browser Optimization")
        print("  • Bloatware Removal") 
        print("  • Developer Environment Setup")
        print("  • Program Analysis & Recommendations")
        print("  • Full System Optimization")
        
        if enable_on_integration:
            print("\n🤖 ON Platform Features:")
            print("  • Intelligent routing via Orchestrator")
            print("  • Multi-agent coordination")
            print("  • Advanced semantic analysis")
            print("  • Distributed optimization")
        
        print("\n🌟 Starting web server...")
        print("   Press Ctrl+C to stop\n")
        
        # Start the application
        app.run(host="127.0.0.1", port=8000, debug=False)
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down Windows Dev Optimizer...")
        if 'on_integration' in locals():
            await on_integration.shutdown()
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher required")
        sys.exit(1)
    
    # Run the application
    asyncio.run(main())