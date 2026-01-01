"""Bundle database for caching and sharing Eshu's Path bundles"""

import sqlite3
import json
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Bundle:
    """Represents a package bundle"""
    package_name: str
    distro: str
    distro_version: str
    bundle_data: Dict
    ai_generated: bool
    created_at: str
    usage_count: int = 0
    success_count: int = 0
    failure_count: int = 0

    @property
    def success_rate(self) -> float:
        """Calculate success rate"""
        total = self.success_count + self.failure_count
        if total == 0:
            return 0.0
        return (self.success_count / total) * 100


class BundleDatabase:
    """Manages bundle storage and retrieval"""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_db()

    def _initialize_db(self):
        """Create database tables if they don't exist"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS bundles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    package_name TEXT NOT NULL,
                    distro TEXT NOT NULL,
                    distro_version TEXT NOT NULL,
                    bundle_json TEXT NOT NULL,
                    ai_generated BOOLEAN NOT NULL,
                    created_at TEXT NOT NULL,
                    usage_count INTEGER DEFAULT 0,
                    success_count INTEGER DEFAULT 0,
                    failure_count INTEGER DEFAULT 0,
                    UNIQUE(package_name, distro, distro_version)
                )
            """)

            # Create index for fast lookups
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_package_lookup
                ON bundles(package_name, distro, distro_version)
            """)

            conn.commit()

    def get_bundle(self, package_name: str, distro: str, distro_version: str) -> Optional[Bundle]:
        """Retrieve a bundle from cache"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT package_name, distro, distro_version, bundle_json,
                       ai_generated, created_at, usage_count, success_count, failure_count
                FROM bundles
                WHERE package_name = ? AND distro = ? AND distro_version = ?
            """, (package_name.lower(), distro.lower(), distro_version))

            row = cursor.fetchone()
            if row:
                return Bundle(
                    package_name=row[0],
                    distro=row[1],
                    distro_version=row[2],
                    bundle_data=json.loads(row[3]),
                    ai_generated=bool(row[4]),
                    created_at=row[5],
                    usage_count=row[6],
                    success_count=row[7],
                    failure_count=row[8]
                )

        return None

    def save_bundle(self, package_name: str, distro: str, distro_version: str,
                   bundle_data: Dict, ai_generated: bool = True):
        """Save a bundle to cache"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO bundles
                (package_name, distro, distro_version, bundle_json, ai_generated, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                package_name.lower(),
                distro.lower(),
                distro_version,
                json.dumps(bundle_data),
                ai_generated,
                datetime.now().isoformat()
            ))
            conn.commit()

    def increment_usage(self, package_name: str, distro: str, distro_version: str):
        """Track bundle usage"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE bundles
                SET usage_count = usage_count + 1
                WHERE package_name = ? AND distro = ? AND distro_version = ?
            """, (package_name.lower(), distro.lower(), distro_version))
            conn.commit()

    def record_success(self, package_name: str, distro: str, distro_version: str):
        """Record successful bundle installation"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE bundles
                SET success_count = success_count + 1
                WHERE package_name = ? AND distro = ? AND distro_version = ?
            """, (package_name.lower(), distro.lower(), distro_version))
            conn.commit()

    def record_failure(self, package_name: str, distro: str, distro_version: str):
        """Record failed bundle installation"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE bundles
                SET failure_count = failure_count + 1
                WHERE package_name = ? AND distro = ? AND distro_version = ?
            """, (package_name.lower(), distro.lower(), distro_version))
            conn.commit()

    def get_popular_bundles(self, limit: int = 10) -> List[Bundle]:
        """Get most popular bundles"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT package_name, distro, distro_version, bundle_json,
                       ai_generated, created_at, usage_count, success_count, failure_count
                FROM bundles
                ORDER BY usage_count DESC
                LIMIT ?
            """, (limit,))

            return [
                Bundle(
                    package_name=row[0],
                    distro=row[1],
                    distro_version=row[2],
                    bundle_data=json.loads(row[3]),
                    ai_generated=bool(row[4]),
                    created_at=row[5],
                    usage_count=row[6],
                    success_count=row[7],
                    failure_count=row[8]
                )
                for row in cursor.fetchall()
            ]

    def get_stats(self) -> Dict:
        """Get database statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT
                    COUNT(*) as total_bundles,
                    SUM(usage_count) as total_uses,
                    SUM(ai_generated) as ai_generated_count,
                    AVG(CAST(success_count AS FLOAT) / NULLIF(success_count + failure_count, 0) * 100) as avg_success_rate
                FROM bundles
            """)

            row = cursor.fetchone()
            return {
                "total_bundles": row[0] or 0,
                "total_uses": row[1] or 0,
                "ai_generated_count": row[2] or 0,
                "curated_count": (row[0] or 0) - (row[2] or 0),
                "avg_success_rate": round(row[3] or 0, 2)
            }
