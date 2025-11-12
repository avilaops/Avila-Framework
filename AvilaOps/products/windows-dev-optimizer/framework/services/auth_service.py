"""
AvilaOps | Windows Dev Optimizer
Authentication & Session Management Services
Privacy-Focused User Management
"""

import hashlib
import hmac
import secrets
import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional
from pathlib import Path
import json
from cryptography.fernet import Fernet
from fastapi import Request, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

class AuthService:
    """
    Privacy-focused authentication service
    - Anonymous session management
    - No personal data storage
    - Local-only authentication
    """
    
    def __init__(self, secret_key: str = None):
        if secret_key is None:
            # Generate or load secret key
            key_file = Path.home() / "OneDrive" / "Avila" / "AvilaOps" / \
                      "products" / "windows-dev-optimizer" / "config" / ".secret_key"
            key_file.parent.mkdir(parents=True, exist_ok=True)
            
            if key_file.exists():
                secret_key = key_file.read_text().strip()
            else:
                secret_key = secrets.token_urlsafe(32)
                key_file.write_text(secret_key)
                key_file.chmod(0o600)
        
        self.secret_key = secret_key.encode()
        self.security = HTTPBasic()
    
    def create_session_token(self, user_identifier: str = None) -> str:
        """Create anonymous session token"""
        if user_identifier is None:
            user_identifier = f"anon_{secrets.token_hex(8)}"
        
        # Create secure session token
        timestamp = str(int(datetime.now(timezone.utc).timestamp()))
        payload = f"{user_identifier}:{timestamp}"
        
        signature = hmac.new(
            self.secret_key,
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return f"{payload}:{signature}"
    
    def validate_session_token(self, token: str) -> Dict[str, Any]:
        """Validate and decode session token"""
        try:
            parts = token.split(':')
            if len(parts) != 3:
                raise ValueError("Invalid token format")
            
            user_id, timestamp, signature = parts
            payload = f"{user_id}:{timestamp}"
            
            # Verify signature
            expected_signature = hmac.new(
                self.secret_key,
                payload.encode(),
                hashlib.sha256
            ).hexdigest()
            
            if not hmac.compare_digest(signature, expected_signature):
                raise ValueError("Invalid signature")
            
            # Check expiration (24 hours)
            token_time = datetime.fromtimestamp(int(timestamp), tz=timezone.utc)
            if datetime.now(timezone.utc) - token_time > timedelta(hours=24):
                raise ValueError("Token expired")
            
            return {
                "user_id": user_id,
                "created_at": token_time,
                "valid": True
            }
            
        except Exception as e:
            return {
                "valid": False,
                "error": str(e)
            }
    
    def create_api_key(self, purpose: str = "api_access") -> str:
        """Create API key for external access"""
        prefix = "wdo"  # Windows Dev Optimizer
        key_id = secrets.token_hex(4)
        secret = secrets.token_urlsafe(32)
        
        return f"{prefix}_{key_id}_{secret}"
    
    def validate_api_key(self, api_key: str) -> bool:
        """Validate API key (basic validation)"""
        if not api_key:
            return False
        
        parts = api_key.split('_')
        return len(parts) == 3 and parts[0] == "wdo"
    
    async def authenticate_request(self, request: Request) -> Optional[str]:
        """Authenticate request and return user ID"""
        
        # Check for API key
        api_key = request.headers.get("X-API-Key")
        if api_key and self.validate_api_key(api_key):
            return f"api_user_{api_key[:8]}"
        
        # Check for session token
        session_token = request.cookies.get("session_token")
        if session_token:
            validation = self.validate_session_token(session_token)
            if validation["valid"]:
                return validation["user_id"]
        
        # Return None for anonymous access
        return None

class SessionService:
    """
    Privacy-focused session management
    - Minimal data storage
    - Automatic cleanup
    - Anonymous tracking
    """
    
    def __init__(self):
        self.auth = AuthService()
        self.sessions_dir = Path.home() / "OneDrive" / "Avila" / "AvilaOps" / \
                           "products" / "windows-dev-optimizer" / "logs" / "sessions"
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup encryption for session data
        key_file = self.sessions_dir / ".session_key"
        if key_file.exists():
            encryption_key = key_file.read_text().strip()
        else:
            encryption_key = Fernet.generate_key().decode()
            key_file.write_text(encryption_key)
            key_file.chmod(0o600)
        
        self.cipher = Fernet(encryption_key.encode())
    
    async def get_or_create_session(self, request: Request) -> str:
        """Get existing session or create new one"""
        
        # Try to get existing session
        session_token = request.cookies.get("session_token")
        if session_token:
            validation = self.auth.validate_session_token(session_token)
            if validation["valid"]:
                return validation["user_id"]
        
        # Create new session
        session_id = f"session_{uuid.uuid4().hex[:12]}"
        session_token = self.auth.create_session_token(session_id)
        
        # Store minimal session data
        await self._store_session_data(session_id, {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "last_activity": datetime.now(timezone.utc).isoformat(),
            "request_count": 0
        })
        
        return session_id
    
    async def update_session_activity(self, session_id: str):
        """Update session last activity"""
        session_data = await self._load_session_data(session_id)
        if session_data:
            session_data["last_activity"] = datetime.now(timezone.utc).isoformat()
            session_data["request_count"] = session_data.get("request_count", 0) + 1
            await self._store_session_data(session_id, session_data)
    
    async def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session information"""
        return await self._load_session_data(session_id)
    
    async def cleanup_expired_sessions(self):
        """Remove expired sessions"""
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=24)
        
        for session_file in self.sessions_dir.glob("*.json"):
            try:
                session_data = await self._load_session_data(session_file.stem)
                if session_data:
                    last_activity = datetime.fromisoformat(
                        session_data["last_activity"].replace("Z", "+00:00")
                    )
                    if last_activity < cutoff_time:
                        session_file.unlink()  # Delete expired session
            except Exception:
                # Delete corrupted session files
                session_file.unlink()
    
    async def _store_session_data(self, session_id: str, data: Dict[str, Any]):
        """Store encrypted session data"""
        try:
            # Encrypt session data
            data_json = json.dumps(data)
            encrypted_data = self.cipher.encrypt(data_json.encode())
            
            # Store to file
            session_file = self.sessions_dir / f"{session_id}.json"
            session_file.write_bytes(encrypted_data)
            
        except Exception as e:
            print(f"Session storage error (non-critical): {e}")
    
    async def _load_session_data(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load encrypted session data"""
        try:
            session_file = self.sessions_dir / f"{session_id}.json"
            if not session_file.exists():
                return None
            
            # Decrypt session data
            encrypted_data = session_file.read_bytes()
            data_json = self.cipher.decrypt(encrypted_data).decode()
            
            return json.loads(data_json)
            
        except Exception as e:
            print(f"Session load error (non-critical): {e}")
            return None
    
    def create_session_cookie(self, session_token: str) -> Dict[str, Any]:
        """Create session cookie parameters"""
        return {
            "key": "session_token",
            "value": session_token,
            "max_age": 86400,  # 24 hours
            "httponly": True,
            "secure": False,  # Set to True in production with HTTPS
            "samesite": "lax"
        }

class RateLimitService:
    """
    Simple rate limiting for API protection
    """
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 3600):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, List[datetime]] = {}
    
    def check_rate_limit(self, client_id: str) -> bool:
        """Check if client is within rate limit"""
        now = datetime.now(timezone.utc)
        window_start = now - timedelta(seconds=self.window_seconds)
        
        # Initialize or clean up old requests
        if client_id not in self.requests:
            self.requests[client_id] = []
        
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if req_time > window_start
        ]
        
        # Check limit
        if len(self.requests[client_id]) >= self.max_requests:
            return False
        
        # Add current request
        self.requests[client_id].append(now)
        return True
    
    def get_rate_limit_info(self, client_id: str) -> Dict[str, Any]:
        """Get rate limit information for client"""
        if client_id not in self.requests:
            return {
                "remaining": self.max_requests,
                "reset_time": datetime.now(timezone.utc) + timedelta(seconds=self.window_seconds)
            }
        
        remaining = max(0, self.max_requests - len(self.requests[client_id]))
        
        # Find oldest request to determine reset time
        if self.requests[client_id]:
            oldest_request = min(self.requests[client_id])
            reset_time = oldest_request + timedelta(seconds=self.window_seconds)
        else:
            reset_time = datetime.now(timezone.utc) + timedelta(seconds=self.window_seconds)
        
        return {
            "remaining": remaining,
            "reset_time": reset_time
        }

# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def main():
        # Test authentication
        auth = AuthService()
        
        # Create session token
        token = auth.create_session_token("test_user")
        print(f"Session token: {token}")
        
        # Validate token
        validation = auth.validate_session_token(token)
        print(f"Validation: {validation}")
        
        # Test session service
        session_service = SessionService()
        
        # Simulate request (would normally come from FastAPI)
        class MockRequest:
            def __init__(self):
                self.cookies = {}
        
        request = MockRequest()
        session_id = await session_service.get_or_create_session(request)
        print(f"Session ID: {session_id}")
        
        # Test rate limiting
        rate_limiter = RateLimitService(max_requests=5, window_seconds=60)
        
        for i in range(7):
            allowed = rate_limiter.check_rate_limit("test_client")
            print(f"Request {i+1}: {'Allowed' if allowed else 'Rate limited'}")
        
        rate_info = rate_limiter.get_rate_limit_info("test_client")
        print(f"Rate limit info: {rate_info}")
    
    asyncio.run(main())