


class RoleChecker:
    """Класс для определения роли пользователя."""

    def get_user_role(self, user):
        """Метод для определения роли пользователя."""
        if hasattr(user, 'employer_profile'):
            return 'employer'
        elif hasattr(user, 'manager_profile'):
            return 'manager'
        return None
