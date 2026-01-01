"""Privacy-respecting analytics for ESHU usage patterns

Collects ONLY aggregate, non-PII data:
- Package manager usage stats
- Search patterns (popular packages)
- Error patterns and recovery success
- Performance metrics

NO user identification, NO IP addresses, NO personal data
"""

import sqlite3
import json
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime
from dataclasses import dataclass


@dataclass
class AnalyticsEvent:
    """Represents an analytics event"""
    event_type: str  # search, install_success, install_failure, error_recovery, etc.
    package_name: str
    package_manager: str
    distro: str
    distro_version: str
    metadata: Dict
    timestamp: str


class Analytics:
    """Privacy-respecting analytics collection"""

    def __init__(self, db_path: Path, enabled: bool = True):
        self.db_path = db_path
        self.enabled = enabled

        if self.enabled:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self._initialize_db()

    def _initialize_db(self):
        """Create analytics tables"""
        with sqlite3.connect(self.db_path) as conn:
            # Search events
            conn.execute("""
                CREATE TABLE IF NOT EXISTS searches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    package_name TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)

            # Installation events
            conn.execute("""
                CREATE TABLE IF NOT EXISTS installations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    package_name TEXT NOT NULL,
                    package_manager TEXT NOT NULL,
                    distro TEXT NOT NULL,
                    distro_version TEXT NOT NULL,
                    success BOOLEAN NOT NULL,
                    duration_seconds REAL,
                    timestamp TEXT NOT NULL
                )
            """)

            # Error events
            conn.execute("""
                CREATE TABLE IF NOT EXISTS errors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    package_name TEXT NOT NULL,
                    package_manager TEXT NOT NULL,
                    distro TEXT NOT NULL,
                    error_type TEXT NOT NULL,
                    error_message TEXT,
                    recovery_attempted BOOLEAN DEFAULT 0,
                    recovery_successful BOOLEAN DEFAULT 0,
                    timestamp TEXT NOT NULL
                )
            """)

            # Package manager usage
            conn.execute("""
                CREATE TABLE IF NOT EXISTS manager_usage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    package_manager TEXT NOT NULL,
                    operation TEXT NOT NULL,
                    success BOOLEAN NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)

            # Performance metrics
            conn.execute("""
                CREATE TABLE IF NOT EXISTS performance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation TEXT NOT NULL,
                    duration_seconds REAL NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)

            # Create indices
            conn.execute("CREATE INDEX IF NOT EXISTS idx_searches_pkg ON searches(package_name)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_installs_pkg ON installations(package_name)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_installs_mgr ON installations(package_manager)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_errors_type ON errors(error_type)")

            conn.commit()

    def track_search(self, package_name: str):
        """Track package search"""
        if not self.enabled:
            return

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO searches (package_name, timestamp)
                VALUES (?, ?)
            """, (package_name.lower(), datetime.now().isoformat()))
            conn.commit()

    def track_installation(self, package_name: str, package_manager: str,
                          distro: str, distro_version: str,
                          success: bool, duration_seconds: Optional[float] = None):
        """Track installation attempt"""
        if not self.enabled:
            return

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO installations
                (package_name, package_manager, distro, distro_version, success, duration_seconds, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                package_name.lower(),
                package_manager,
                distro,
                distro_version,
                success,
                duration_seconds,
                datetime.now().isoformat()
            ))
            conn.commit()

    def track_error(self, package_name: str, package_manager: str, distro: str,
                   error_type: str, error_message: Optional[str] = None,
                   recovery_attempted: bool = False, recovery_successful: bool = False):
        """Track installation error"""
        if not self.enabled:
            return

        # Truncate error message to avoid storing too much data
        if error_message and len(error_message) > 500:
            error_message = error_message[:500] + "..."

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO errors
                (package_name, package_manager, distro, error_type, error_message,
                 recovery_attempted, recovery_successful, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                package_name.lower(),
                package_manager,
                distro,
                error_type,
                error_message,
                recovery_attempted,
                recovery_successful,
                datetime.now().isoformat()
            ))
            conn.commit()

    def track_manager_usage(self, package_manager: str, operation: str, success: bool):
        """Track package manager operation"""
        if not self.enabled:
            return

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO manager_usage (package_manager, operation, success, timestamp)
                VALUES (?, ?, ?, ?)
            """, (package_manager, operation, success, datetime.now().isoformat()))
            conn.commit()

    def track_performance(self, operation: str, duration_seconds: float):
        """Track operation performance"""
        if not self.enabled:
            return

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO performance (operation, duration_seconds, timestamp)
                VALUES (?, ?, ?)
            """, (operation, duration_seconds, datetime.now().isoformat()))
            conn.commit()

    # Analytics queries

    def get_popular_searches(self, limit: int = 20) -> List[tuple]:
        """Get most searched packages"""
        if not self.enabled:
            return []

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT package_name, COUNT(*) as search_count
                FROM searches
                WHERE timestamp > datetime('now', '-30 days')
                GROUP BY package_name
                ORDER BY search_count DESC
                LIMIT ?
            """, (limit,))
            return cursor.fetchall()

    def get_manager_stats(self) -> Dict:
        """Get package manager usage statistics"""
        if not self.enabled:
            return {}

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT
                    package_manager,
                    COUNT(*) as total_uses,
                    SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successes,
                    AVG(duration_seconds) as avg_duration
                FROM installations
                WHERE timestamp > datetime('now', '-30 days')
                GROUP BY package_manager
                ORDER BY total_uses DESC
            """)

            return {
                row[0]: {
                    "total_uses": row[1],
                    "successes": row[2],
                    "success_rate": round((row[2] / row[1] * 100) if row[1] > 0 else 0, 2),
                    "avg_duration": round(row[3], 2) if row[3] else 0
                }
                for row in cursor.fetchall()
            }

    def get_error_patterns(self, limit: int = 10) -> List[Dict]:
        """Get most common error patterns"""
        if not self.enabled:
            return []

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT
                    error_type,
                    package_manager,
                    distro,
                    COUNT(*) as occurrence_count,
                    SUM(CASE WHEN recovery_successful = 1 THEN 1 ELSE 0 END) as recovery_success_count
                FROM errors
                WHERE timestamp > datetime('now', '-30 days')
                GROUP BY error_type, package_manager, distro
                ORDER BY occurrence_count DESC
                LIMIT ?
            """, (limit,))

            return [
                {
                    "error_type": row[0],
                    "package_manager": row[1],
                    "distro": row[2],
                    "occurrences": row[3],
                    "recovery_success_count": row[4],
                    "recovery_rate": round((row[4] / row[3] * 100) if row[3] > 0 else 0, 2)
                }
                for row in cursor.fetchall()
            ]

    def get_failure_hotspots(self) -> List[Dict]:
        """Get packages/managers with highest failure rates"""
        if not self.enabled:
            return []

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT
                    package_name,
                    package_manager,
                    distro,
                    COUNT(*) as total_attempts,
                    SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) as failures
                FROM installations
                WHERE timestamp > datetime('now', '-30 days')
                GROUP BY package_name, package_manager, distro
                HAVING total_attempts >= 5
                ORDER BY (CAST(failures AS FLOAT) / total_attempts) DESC
                LIMIT 20
            """)

            return [
                {
                    "package": row[0],
                    "manager": row[1],
                    "distro": row[2],
                    "attempts": row[3],
                    "failures": row[4],
                    "failure_rate": round((row[4] / row[3] * 100), 2)
                }
                for row in cursor.fetchall()
            ]

    def get_summary_stats(self) -> Dict:
        """Get overall summary statistics"""
        if not self.enabled:
            return {}

        with sqlite3.connect(self.db_path) as conn:
            # Total searches
            searches = conn.execute("SELECT COUNT(*) FROM searches").fetchone()[0]

            # Total installations
            installs = conn.execute("SELECT COUNT(*) FROM installations").fetchone()[0]

            # Success rate
            success_rate_row = conn.execute("""
                SELECT
                    AVG(CASE WHEN success = 1 THEN 100.0 ELSE 0.0 END)
                FROM installations
            """).fetchone()
            success_rate = round(success_rate_row[0], 2) if success_rate_row[0] else 0

            # Total errors
            errors = conn.execute("SELECT COUNT(*) FROM errors").fetchone()[0]

            # Error recovery rate
            recovery_row = conn.execute("""
                SELECT
                    AVG(CASE WHEN recovery_successful = 1 THEN 100.0 ELSE 0.0 END)
                FROM errors
                WHERE recovery_attempted = 1
            """).fetchone()
            recovery_rate = round(recovery_row[0], 2) if recovery_row[0] else 0

            return {
                "total_searches": searches,
                "total_installations": installs,
                "overall_success_rate": success_rate,
                "total_errors": errors,
                "error_recovery_rate": recovery_rate
            }

    def export_aggregated_data(self) -> Dict:
        """Export all aggregated data (for potential monetization/sharing)"""
        if not self.enabled:
            return {}

        return {
            "summary": self.get_summary_stats(),
            "popular_searches": self.get_popular_searches(50),
            "manager_stats": self.get_manager_stats(),
            "error_patterns": self.get_error_patterns(50),
            "failure_hotspots": self.get_failure_hotspots(),
            "exported_at": datetime.now().isoformat()
        }
