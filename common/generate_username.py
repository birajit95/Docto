from datetime import datetime
from user_management.models import User


def get_username(user_type):
    prefix = ""
    if user_type.upper() == "DOCTOR":
        prefix += 'ud'
    elif user_type.upper() == "PATIENT":
        prefix += 'up'
    current_date = datetime.now().date()
    mid = str(current_date).replace('-', '')

    user = User.objects.filter(groups__name__iexact=user_type).last()
    if user:
        postfix = user.username[10:]
    else:
        postfix = 0000
    new_username = prefix + mid + str(int(postfix)+1).zfill(5)
    return new_username







