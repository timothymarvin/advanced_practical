class User:
    # Define roles and their privileges
    _ROLE_PERMISSIONS = {
        'admin': {'access_sensitive_data': True},
        'user': {'access_sensitive_data': False},
    }

    def __init__(self, username, role):
        self.username = username
        # Validate role during initialization
        if role not in self._ROLE_PERMISSIONS:
            raise ValueError(f"Invalid role: {role}")
        self._role = role

    # Getter for role (to prevent direct modification)
    @property
    def role(self):
        return self._role

    # Method to check access to sensitive data
    def can_access_sensitive_data(self):
        # Check role-based permissions
        return self._ROLE_PERMISSIONS[self._role].get('access_sensitive_data', False)


# Usage
try:
    user1 = User('Alice', 'admin')  # Valid role
    user2 = User('Bob', 'user')  # Valid role
    # user3 = User('Charlie', 'guest')  # Invalid role, raises ValueError
except ValueError as e:
    print(e)

print(user1.can_access_sensitive_data())  # Output: True
print(user2.can_access_sensitive_data())  # Output: False
