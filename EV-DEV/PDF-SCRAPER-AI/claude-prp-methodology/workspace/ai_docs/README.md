# AI Docs - Curated Documentation

Store important documentation here for quick AI reference.

## Purpose

Cache frequently-used documentation locally so Claude can:
- Access it faster than web fetching
- Reference it in PRPs without URLs
- Work offline
- Have consistent documentation versions

## What to Store

### Framework Documentation
```
- Next.js App Router patterns
- FastAPI dependency injection
- Django ORM query optimization
- React hooks best practices
```

### Library Quirks
```
- "Library X requires Y before Z"
- Common gotchas and solutions
- API rate limits and workarounds
```

### API References
```
- Key API endpoints and parameters
- Authentication patterns
- Error codes and handling
```

### Integration Guides
```
- Stripe webhook setup
- AWS S3 upload patterns
- Database connection pooling
```

## File Naming Convention

Use descriptive names:
- `fastapi-jwt-auth-pattern.md`
- `next-15-server-components.md`
- `stripe-webhook-verification.md`
- `postgres-connection-pooling.md`

## How to Reference in PRPs

```yaml
- docfile: workspace/ai_docs/fastapi-jwt-auth-pattern.md
  why: Shows our JWT implementation pattern
```

## Maintenance

- **Update regularly** - Keep docs current with library versions
- **Remove outdated** - Delete when library/framework changes significantly
- **Version in filename** - `react-18-hooks.md` vs `react-19-hooks.md`

## Examples

See examples/ folder for how to reference these docs in PRPs.