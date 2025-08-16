"""
Application entry point for the AI Outfit Evaluator API
"""

import uvicorn
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.config import API_HOST, API_PORT

def main():
    """Main entry point"""
    # Get port from Cloud Run environment (important for Cloud Run)
    port = int(os.getenv("PORT", API_PORT))
    host = "0.0.0.0"  # Required for Cloud Run
    
    print("🚀 Starting AI Outfit Evaluator API Server...")
    print(f"📁 Project root: {project_root}")
    print(f"🌐 Server will be available at: http://{host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    print("=" * 60)

    # Debug: Show what's in the current directory
    print(f"🔍 Current working directory: {os.getcwd()}")
    print(f"🔍 Files in project root: {list(project_root.iterdir())}")
    
    # Check if app directory exists and show contents
    if (project_root / "app").exists():
        print(f"🔍 Contents of app/: {list((project_root / 'app').iterdir())}")
        if (project_root / "app" / "models").exists():
            print(f"🔍 Contents of app/models/: {list((project_root / 'app' / 'models').iterdir())}")

    # Check if required directories exist
    required_dirs = ['uploads']
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        if not dir_path.exists():
            print(f"📁 Creating directory: {dir_path}")
            dir_path.mkdir(exist_ok=True)
    
    # Check for model file in your actual location
    model_path = project_root / "app" / "best.pt"
    if model_path.exists():
        print(f"✅ Model file found at: {model_path}")
    else:
        print(f"⚠️  WARNING: Model file not found at: {model_path}")
        print("   The API will start but outfit detection will not work.")
        print()
    
    # Set environment variables if not set
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️  WARNING: GEMINI_API_KEY environment variable not set!")
        print("   LLM suggestions will use fallback mode.")
        print("   Set your Gemini API key to enable AI suggestions.")
        print()
    
    try:
        # Determine if this is production (Cloud Run) or development
        is_production = os.getenv("PORT") is not None
        
        # Run the FastAPI app
        uvicorn.run(
            "app.main:app",
            host=host,
            port=port,
            reload=not is_production,  # Disable reload in production
            log_level="info",
            access_log=True
        )
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()