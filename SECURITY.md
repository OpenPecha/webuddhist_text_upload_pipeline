# Security Guidelines

This document outlines security best practices for the Payload Generator Pecha project.

## 🔒 Environment Variables & Secrets Management

### ✅ What We Do Right

1. **No Hardcoded Secrets**: API endpoints and credentials are never hardcoded in source code
2. **Environment Variables**: All sensitive configuration is loaded from environment variables
3. **Template System**: `env.template` provides a safe template without real values
4. **Gitignore Protection**: `.env` files are automatically ignored by Git
5. **Optional Credentials**: Credentials can be provided at runtime instead of stored

### 🚫 What to Avoid

- **Never commit `.env` files** to version control
- **Never hardcode API endpoints** in source code
- **Never store production credentials** in development environments
- **Never share `.env` files** via email, chat, or other insecure channels

## 🛡️ Configuration Security

### Development Environment
```bash
# .env file for development
WEBUDDHIST_API_BASE_URL=https://dev-api.example.com
WEBUDDHIST_EMAIL=dev-user@example.com
WEBUDDHIST_PASSWORD=dev-password
ENVIRONMENT=development
```

### Production Environment
```bash
# .env file for production (or use proper secret management)
WEBUDDHIST_API_BASE_URL=https://api.production.com
# DO NOT store production credentials in .env files
# Use proper secret management systems instead
ENVIRONMENT=production
```

## 🔐 Authentication Security

### Recommended Approach
1. **Runtime Prompts**: Let the application prompt for credentials
2. **Environment Variables**: Use for non-production environments only
3. **Secret Management**: Use proper systems (AWS Secrets Manager, Azure Key Vault, etc.) for production

### Example: Secure Authentication Flow
```python
# The application will:
1. Check for credentials in environment variables
2. If not found, prompt the user securely
3. Never log or store credentials permanently
```

## 📋 Security Checklist

### Before Deployment
- [ ] Verify `.env` is in `.gitignore`
- [ ] Remove any hardcoded endpoints from code
- [ ] Use proper secret management for production
- [ ] Test with environment variables
- [ ] Review all configuration files

### Code Review Checklist
- [ ] No API endpoints in source code
- [ ] No credentials in source code
- [ ] Environment variables used correctly
- [ ] `.env` files not committed
- [ ] Documentation doesn't expose real endpoints

## 🚨 What to Do If Secrets Are Exposed

### If you accidentally commit secrets:

1. **Immediately rotate/change** the exposed credentials
2. **Remove the secrets** from Git history:
   ```bash
   # Remove file from Git history
   git filter-branch --force --index-filter \
   'git rm --cached --ignore-unmatch .env' \
   --prune-empty --tag-name-filter cat -- --all
   
   # Force push to remote
   git push origin --force --all
   ```
3. **Notify your team** about the incident
4. **Update all environments** with new credentials

## 🔧 Environment Variable Best Practices

### Naming Convention
- Use `WEBUDDHIST_` prefix for API-related variables
- Use descriptive names: `WEBUDDHIST_API_BASE_URL` not `API_URL`
- Use uppercase with underscores: `LOG_LEVEL` not `logLevel`

### Value Guidelines
- **URLs**: Include protocol (`https://`) but no trailing slashes
- **Endpoints**: Start with `/` for paths
- **Booleans**: Use `true`/`false` (lowercase)
- **Passwords**: Use strong, unique passwords

### Example Structure
```bash
# Good
WEBUDDHIST_API_BASE_URL=https://api.example.com
WEBUDDHIST_SEGMENTS_ENDPOINT=/api/v1/segments

# Bad
API_URL=api.example.com/api/v1/segments/
```

## 📖 Additional Resources

- [OWASP Application Security](https://owasp.org/www-project-application-security-verification-standard/)
- [12-Factor App Config](https://12factor.net/config)
- [Python Security Best Practices](https://python.org/dev/security/)

## 🆘 Reporting Security Issues

If you discover a security vulnerability, please:

1. **Do not** create a public GitHub issue
2. **Email** the maintainers directly
3. **Include** detailed information about the vulnerability
4. **Wait** for a response before public disclosure

---

**Remember**: Security is everyone's responsibility. When in doubt, choose the more secure option.
