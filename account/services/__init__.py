from account.models import Waiter, Admin


def waiter_exists(email):
    waiter = Waiter.objects.filter(email=email).first()
    if waiter:
        return True
    return False


def admin_exists(email):
    waiter = Admin.objects.filter(email=email).first()
    if waiter:
        return True
    return False
