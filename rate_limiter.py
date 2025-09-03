"""
Rate limiting utilities for the Interactive Button Application
"""
import time
import logging
from collections import defaultdict, deque
from threading import Lock
from typing import Dict, Deque

logger = logging.getLogger(__name__)

class RateLimiter:
    """Rate limiting class to prevent spam clicking and abuse"""
    
    def __init__(self, max_requests_per_minute: int = 600):
        self.max_requests = max_requests_per_minute
        self.requests: Dict[str, Deque[float]] = defaultdict(deque)
        self.lock = Lock()
        self.warning_counts = defaultdict(int)
    
    def is_allowed(self, client_id: str) -> bool:
        """
        Check if a request from the given client is allowed based on rate limiting
        
        Args:
            client_id: Unique identifier for the client
            
        Returns:
            True if request is allowed, False if rate limited
        """
        with self.lock:
            current_time = time.time()
            client_requests = self.requests[client_id]
            
            # Remove requests older than 1 minute
            while client_requests and current_time - client_requests[0] > 60:
                client_requests.popleft()
            
            # Check if under rate limit
            if len(client_requests) < self.max_requests:
                client_requests.append(current_time)
                return True
            else:
                # Log rate limiting
                self.warning_counts[client_id] += 1
                if self.warning_counts[client_id] % 10 == 1:  # Log every 10th violation
                    logger.warning(f"Rate limit exceeded for client {client_id} "
                                 f"({len(client_requests)} requests in last minute)")
                return False
    
    def get_remaining_requests(self, client_id: str) -> int:
        """Get remaining requests for a client in the current minute"""
        with self.lock:
            current_time = time.time()
            client_requests = self.requests[client_id]
            
            # Clean old requests
            while client_requests and current_time - client_requests[0] > 60:
                client_requests.popleft()
            
            return max(0, self.max_requests - len(client_requests))
    
    def cleanup_old_entries(self):
        """Clean up old client entries to prevent memory leaks"""
        with self.lock:
            current_time = time.time()
            clients_to_remove = []
            
            for client_id, client_requests in self.requests.items():
                # Remove requests older than 1 minute
                while client_requests and current_time - client_requests[0] > 60:
                    client_requests.popleft()
                
                # If no recent requests, mark for removal
                if not client_requests:
                    clients_to_remove.append(client_id)
            
            # Remove empty client entries
            for client_id in clients_to_remove:
                del self.requests[client_id]
                if client_id in self.warning_counts:
                    del self.warning_counts[client_id]
            
            if clients_to_remove:
                logger.debug(f"Cleaned up {len(clients_to_remove)} inactive client entries")


class ConnectionLimiter:
    """Limits the number of concurrent connections to prevent server overload"""
    
    def __init__(self, max_connections: int = 1000):
        self.max_connections = max_connections
        self.active_connections = set()
        self.lock = Lock()
    
    def can_connect(self, client_id: str) -> bool:
        """Check if a new connection can be accepted"""
        with self.lock:
            if len(self.active_connections) >= self.max_connections:
                logger.warning(f"Connection limit reached ({self.max_connections}). "
                              f"Rejecting connection from {client_id}")
                return False
            return True
    
    def add_connection(self, client_id: str):
        """Add a new connection"""
        with self.lock:
            self.active_connections.add(client_id)
            logger.debug(f"Connection added: {client_id}. "
                        f"Total connections: {len(self.active_connections)}")
    
    def remove_connection(self, client_id: str):
        """Remove a connection"""
        with self.lock:
            if client_id in self.active_connections:
                self.active_connections.remove(client_id)
                logger.debug(f"Connection removed: {client_id}. "
                            f"Total connections: {len(self.active_connections)}")
    
    def get_connection_count(self) -> int:
        """Get current number of active connections"""
        with self.lock:
            return len(self.active_connections)
