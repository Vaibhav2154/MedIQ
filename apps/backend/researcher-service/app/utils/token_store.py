"""
STEP 8: Token Storage and Revocation

Redis-backed token store with SHA-256 hashing and TTL.
Supports policy-based revocation.
"""

import redis
import hashlib
import json
from typing import Optional, Dict, Any
from datetime import datetime


class TokenStore:
    """Redis-backed token store with revocation support."""
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        ttl_seconds: int = 300
    ):
        """
        Initialize Redis connection.
        
        Args:
            host: Redis host (default: localhost)
            port: Redis port (default: 6379)
            db: Redis database number (default: 0)
            ttl_seconds: Token TTL in seconds (default: 300 = 5 minutes)
        """
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True
        )
        self.ttl_seconds = ttl_seconds
    
    def _hash_token(self, token: str) -> str:
        """
        Hash token using SHA-256.
        
        Args:
            token: Raw token string
        
        Returns:
            str: SHA-256 hash of token
        """
        return hashlib.sha256(token.encode()).hexdigest()
    
    def store_token(
        self,
        token: str,
        subject_id: str,
        purpose: str,
        allowed_fields: list,
        request_id: str
    ) -> bool:
        """
        Store token in Redis with metadata.
        
        STEP 8: Token Issuance & Storage
        
        Stores:
        - Hash(token) as key
        - Metadata as JSON value
        - TTL of 300 seconds (5 minutes)
        
        Args:
            token: Raw JWT token
            subject_id: Subject/patient ID
            purpose: Purpose of access
            allowed_fields: List of allowed fields
            request_id: Request ID for tracing
        
        Returns:
            bool: True if stored successfully
        """
        
        try:
            token_hash = self._hash_token(token)
            
            # Build metadata
            metadata = {
                "subject_id": subject_id,
                "purpose": purpose,
                "allowed_fields": allowed_fields,
                "request_id": request_id,
                "created_at": datetime.utcnow().isoformat(),
                "status": "active"
            }
            
            # Store with TTL
            key = f"token:{token_hash}"
            self.redis_client.setex(
                key,
                self.ttl_seconds,
                json.dumps(metadata)
            )
            
            # Also store reverse index: subject_id -> token_hash
            subject_key = f"subject:{subject_id}:tokens"
            self.redis_client.sadd(subject_key, token_hash)
            self.redis_client.expire(subject_key, self.ttl_seconds)
            
            return True
        
        except Exception as e:
            print(f"Failed to store token: {str(e)}")
            return False
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify token exists and is not revoked.
        
        Args:
            token: Raw JWT token
        
        Returns:
            dict: Token metadata if valid, None if revoked or not found
        """
        
        try:
            token_hash = self._hash_token(token)
            key = f"token:{token_hash}"
            
            data = self.redis_client.get(key)
            
            if not data:
                return None
            
            metadata = json.loads(data)
            
            # Check if revoked
            if metadata.get("status") == "revoked":
                return None
            
            return metadata
        
        except Exception as e:
            print(f"Failed to verify token: {str(e)}")
            return None
    
    def revoke_token(self, token: str) -> bool:
        """
        Revoke a single token.
        
        STEP 10: Revocation Listener
        
        Marks token as revoked instead of deleting
        (for audit trail).
        
        Args:
            token: Raw JWT token to revoke
        
        Returns:
            bool: True if revoked successfully
        """
        
        try:
            token_hash = self._hash_token(token)
            key = f"token:{token_hash}"
            
            # Get existing metadata
            data = self.redis_client.get(key)
            if not data:
                return False
            
            metadata = json.loads(data)
            metadata["status"] = "revoked"
            metadata["revoked_at"] = datetime.utcnow().isoformat()
            
            # Update metadata
            self.redis_client.setex(
                key,
                self.ttl_seconds,
                json.dumps(metadata)
            )
            
            return True
        
        except Exception as e:
            print(f"Failed to revoke token: {str(e)}")
            return False
    
    def revoke_by_subject(self, subject_id: str) -> int:
        """
        Revoke all tokens for a subject (policy-based revocation).
        
        STEP 10: Policy-Based Revocation
        
        Args:
            subject_id: Subject/patient ID
        
        Returns:
            int: Number of tokens revoked
        """
        
        try:
            subject_key = f"subject:{subject_id}:tokens"
            
            # Get all token hashes for subject
            token_hashes = self.redis_client.smembers(subject_key)
            revoked_count = 0
            
            for token_hash in token_hashes:
                key = f"token:{token_hash}"
                
                # Get metadata
                data = self.redis_client.get(key)
                if data:
                    metadata = json.loads(data)
                    metadata["status"] = "revoked"
                    metadata["revoked_at"] = datetime.utcnow().isoformat()
                    
                    # Update
                    self.redis_client.setex(
                        key,
                        self.ttl_seconds,
                        json.dumps(metadata)
                    )
                    revoked_count += 1
            
            # Clear subject token set
            self.redis_client.delete(subject_key)
            
            return revoked_count
        
        except Exception as e:
            print(f"Failed to revoke by subject: {str(e)}")
            return 0
    
    def revoke_by_purpose(self, subject_id: str, purpose: str) -> int:
        """
        Revoke all tokens for a subject with specific purpose.
        
        Args:
            subject_id: Subject/patient ID
            purpose: Purpose to revoke
        
        Returns:
            int: Number of tokens revoked
        """
        
        try:
            subject_key = f"subject:{subject_id}:tokens"
            token_hashes = self.redis_client.smembers(subject_key)
            revoked_count = 0
            
            for token_hash in token_hashes:
                key = f"token:{token_hash}"
                data = self.redis_client.get(key)
                
                if data:
                    metadata = json.loads(data)
                    
                    # Only revoke if purpose matches
                    if metadata.get("purpose") == purpose:
                        metadata["status"] = "revoked"
                        metadata["revoked_at"] = datetime.utcnow().isoformat()
                        
                        self.redis_client.setex(
                            key,
                            self.ttl_seconds,
                            json.dumps(metadata)
                        )
                        revoked_count += 1
            
            return revoked_count
        
        except Exception as e:
            print(f"Failed to revoke by purpose: {str(e)}")
            return 0
    
    def get_token_count(self, subject_id: str) -> int:
        """
        Get number of active tokens for a subject.
        
        Args:
            subject_id: Subject/patient ID
        
        Returns:
            int: Number of active tokens
        """
        
        try:
            subject_key = f"subject:{subject_id}:tokens"
            count = 0
            
            token_hashes = self.redis_client.smembers(subject_key)
            
            for token_hash in token_hashes:
                key = f"token:{token_hash}"
                data = self.redis_client.get(key)
                
                if data:
                    metadata = json.loads(data)
                    if metadata.get("status") == "active":
                        count += 1
            
            return count
        
        except Exception as e:
            print(f"Failed to get token count: {str(e)}")
            return 0
    
    def health_check(self) -> bool:
        """
        Check Redis connection health.
        
        Returns:
            bool: True if Redis is healthy
        """
        
        try:
            self.redis_client.ping()
            return True
        except Exception:
            return False


# Global token store instance
token_store = TokenStore(host="localhost", port=6379, db=0, ttl_seconds=300)
