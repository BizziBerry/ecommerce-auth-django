from django.contrib.auth.tokens import PasswordResetTokenGenerator

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # В Python 3+ используем str вместо six.text_type
        return (
            str(user.pk) + 
            str(timestamp) + 
            str(user.is_active)
        )

account_activation_token = AccountActivationTokenGenerator()