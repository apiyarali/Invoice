from .models import User, Customer, Invoice, Profile, Product

# ####################################################################################
# xhtml2pdf
# 
# Code Snippet taken from: 
# https://www.codingforentrepreneurs.com/blog/html-template-to-pdf-in-django
# 
# ####################################################################################
# from io import BytesIO
# from django.http import HttpResponse
# from django.template.loader import get_template
# from xhtml2pdf import pisa


def getOrganization(user):
    profile = Profile.objects.filter(user_id=user.id).first()
    return None if profile is None else profile.organization

# xhtml2pdf, see above comment for more information
# def render_to_pdf(template_src, context_dict={}):
#     template = get_template(template_src)
#     html  = template.render(context_dict)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return None