"""
Permission enforcer combining RBAC and ABAC.
"""

from typing import List, Dict, Any
from ..models import UserContext, Role

class PermissionEnforcer:
    def __init__(self):
        self.rbac_enabled = True
        self.abac_enabled = True
        
        # Role hierarchy: ADMIN > EDITOR > ANALYST > VIEWER
        self.role_hierarchy = {
            Role.ADMIN: 100,
            Role.EDITOR: 80,
            Role.ANALYST: 60,
            Role.VIEWER: 40
        }
        
        # Permission mapping for RBAC
        self.role_permissions = {
            Role.ADMIN: ["read:*", "write:*", "delete:*", "manage:*"],
            Role.EDITOR: ["read:*", "write:own", "update:own"],
            Role.ANALYST: ["read:*", "analyze:*"],
            Role.VIEWER: ["read:public", "read:internal"]
        }
    
    def enforce_access(self, user: UserContext, resource_access_level: str = "public", action: str = "read") -> bool:
        """
        Check if user has access to a resource.
        resource_access_level can be: "public", "internal", "confidential", "restricted"
        """
        # Admin always has access
        if Role.ADMIN in user.roles:
            return True
        
        # Public resources - everyone
        if resource_access_level == "public":
            return True
        
        # Internal resources - any authenticated user with role >= ANALYST
        if resource_access_level == "internal":
            return self._has_min_role(user, Role.ANALYST)
        
        # Confidential - need EDITOR or higher
        if resource_access_level == "confidential":
            return self._has_min_role(user, Role.EDITOR)
        
        # Restricted - only ADMIN
        if resource_access_level == "restricted":
            return Role.ADMIN in user.roles
        
        # Default deny
        return False
    
    def _has_min_role(self, user: UserContext, min_role: Role) -> bool:
        """Check if user has at least the given role."""
        user_max_level = max((self.role_hierarchy.get(r, 0) for r in user.roles), default=0)
        required_level = self.role_hierarchy.get(min_role, 0)
        return user_max_level >= required_level
    
    def check_permission(self, user: UserContext, permission: str) -> bool:
        """Check if user has a specific permission string."""
        if not self.rbac_enabled:
            return True
        
        for role in user.roles:
            allowed = self.role_permissions.get(role, [])
            for p in allowed:
                if p == permission or (p.endswith(":*") and permission.startswith(p[:-2])):
                    return True
        return False
    
    def audit_access_decision(self, user: UserContext, resource: str, action: str, granted: bool, reason: str = ""):
        """Log access decision for auditing."""
        # In production, write to a secure log
        from ..utils.logging import get_logger
        logger = get_logger("permissions")
        logger.info(f"Access decision: user={user.user_id}, resource={resource}, action={action}, granted={granted}, reason={reason}")
