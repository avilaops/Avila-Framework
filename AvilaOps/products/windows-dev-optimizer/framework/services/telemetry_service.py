"""
AvilaOps | Windows Dev Optimizer
Privacy-First Telemetry Service
Secure, Anonymous Usage Analytics
"""

import asyncio
import json
import hashlib
import hmac
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, List
from pathlib import Path
import sqlite3
from dataclasses import dataclass, asdict
from cryptography.fernet import Fernet
import uuid

@dataclass
class TelemetryEvent:
    """Privacy-safe telemetry event"""
    event_id: str
    event_type: str  # request, optimization, error, system
    timestamp: str
    duration: float = 0.0
    status: str = "success"
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class PrivacyTelemetry:
    """
    Privacy-first telemetry system with:
    - Anonymous data collection
    - Local storage only
    - Automatic data expiration
    - No personal identifiable information
    - Encrypted storage
    """
    
    def __init__(self, 
                 db_path: str = None,
                 retention_days: int = 7,
                 encryption_key: str = None):
        
        self.retention_days = retention_days
        
        # Setup database
        if db_path is None:
            db_path = Path.home() / "OneDrive" / "Avila" / "AvilaOps" / "products" / \
                     "windows-dev-optimizer" / "logs" / "telemetry.db"
        
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Setup encryption
        if encryption_key is None:
            key_file = self.db_path.parent / ".telemetry_key"
            if key_file.exists():
                encryption_key = key_file.read_text().strip()
            else:
                encryption_key = Fernet.generate_key().decode()
                key_file.write_text(encryption_key)
                key_file.chmod(0o600)  # Restrict permissions
        
        self.cipher = Fernet(encryption_key.encode())
        
        # Initialize database
        self._init_database()
        
        # Setup cleanup task
        self._last_cleanup = datetime.now()
        
    def _init_database(self):
        """Initialize telemetry database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS telemetry_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id TEXT UNIQUE,
                    event_type TEXT,
                    timestamp TEXT,
                    duration REAL,
                    status TEXT,
                    encrypted_metadata BLOB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp ON telemetry_events(timestamp)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_event_type ON telemetry_events(event_type)
            """)
    
    async def record_request(self,
                           request_id: str,
                           endpoint: str,
                           method: str,
                           status_code: int,
                           duration: float,
                           user_agent_hash: str = None):
        """Record HTTP request telemetry"""
        
        # Privacy-safe metadata (no IP, no personal data)
        metadata = {
            "endpoint_hash": self._hash_endpoint(endpoint),
            "method": method,
            "status_code": status_code,
            "user_agent_hash": user_agent_hash[:8] if user_agent_hash else None,  # Truncated
        }
        
        event = TelemetryEvent(
            event_id=request_id,
            event_type="request",
            timestamp=datetime.now(timezone.utc).isoformat(),
            duration=duration,
            status="success" if 200 <= status_code < 400 else "error",
            metadata=metadata
        )
        
        await self._store_event(event)
    
    async def record_optimization(self,
                                optimization_id: str,
                                optimization_type: str,
                                duration: float,
                                success: bool,
                                items_processed: int = 0,
                                errors_count: int = 0):
        """Record optimization telemetry"""
        
        metadata = {
            "optimization_type": optimization_type,
            "items_processed": items_processed,
            "errors_count": errors_count,
        }
        
        event = TelemetryEvent(
            event_id=optimization_id,
            event_type="optimization",
            timestamp=datetime.now(timezone.utc).isoformat(),
            duration=duration,
            status="success" if success else "error",
            metadata=metadata
        )
        
        await self._store_event(event)
    
    async def record_error(self,
                          request_id: str,
                          endpoint: str,
                          error_type: str,
                          duration: float):
        """Record error telemetry"""
        
        metadata = {
            "endpoint_hash": self._hash_endpoint(endpoint),
            "error_type": error_type,
        }
        
        event = TelemetryEvent(
            event_id=request_id,
            event_type="error",
            timestamp=datetime.now(timezone.utc).isoformat(),
            duration=duration,
            status="error",
            metadata=metadata
        )
        
        await self._store_event(event)
    
    async def record_system_event(self,
                                 event_name: str,
                                 details: Dict[str, Any] = None):
        """Record system event"""
        
        event = TelemetryEvent(
            event_id=str(uuid.uuid4()),
            event_type="system",
            timestamp=datetime.now(timezone.utc).isoformat(),
            duration=0.0,
            status="info",
            metadata={"event_name": event_name, **(details or {})}
        )
        
        await self._store_event(event)
    
    async def _store_event(self, event: TelemetryEvent):
        """Store telemetry event securely"""
        
        try:
            # Encrypt metadata
            metadata_json = json.dumps(event.metadata or {})
            encrypted_metadata = self.cipher.encrypt(metadata_json.encode())
            
            # Store in database
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO telemetry_events 
                    (event_id, event_type, timestamp, duration, status, encrypted_metadata)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    event.event_id,
                    event.event_type,
                    event.timestamp,
                    event.duration,
                    event.status,
                    encrypted_metadata
                ))
            
            # Periodic cleanup
            if (datetime.now() - self._last_cleanup).total_seconds() > 3600:  # Every hour
                await self._cleanup_old_data()
                
        except Exception as e:
            # Silent fail for telemetry - never break the main application
            print(f"Telemetry storage error (non-critical): {e}")
    
    async def get_summary(self, days: int = 7) -> Dict[str, Any]:
        """Get privacy-safe telemetry summary"""
        
        try:
            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            with sqlite3.connect(self.db_path) as conn:
                # Request summary
                requests = conn.execute("""
                    SELECT status, COUNT(*) as count, AVG(duration) as avg_duration
                    FROM telemetry_events
                    WHERE event_type = 'request' AND timestamp > ?
                    GROUP BY status
                """, (cutoff_date,)).fetchall()
                
                # Optimization summary
                optimizations = conn.execute("""
                    SELECT status, COUNT(*) as count, AVG(duration) as avg_duration
                    FROM telemetry_events
                    WHERE event_type = 'optimization' AND timestamp > ?
                    GROUP BY status
                """, (cutoff_date,)).fetchall()
                
                # Error summary
                errors = conn.execute("""
                    SELECT COUNT(*) as count
                    FROM telemetry_events
                    WHERE event_type = 'error' AND timestamp > ?
                """, (cutoff_date,)).fetchone()
                
                # Most recent events
                recent_events = conn.execute("""
                    SELECT event_type, status, timestamp, duration
                    FROM telemetry_events
                    WHERE timestamp > ?
                    ORDER BY timestamp DESC
                    LIMIT 10
                """, (cutoff_date,)).fetchall()
            
            return {
                "period_days": days,
                "requests": {row[0]: {"count": row[1], "avg_duration": row[2]} for row in requests},
                "optimizations": {row[0]: {"count": row[1], "avg_duration": row[2]} for row in optimizations},
                "errors": {"count": errors[0] if errors else 0},
                "recent_events": [
                    {
                        "type": row[0],
                        "status": row[1], 
                        "timestamp": row[2],
                        "duration": row[3]
                    } for row in recent_events
                ],
                "privacy_note": "All data is anonymized and stored locally only"
            }
            
        except Exception as e:
            return {"error": f"Could not retrieve telemetry summary: {e}"}
    
    async def get_optimization_stats(self) -> Dict[str, Any]:
        """Get optimization-specific statistics"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Decrypt and analyze optimization metadata
                optimization_events = conn.execute("""
                    SELECT encrypted_metadata, status, duration
                    FROM telemetry_events
                    WHERE event_type = 'optimization'
                    ORDER BY timestamp DESC
                    LIMIT 100
                """).fetchall()
                
                stats = {
                    "total_optimizations": len(optimization_events),
                    "success_rate": 0,
                    "avg_duration": 0,
                    "by_type": {},
                    "total_items_processed": 0
                }
                
                if optimization_events:
                    successful = 0
                    total_duration = 0
                    total_items = 0
                    
                    for encrypted_meta, status, duration in optimization_events:
                        if status == "success":
                            successful += 1
                        total_duration += duration
                        
                        # Decrypt metadata
                        try:
                            metadata_json = self.cipher.decrypt(encrypted_meta).decode()
                            metadata = json.loads(metadata_json)
                            
                            opt_type = metadata.get("optimization_type", "unknown")
                            items = metadata.get("items_processed", 0)
                            
                            if opt_type not in stats["by_type"]:
                                stats["by_type"][opt_type] = {"count": 0, "avg_duration": 0}
                            
                            stats["by_type"][opt_type]["count"] += 1
                            stats["by_type"][opt_type]["avg_duration"] += duration
                            
                            total_items += items
                            
                        except Exception:
                            # Skip corrupted metadata
                            pass
                    
                    stats["success_rate"] = (successful / len(optimization_events)) * 100
                    stats["avg_duration"] = total_duration / len(optimization_events)
                    stats["total_items_processed"] = total_items
                    
                    # Calculate averages
                    for opt_type in stats["by_type"]:
                        count = stats["by_type"][opt_type]["count"]
                        stats["by_type"][opt_type]["avg_duration"] /= count
                
                return stats
                
        except Exception as e:
            return {"error": f"Could not retrieve optimization stats: {e}"}
    
    async def _cleanup_old_data(self):
        """Remove old telemetry data"""
        
        try:
            cutoff_date = (datetime.now() - timedelta(days=self.retention_days)).isoformat()
            
            with sqlite3.connect(self.db_path) as conn:
                deleted = conn.execute("""
                    DELETE FROM telemetry_events
                    WHERE timestamp < ?
                """, (cutoff_date,)).rowcount
                
                # Vacuum database to reclaim space
                conn.execute("VACUUM")
            
            self._last_cleanup = datetime.now()
            
            if deleted > 0:
                await self.record_system_event("telemetry_cleanup", {"deleted_events": deleted})
                
        except Exception as e:
            print(f"Telemetry cleanup error (non-critical): {e}")
    
    def _hash_endpoint(self, endpoint: str) -> str:
        """Create privacy-safe hash of endpoint"""
        # Remove parameters and keep only path structure
        clean_endpoint = endpoint.split('?')[0]
        return hashlib.sha256(clean_endpoint.encode()).hexdigest()[:12]
    
    async def export_data(self, output_file: str = None) -> str:
        """Export telemetry data for analysis"""
        
        if output_file is None:
            output_file = f"telemetry_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            summary = await self.get_summary(days=self.retention_days)
            optimization_stats = await self.get_optimization_stats()
            
            export_data = {
                "export_timestamp": datetime.now(timezone.utc).isoformat(),
                "privacy_statement": "This data contains no personal identifiable information",
                "retention_policy": f"{self.retention_days} days",
                "summary": summary,
                "optimization_stats": optimization_stats
            }
            
            output_path = Path(output_file)
            with open(output_path, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            return str(output_path)
            
        except Exception as e:
            raise Exception(f"Could not export telemetry data: {e}")
    
    async def clear_all_data(self):
        """Clear all telemetry data (for privacy compliance)"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                deleted = conn.execute("DELETE FROM telemetry_events").rowcount
                conn.execute("VACUUM")
            
            await self.record_system_event("telemetry_cleared", {"deleted_events": deleted})
            return deleted
            
        except Exception as e:
            raise Exception(f"Could not clear telemetry data: {e}")

# Example usage
if __name__ == "__main__":
    async def main():
        telemetry = PrivacyTelemetry()
        
        # Record some test events
        await telemetry.record_request(
            request_id="test_001",
            endpoint="/api/optimize",
            method="POST",
            status_code=200,
            duration=0.5,
            user_agent_hash="chrome_hash"
        )
        
        await telemetry.record_optimization(
            optimization_id="opt_001",
            optimization_type="edge",
            duration=120.5,
            success=True,
            items_processed=15,
            errors_count=0
        )
        
        # Get summary
        summary = await telemetry.get_summary()
        print("Telemetry Summary:")
        print(json.dumps(summary, indent=2))
        
        # Get optimization stats
        opt_stats = await telemetry.get_optimization_stats()
        print("\nOptimization Stats:")
        print(json.dumps(opt_stats, indent=2))
    
    asyncio.run(main())