#!/usr/bin/env python3
# File: StartAndyGoogle.py
# Path: AndyGoogle/StartAndyGoogle.py
# Standard: AIDEV-PascalCase-2.1
# Created: 2025-07-12
# Last Modified: 2025-07-12  07:40PM
"""
Description: AndyGoogle startup script with smart port detection and environment checks
Main entry point for the AndyGoogle cloud-synchronized digital library system
"""

import os
import sys
import json
import socket
import subprocess
import argparse
from datetime import datetime

class AndyGoogleStarter:
    """Smart startup manager for AndyGoogle"""
    
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(self.script_dir, "Config", "andygoogle_config.json")
        self.config = self.load_config()
        
    def load_config(self):
        """Load AndyGoogle configuration"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            else:
                print(f"⚠️ Config file not found: {self.config_path}")
                return {}
        except Exception as e:
            print(f"⚠️ Error loading config: {e}")
            return {}
    
    def check_environment(self):
        """Check if the environment is ready for AndyGoogle"""
        issues = []
        
        # Check Python version
        if sys.version_info < (3, 8):
            issues.append(f"Python 3.8+ required (current: {sys.version})")
        
        # Check required directories
        required_dirs = [
            "Source/API",
            "Source/Core", 
            "Source/Utils",
            "WebPages",
            "Data/Local",
            "Data/Logs",
            "Config"
        ]
        
        for dir_path in required_dirs:
            full_path = os.path.join(self.script_dir, dir_path)
            if not os.path.exists(full_path):
                issues.append(f"Missing directory: {dir_path}")
        
        # Check required Python packages
        required_packages = [
            'fastapi',
            'uvicorn',
            'google-auth',
            'google-auth-oauthlib', 
            'google-api-python-client',
            'pydantic'
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                if package == 'google-auth':
                    import google.auth
                elif package == 'google-auth-oauthlib':
                    import google_auth_oauthlib
                elif package == 'google-api-python-client':
                    import googleapiclient
                else:
                    __import__(package.replace('-', '_'))
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            issues.append(f"Missing Python packages: {', '.join(missing_packages)}")
        
        # Check Google credentials
        credentials_path = self.config.get('google_credentials_path', 'Config/google_credentials.json')
        full_credentials_path = os.path.join(self.script_dir, credentials_path)
        if not os.path.exists(full_credentials_path):
            issues.append(f"Google credentials not found: {full_credentials_path}")
        
        return issues
    
    def find_available_port(self, start_port=8000, max_attempts=20):
        """Find an available port starting from start_port"""
        print(f"🔍 Searching for available port starting from {start_port}...")
        
        for port in range(start_port, start_port + max_attempts):
            try:
                test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                test_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                test_socket.bind(('127.0.0.1', port))
                test_socket.close()
                
                if port != start_port:
                    print(f"✅ Found available port: {port} (port {start_port} was busy)")
                
                return port
                
            except OSError as e:
                # Identify common port conflicts
                if port == 8000:
                    print(f"⚠️ Port 8000 busy (common causes: HP printer service, other web servers)")
                elif port == 8080:
                    print(f"⚠️ Port 8080 busy (common causes: Tomcat, Jenkins, proxy servers)")
                elif port == 3000:
                    print(f"⚠️ Port 3000 busy (common causes: Node.js development servers)")
                
                # Try to identify what's using the port
                self.identify_port_user(port)
                continue
        
        return None
    
    def identify_port_user(self, port):
        """Try to identify what process is using a port"""
        try:
            # Try netstat first (more widely available)
            result = subprocess.run(['netstat', '-tlnp', '2>/dev/null'], 
                                  capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if f':{port} ' in line:
                        parts = line.split()
                        if len(parts) >= 7:
                            process_info = parts[6] if '/' in parts[6] else 'unknown'
                            print(f"   └─ Used by: {process_info}")
                            return
            
            # Fallback to lsof if available
            result = subprocess.run(['lsof', '-i', f':{port}'], 
                                  capture_output=True, text=True)
            if result.returncode == 0 and result.stdout:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:  # Skip header
                    process_info = lines[1].split()[0]
                    print(f"   └─ Used by: {process_info}")
        except (FileNotFoundError, subprocess.SubprocessError):
            pass
    
    def check_port_conflicts(self, port):
        """Check what might be using a port"""
        try:
            # Try to identify what's using the port
            result = subprocess.run(['lsof', '-i', f':{port}'], 
                                  capture_output=True, text=True)
            if result.returncode == 0 and result.stdout:
                print(f"ℹ️ Port {port} is being used by:")
                print(result.stdout)
        except FileNotFoundError:
            # lsof not available
            pass
    
    def start_server(self, host="127.0.0.1", port=None, check_only=False):
        """Start the AndyGoogle server"""
        
        # Environment check
        print("🔍 Checking environment...")
        issues = self.check_environment()
        
        if issues:
            print("❌ Environment issues found:")
            for issue in issues:
                print(f"   • {issue}")
            
            if check_only:
                return False
            
            print("\nTo fix these issues:")
            print("1. Install missing packages: pip install fastapi uvicorn google-auth google-auth-oauthlib google-api-python-client pydantic")
            print("2. Set up Google API credentials in Config/google_credentials.json")
            print("3. Ensure all required directories exist")
            return False
        
        if check_only:
            print("✅ Environment check passed!")
            return True
        
        # Find available port
        if port is None:
            port = self.config.get('server_port', 8000)
        
        # Try user-specified port first
        available_port = self.find_available_port(port)
        
        # If that fails, try the configured port range
        if available_port is None:
            print(f"⚠️ Could not find available port starting from {port}")
            port_range = self.config.get('server_port_range', [8001, 8002, 8003, 8080, 8090, 3000, 5000, 9000])
            
            print(f"🔄 Trying alternative ports: {port_range}")
            for alt_port in port_range:
                if alt_port != port:  # Don't retry the same port
                    available_port = self.find_available_port(alt_port, max_attempts=1)
                    if available_port:
                        break
        
        if available_port is None:
            print("❌ Could not find any available port!")
            print("💡 Try these solutions:")
            print("   1. Stop other web servers (Apache, Nginx, etc.)")
            print("   2. Use a specific port: python StartAndyGoogle.py --port 8888")
            print("   3. Check what's using ports: netstat -tlnp | grep LISTEN")
            return False
        
        if available_port != port:
            print(f"ℹ️ Port {port} unavailable, using port {available_port} instead")
        
        # Set up environment
        os.chdir(self.script_dir)
        sys.path.insert(0, self.script_dir)
        
        print("🚀 Starting AndyGoogle...")
        print(f"📍 Working directory: {self.script_dir}")
        print(f"🌐 Server URL: http://{host}:{available_port}")
        print(f"📚 Library interface: http://{host}:{available_port}")
        print(f"🔧 API docs: http://{host}:{available_port}/docs")
        print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Import and start the FastAPI app
        try:
            from Source.API.MainAPI import app
            import uvicorn
            
            uvicorn.run(
                app,
                host=host,
                port=available_port,
                log_level="info",
                access_log=True
            )
            
        except KeyboardInterrupt:
            print("\n👋 AndyGoogle server stopped by user")
            return True
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            return False

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="AndyGoogle - Cloud-synchronized digital library",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python StartAndyGoogle.py                    # Start with smart port detection
  python StartAndyGoogle.py --port 8080       # Force specific port
  python StartAndyGoogle.py --port 3000       # Use alternative port (good for development)
  python StartAndyGoogle.py --check           # Check environment only
  python StartAndyGoogle.py --host 0.0.0.0    # Allow external connections

Port Selection:
  AndyGoogle automatically finds available ports starting from 8000.
  Common alternatives: 8001, 8002, 8080, 8090, 3000, 5000, 9000
  If port 8000 is busy (HP printer service), it will try the next available port.
        """
    )
    
    parser.add_argument('--host', default='127.0.0.1', 
                       help='Host to bind to (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=None,
                       help='Port to use (default: from config or 8000)')
    parser.add_argument('--check', action='store_true',
                       help='Check environment and exit')
    
    args = parser.parse_args()
    
    print("🚀 AndyGoogle - Cloud Library System")
    print("=" * 60)
    
    starter = AndyGoogleStarter()
    success = starter.start_server(
        host=args.host,
        port=args.port,
        check_only=args.check
    )
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()