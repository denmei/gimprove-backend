from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import ContactForm
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import get_template
from django.core.mail import send_mail

# Create your views here.


def home(request):
    if request.user.is_authenticated:
            return HttpResponseRedirect('/tracker/')
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_name = request.POST.get(
                'contact_name', '')
            contact_email = request.POST.get(
                'contact_email', '')

            # Email the profile with the
            # contact information
            template = get_template('home/subscription_email_template.txt')
            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
            }
            content = template.render(context)
            send_mail('SmartGym: Your Subscription', content, 'meisnerden@gmail.com', [contact_email],
                      fail_silently=False)
            return redirect('/home/', {'form': form})
    else:
        form = ContactForm()
        return render(request, 'home/homepage2.html', {'form': form})


def sign_up(request):
    form_class = ContactForm

    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get(
                'contact_name', '')
            contact_email = request.POST.get(
                'contact_email', '')
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

    return render(request, 'home/sign_up.html', {
        'form': form_class
    })
