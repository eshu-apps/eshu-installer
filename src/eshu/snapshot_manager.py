"""Snapshot manager for system rollback support (Btrfs/Timeshift integration)"""

import subprocess
import shutil
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime
from dataclasses import dataclass
import json


@dataclass
class Snapshot:
    """Represents a system snapshot"""
    id: str
    timestamp: str
    description: str
    backend: str  # "btrfs", "timeshift", or "manual"
    size_mb: Optional[float] = None


class SnapshotManager:
    """Manages system snapshots for safe rollback"""
    
    def __init__(self, cache_dir: Path = None):
        if cache_dir is None:
            cache_dir = Path.home() / ".cache" / "eshu"
        self.cache_dir = cache_dir
        self.snapshots_file = cache_dir / "snapshots.json"
        self.backend = self._detect_backend()
    
    def _detect_backend(self) -> Optional[str]:
        """Detect available snapshot backend"""
        # Check for Timeshift (most user-friendly)
        if shutil.which("timeshift"):
            return "timeshift"
        
        # Check for Btrfs
        try:
            result = subprocess.run(
                ["findmnt", "-n", "-o", "FSTYPE", "/"],
                capture_output=True,
                text=True,
                check=True
            )
            if "btrfs" in result.stdout.lower():
                return "btrfs"
        except Exception:
            pass
        
        return None
    
    def is_available(self) -> bool:
        """Check if snapshot functionality is available"""
        return self.backend is not None
    
    def create_snapshot(self, description: str = "ESHU pre-install snapshot") -> Optional[Snapshot]:
        """Create a system snapshot before installation"""
        if not self.is_available():
            return None
        
        try:
            if self.backend == "timeshift":
                return self._create_timeshift_snapshot(description)
            elif self.backend == "btrfs":
                return self._create_btrfs_snapshot(description)
        except Exception as e:
            print(f"Failed to create snapshot: {e}")
            return None
    
    def _create_timeshift_snapshot(self, description: str) -> Optional[Snapshot]:
        """Create snapshot using Timeshift"""
        try:
            # Create snapshot with comment
            result = subprocess.run(
                ["sudo", "timeshift", "--create", "--comments", description, "--scripted"],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                # Parse output to get snapshot ID
                snapshot_id = None
                for line in result.stdout.split("\n"):
                    if "Tagged snapshot" in line:
                        # Extract ID from output
                        parts = line.split("'")
                        if len(parts) >= 2:
                            snapshot_id = parts[1]
                            break
                
                if not snapshot_id:
                    # Fallback: use timestamp
                    snapshot_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                
                snapshot = Snapshot(
                    id=snapshot_id,
                    timestamp=datetime.now().isoformat(),
                    description=description,
                    backend="timeshift"
                )
                
                self._save_snapshot_record(snapshot)
                return snapshot
        
        except subprocess.TimeoutExpired:
            print("Snapshot creation timed out")
        except Exception as e:
            print(f"Timeshift snapshot failed: {e}")
        
        return None
    
    def _create_btrfs_snapshot(self, description: str) -> Optional[Snapshot]:
        """Create snapshot using Btrfs"""
        try:
            # Create snapshot directory if it doesn't exist
            snapshot_dir = Path("/snapshots")
            if not snapshot_dir.exists():
                subprocess.run(
                    ["sudo", "mkdir", "-p", str(snapshot_dir)],
                    check=True
                )
            
            # Generate snapshot name
            snapshot_name = f"eshu_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            snapshot_path = snapshot_dir / snapshot_name
            
            # Create read-only snapshot
            result = subprocess.run(
                ["sudo", "btrfs", "subvolume", "snapshot", "-r", "/", str(snapshot_path)],
                capture_output=True,
                text=True,
                check=True
            )
            
            if result.returncode == 0:
                snapshot = Snapshot(
                    id=snapshot_name,
                    timestamp=datetime.now().isoformat(),
                    description=description,
                    backend="btrfs"
                )
                
                self._save_snapshot_record(snapshot)
                return snapshot
        
        except Exception as e:
            print(f"Btrfs snapshot failed: {e}")
        
        return None
    
    def _save_snapshot_record(self, snapshot: Snapshot):
        """Save snapshot record to cache"""
        records = self._load_snapshot_records()
        records.append({
            "id": snapshot.id,
            "timestamp": snapshot.timestamp,
            "description": snapshot.description,
            "backend": snapshot.backend,
            "size_mb": snapshot.size_mb
        })
        
        # Keep only last 10 snapshots
        records = records[-10:]
        
        with open(self.snapshots_file, 'w') as f:
            json.dump(records, f, indent=2)
    
    def _load_snapshot_records(self) -> List[Dict]:
        """Load snapshot records from cache"""
        if not self.snapshots_file.exists():
            return []
        
        try:
            with open(self.snapshots_file) as f:
                return json.load(f)
        except Exception:
            return []
    
    def list_snapshots(self) -> List[Snapshot]:
        """List available snapshots"""
        records = self._load_snapshot_records()
        return [
            Snapshot(
                id=r["id"],
                timestamp=r["timestamp"],
                description=r["description"],
                backend=r["backend"],
                size_mb=r.get("size_mb")
            )
            for r in records
        ]
    
    def restore_snapshot(self, snapshot_id: str) -> bool:
        """Restore a snapshot (requires user confirmation)"""
        if self.backend == "timeshift":
            return self._restore_timeshift_snapshot(snapshot_id)
        elif self.backend == "btrfs":
            return self._restore_btrfs_snapshot(snapshot_id)
        return False
    
    def _restore_timeshift_snapshot(self, snapshot_id: str) -> bool:
        """Restore using Timeshift"""
        try:
            print(f"⚠️  WARNING: This will restore your system to snapshot {snapshot_id}")
            print("⚠️  This operation requires a reboot and cannot be undone!")
            
            result = subprocess.run(
                ["sudo", "timeshift", "--restore", "--snapshot", snapshot_id, "--scripted"],
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )
            
            return result.returncode == 0
        
        except Exception as e:
            print(f"Restore failed: {e}")
            return False
    
    def _restore_btrfs_snapshot(self, snapshot_id: str) -> bool:
        """Restore using Btrfs (requires manual intervention)"""
        snapshot_path = Path("/snapshots") / snapshot_id
        
        print(f"⚠️  To restore Btrfs snapshot {snapshot_id}:")
        print(f"1. Boot from live USB")
        print(f"2. Mount your Btrfs filesystem")
        print(f"3. Run: sudo btrfs subvolume delete /@")
        print(f"4. Run: sudo btrfs subvolume snapshot {snapshot_path} /@")
        print(f"5. Reboot")
        
        return False  # Manual process
    
    def delete_snapshot(self, snapshot_id: str) -> bool:
        """Delete a snapshot"""
        try:
            if self.backend == "timeshift":
                result = subprocess.run(
                    ["sudo", "timeshift", "--delete", "--snapshot", snapshot_id],
                    capture_output=True,
                    text=True,
                    check=True
                )
                return result.returncode == 0
            
            elif self.backend == "btrfs":
                snapshot_path = Path("/snapshots") / snapshot_id
                result = subprocess.run(
                    ["sudo", "btrfs", "subvolume", "delete", str(snapshot_path)],
                    capture_output=True,
                    text=True,
                    check=True
                )
                return result.returncode == 0
        
        except Exception as e:
            print(f"Delete failed: {e}")
            return False
        
        return False
