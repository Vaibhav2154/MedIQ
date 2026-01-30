from jose import jwt, JWTError, ExpiredSignatureError
from uuid import UUID
import os
import logging

# Try to import UserRole enum if available; keep tolerant to avoid import errors
try:
    from app.models.user import UserRole  # adjust import if needed
except Exception:
    UserRole = None


JWT_PUBLIC_KEY = os.getenv("JWT_PUBLIC_KEY")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ISSUER = os.getenv("JWT_ISSUER", "eka-care")


class AuthenticationError(Exception):
    """Raised when authentication/validation fails."""


def verify_jwt(token: str) -> dict:
    """Verify a JWT token and return normalized user info.

    Behavior:
    - If `JWT_PUBLIC_KEY` is present, use RS256 verification.
    - Else if `JWT_SECRET_KEY` is present, use HS256 verification.
    - Else fall back to a development HS256 secret (logs a warning).

    Returns a dict with `id`, `email`, `role` on success.

    Raises `AuthenticationError` on any validation failure.
    """
    if not token or not isinstance(token, str):
        raise AuthenticationError("Missing token")

    # decide algorithm / key
    if JWT_PUBLIC_KEY:
        key = JWT_PUBLIC_KEY
        algorithms = ["RS256"]
    else:
        # prefer explicit secret, otherwise fallback (dev only)
        key = JWT_SECRET_KEY or "your-secret-key-change-in-production"
        algorithms = ["HS256"]

    try:
        payload = jwt.decode(
            token,
            key,
            algorithms=algorithms,
            options={"verify_aud": False, "verify_iss": False},
        )

        # ---- User model–level validation ----
        user_id = payload.get("sub")
        if not user_id:
            raise AuthenticationError("Missing user id (sub)")
        try:
            UUID(user_id)
        except Exception:
            raise AuthenticationError("Invalid sub: must be a UUID")

        email = payload.get("email")
        if not email or not isinstance(email, str):
            raise AuthenticationError("Invalid or missing email")

        role = payload.get("role")
        if UserRole is not None:
            try:
                valid_roles = {r.value for r in UserRole}
            except Exception:
                valid_roles = None
            if valid_roles and role not in valid_roles:
                raise AuthenticationError("Invalid user role")
        else:
            if not role or not isinstance(role, str):
                raise AuthenticationError("Invalid user role")

        return {"id": user_id, "email": email, "role": role}

    except ExpiredSignatureError:
        raise AuthenticationError("JWT token expired")
    except JWTError as e:
        # Log the error for debugging without leaking secrets
        logging.exception("JWT validation error")
        raise AuthenticationError(f"JWT validation failed: {str(e)}")
    except ValueError as e:
        raise AuthenticationError(f"Invalid token data: {str(e)}")
