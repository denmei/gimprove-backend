from django.shortcuts import render
from .forms import NewsletterForm, ContactForm, LoginForm
from django.shortcuts import redirect
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from main.models.models import get_profile_type, UserProfile
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage

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
                return redirect(index)
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

@login_required
def index(request):
    if request.user.is_authenticated:
        if get_profile_type(request.user) == 'gym':
            return render(request, 'tracker/Gym/gym_tracker_base.html')
        return redirect('activities', request.user.id)
    return redirect('home')


@login_required
def about(request):
    return render(request, 'about.html')


class AppMockupView(LoginRequiredMixin, generic.ListView):
    model = UserProfile
    context_object_name = 'user_profile'
    template_name = 'tracker/User/AppMockup/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_id'] = self.request.user.id
        return context


@login_required
def contact(request):
    form_class = ContactForm

    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get(
                'contact_name'
            , '')
            contact_email = request.POST.get(
                'contact_email'
            , '')
            form_content = request.POST.get('content', '')

            # Email the profile with the
            # contact information
            template = get_template('subscription_email_template.txt')
            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
            }
            content = template.render(context)

            email = EmailMessage(
                "New contact form submission",
                content,
                "Your website" + '',
                ['meisnerdennis@web.de'],
                headers={'Reply-To': contact_email}
            )
            email.send()
            return redirect('contact')

    return render(request, 'contact.html', {
        'form': form_class
    })
