import os
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

# Initialize the HTTPBearer for token extraction
security = HTTPBearer()

def get_admin_api_key() -> str:
    """Get admin API key from environment variables"""
    api_key = os.getenv("ADMIN_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Admin API key not configured"
        )
    return api_key

def verify_admin_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> bool:
    """
    Verify that the provided token matches the admin API key
    Usage: Add as dependency to admin-only endpoints
    """
    admin_key = get_admin_api_key()
    
    if not credentials or credentials.credentials != admin_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return True

def optional_admin_token(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> bool:
    """
    Optional admin verification - returns True if admin, False if not
    Useful for endpoints that behave differently for admins
    """
    if not credentials:
        return False
    
    try:
        admin_key = get_admin_api_key()
        return credentials.credentials == admin_key
    except:
        return False

# Convenience function for admin-only endpoints
admin_required = Depends(verify_admin_token)
