from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from .forms import NewsletterForm, ContactForm, LoginForm
from django.shortcuts import redirect
from django.template.loader import get_template
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth import authenticate, login
from tracker.views.views import index as indexview

# Create your views here.


def home(request):
    """
    Handles newsletter subscriptions. Valid email-addresses are added to the subscription-files and a confirmation is
    sent.
    :param request:
    :return:
    """
    if request.method == 'POST':
        newsletter_form = NewsletterForm(request.POST)
        contact_form = ContactForm(request.POST)
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user=user)
                return redirect(indexview)
        else:
            if newsletter_form.is_valid():
                contact_email = request.POST.get('contact_email', '')
                # Email the profile with the contact information
                template = get_template('landing_page/subscription_email_template.txt')
                context = {'contact_email': contact_email}
                content = template.render(context)
                # send confirmation
                # send_mail(subject='GImprove: Your Subscription', message=content, from_email='dennis@gimprove.com',
                #         recipient_list=list([contact_email] + ['dennis@gimprove.com']), fail_silently=False)

                subject, from_email, to = 'GImprove: Your Subscription', 'dennis@gimprove.com', [contact_email]
                text_content = 'This is an important message.'
                html_content = content
                msg = EmailMultiAlternatives(subject=subject, body=text_content, from_email=from_email, to=to, bcc=['dennis@gimprove.com'])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                # save mail-address locally
                # TODO: create Database for addresses
                with open('landing_page/newsletter_subscriptions.txt', 'a') as subscriptions_file:
                    subscriptions_file.write(contact_email + "\n")
            if contact_form.is_valid():
                contact_email = request.POST.get('email')
                contact_name = request.POST.get('name')
                message = request.POST.get('message')
                template = get_template('landing_page/contact_email_template.txt')
                context = {'email': contact_email, 'name': contact_name, 'message': message}
                content = template.render(context)
                subject, from_email, to = 'GImprove: Your Message', 'dennis@gimprove.com', [contact_email]
                text_content = 'This is an important message.'
                html_content = content
                msg = EmailMultiAlternatives(subject=subject, body=text_content, from_email=from_email, to=to, bcc=['dennis@gimprove.com'])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
        return redirect('/landing_page/', {'newsletter_form': newsletter_form, 'contact_form': contact_form,
                        'login_form': login_form})
    else:
        newsletter_form = NewsletterForm()
        contact_form = ContactForm()
        login_form = LoginForm()
        return render(request, "landing_page/index.html", {'newsletter_form': newsletter_form,
                                                           'contact_form': contact_form, 'login_form': login_form})
