from .models import User, Customer, Invoice, Profile, Product

def getOrganization(user):
    profile = Profile.objects.filter(user_id=user.id).first()
    return None if profile is None else profile.organization
