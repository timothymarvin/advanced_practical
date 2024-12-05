import re  # For enhanced validation


class SecureLoginSystem:
    def __init__(self, username, password):
        self._username = username  # Encapsulated attribute
        self._password = password  # Encapsulated attribute

    # Getter and Setter for username
    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        if not value:
            raise ValueError("Username cannot be empty.")
        self._username = value

    # Getter and Setter for password
    @property
    def password(self):
        return "*" * len(self._password)  # Return masked password for security

    @password.setter
    def password(self, value):
        if not self._is_strong_password(value):
            raise ValueError(
                "Password must be at least 8 characters long, contain uppercase, lowercase, digit, and special character."
            )
        self._password = value

    # Abstraction for password validation
    def _is_strong_password(self, password):
        pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$"
        return bool(re.match(pattern, password))

    # Public method to validate credentials
    def validate_credentials(self):
        if not self._username:
            print("Error: Username cannot be empty.")
            return False
        if not self._is_strong_password(self._password):
            print("Error: Password does not meet security requirements.")
            return False
        return True


# Example usage
try:
    # Valid username and password
    x = str(input('Enter username: '))
    y = str(input('Enter password: '))
    user = SecureLoginSystem(x, y)
    print(f"Username: {user.username}")  # Accessing username
    print(f"Password: {user.password}")

    # Update the password using the setter
    # user.password = "NewSecure@5678"

    # Validate credentials
    if user.validate_credentials():
        print("Login successful")
    else:
        print("Invalid credentials")

except ValueError as e:
    print(e)
