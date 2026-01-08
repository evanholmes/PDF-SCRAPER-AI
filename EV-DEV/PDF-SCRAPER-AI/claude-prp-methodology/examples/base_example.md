# BASE PRP Example: Add JWT Authentication

**Generated**: 2025-12-16
**Type**: BASE PRP (Standard Implementation)
**Complexity**: Medium
**Estimated Time**: 1-2 hours

---

## Goal

Implement JWT-based authentication for FastAPI application with token generation, validation, and refresh capabilities.

## Why

- Enable secure API access control
- Allow users to authenticate once and access protected endpoints
- Support token refresh for better UX (no frequent re-authentication)

## What

### User-Visible Behavior
- POST /auth/login → Returns access_token + refresh_token
- GET /protected → Requires valid access token in Authorization header
- POST /auth/refresh → Accepts refresh_token, returns new access_token

### Success Criteria
- [ ] Users can log in with email/password
- [ ] Protected endpoints reject invalid/expired tokens
- [ ] Token refresh works without re-entering password
- [ ] All security best practices followed (RS256, proper expiry)

## All Needed Context

### Documentation & References

```yaml
- url: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
  why: Official FastAPI JWT pattern with dependency injection
  critical: Shows how to use OAuth2PasswordBearer for token extraction

- url: https://pyjwt.readthedocs.io/en/stable/
  why: PyJWT library docs for RS256 algorithm
  section: "Algorithms" page shows RS256 key generation

- file: src/api/users.py (lines 23-45)
  why: Shows our existing endpoint structure and error handling pattern
  note: Use same response format with standardize_response()

- file: src/database/models/user.py
  why: User model with password_hash field
  note: Use check_password() method for verification

- gotcha: "PyJWT 2.0+ required for RS256"
  solution: "Install with: pip install 'PyJWT[crypto]>=2.0'"

- gotcha: "Don't use HS256 (symmetric) in production"
  solution: "Always use RS256 (asymmetric) for better security"
```

### Current Codebase Tree

```bash
project/
├── src/
│   ├── api/
│   │   └── users.py          # Existing endpoint patterns
│   ├── database/
│   │   └── models/
│   │       └── user.py       # User model with password methods
│   ├── utils/
│   │   └── responses.py      # standardize_response()
│   └── main.py              # FastAPI app instance
├── tests/
│   └── api/
│       └── test_users.py     # Test pattern to follow
└── config/
    └── settings.py          # Environment variables
```

### Desired Codebase Tree

```bash
project/
├── src/
│   ├── api/
│   │   ├── users.py
│   │   └── auth.py           # NEW: Authentication endpoints
│   ├── auth/                 # NEW: Auth logic folder
│   │   ├── __init__.py
│   │   ├── jwt.py           # JWT generation/validation
│   │   └── dependencies.py   # FastAPI dependencies
│   ├── database/
│   │   └── models/
│   │       ├── user.py
│   │       └── token.py      # NEW: Refresh token model
│   └── ...
├── tests/
│   ├── api/
│   │   └── test_auth.py      # NEW: Auth endpoint tests
│   └── auth/
│       └── test_jwt.py       # NEW: JWT logic tests
└── config/
    ├── keys/                 # NEW: RS256 key pair
    │   ├── private.pem
    │   └── public.pem
    └── settings.py
```

### Known Gotchas

```python
# GOTCHA #1: PyJWT requires crypto dependencies for RS256
# → pip install 'PyJWT[crypto]>=2.0'

# GOTCHA #2: Keys must be in PEM format, not JWK
# → Generate with: ssh-keygen -t rsa -b 2048 -m PEM

# GOTCHA #3: FastAPI's OAuth2PasswordBearer expects "Bearer {token}"
# → Don't forget "Bearer " prefix in Authorization header

# GOTCHA #4: Token expiry must be datetime, not timedelta
# → Use: datetime.utcnow() + timedelta(hours=1)
```

## Implementation Blueprint

### Data Models

```python
# src/database/models/token.py
class RefreshToken:
    id: int
    user_id: int
    token: str  # Hashed refresh token
    expires_at: datetime
    created_at: datetime
```

### Task List

```yaml
Task 1: Generate RS256 Key Pair
CREATE config/keys/ directory:
  - Generate private key: openssl genrsa -out private.pem 2048
  - Generate public key: openssl rsa -in private.pem -pubout -out public.pem
  - Add to .gitignore: config/keys/*.pem
  - VALIDATE: cat config/keys/private.pem | head -1 → "-----BEGIN RSA PRIVATE KEY-----"

Task 2: Create JWT Utilities
CREATE src/auth/jwt.py:
  - IMPLEMENT: generate_access_token(user_id: int) -> str
  - IMPLEMENT: generate_refresh_token() -> str
  - IMPLEMENT: verify_token(token: str) -> dict
  - VALIDATE: pytest tests/auth/test_jwt.py -v

Task 3: Create FastAPI Dependencies
CREATE src/auth/dependencies.py:
  - MIRROR pattern from: FastAPI docs OAuth2PasswordBearer
  - IMPLEMENT: get_current_user(token: str = Depends(oauth2_scheme))
  - VALIDATE: pytest tests/auth/test_dependencies.py -v

Task 4: Create Auth Endpoints
CREATE src/api/auth.py:
  - MIRROR pattern from: src/api/users.py (endpoint structure)
  - IMPLEMENT: POST /auth/login
  - IMPLEMENT: POST /auth/refresh
  - VALIDATE: pytest tests/api/test_auth.py -v

Task 5: Create Refresh Token Model & Migration
CREATE src/database/models/token.py:
  - MIRROR pattern from: src/database/models/user.py
  - CREATE migration: alembic revision -m "add_refresh_tokens"
  - VALIDATE: alembic upgrade head (no errors)

Task 6: Register Auth Router
MODIFY src/main.py:
  - FIND: app.include_router(users.router)
  - ADD AFTER: app.include_router(auth.router, prefix="/auth")
  - VALIDATE: curl http://localhost:8000/docs → See /auth endpoints

Task 7: Protect Existing Endpoints
MODIFY src/api/users.py:
  - FIND: @router.get("/users/me")
  - ADD dependency: current_user: User = Depends(get_current_user)
  - VALIDATE: curl without token → 401, with valid token → 200
```

### Pseudocode (Task 2 Detail)

```python
# src/auth/jwt.py

def generate_access_token(user_id: int) -> str:
    # PATTERN: Load keys from config (see config/settings.py)
    private_key = load_private_key()  # from config/keys/private.pem

    # PATTERN: Standard JWT claims
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1),  # 1 hour expiry
        "iat": datetime.utcnow(),
        "type": "access"
    }

    # CRITICAL: Use RS256, not HS256
    token = jwt.encode(payload, private_key, algorithm="RS256")
    return token

def verify_token(token: str) -> dict:
    # PATTERN: Load public key
    public_key = load_public_key()  # from config/keys/public.pem

    try:
        # GOTCHA: Must specify algorithms list
        payload = jwt.decode(token, public_key, algorithms=["RS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

## Validation Loop

### Level 1: Syntax & Style
```bash
ruff check src/auth/ --fix
mypy src/auth/
# Expected: No errors
```

### Level 2: Unit Tests
```bash
pytest tests/auth/test_jwt.py -v
# Expected: All 6 tests pass
# Tests: token generation, validation, expiry, invalid tokens

pytest tests/auth/test_dependencies.py -v
# Expected: All 4 tests pass
# Tests: get_current_user with valid/invalid/expired tokens
```

### Level 3: Integration Tests
```bash
# Start server
uvicorn src.main:app --reload

# Test login
curl -X POST http://localhost:8000/auth/login \
  -d "username=test@example.com&password=testpass"
# Expected: {"access_token": "eyJ...", "refresh_token": "..."}

# Test protected endpoint
curl http://localhost:8000/users/me \
  -H "Authorization: Bearer eyJ..."
# Expected: {"id": 1, "email": "test@example.com"}

# Test without token
curl http://localhost:8000/users/me
# Expected: 401 Unauthorized
```

### Level 4: Security Validation
```bash
# Test token expiry (wait 1 hour or mock time)
# Test refresh token flow
# Test invalid signature
# Test algorithm confusion attack (try HS256)
```

## Final Checklist

- [ ] All tests pass: `pytest tests/ -v`
- [ ] Keys generated and .gitignored
- [ ] Tokens use RS256 (not HS256)
- [ ] Protected endpoints require auth
- [ ] Refresh flow works
- [ ] Error messages are clear (not leaking info)
- [ ] Documentation updated (API docs show auth)