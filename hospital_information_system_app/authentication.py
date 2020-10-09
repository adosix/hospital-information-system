from .models import User

def authenticate(username, password):
    for p in User.objects.raw('''SELECT id,First_name,Password password FROM hospital_information_system_app_user'''):
        if (str(p.First_name) == username) and (str(p.Password) == password):
            print("Succesfull: Good job Andrejko")
    return True
    