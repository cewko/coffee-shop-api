from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("User must have an email address")
        
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_cashier(self, username, email, password):
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.role = 1
        user.save(using=self._db)

        return user

    def create_barista(self, username, email, password):
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.role = 2
        user.save(using=self._db)

        return user

    def create_manager(self, username, email, password):
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.role = 3
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.role = 4
        user.save(using=self._db)

        return user