from lib2to3.fixes.fix_input import context

from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

class Command(BaseCommand):
    help = "Send example email"

    def handle(self, *args, **options):
        self.stdout.write("Send Email")

        name = 'Grisha Valyna'
        subject = f"welcome, {name}"
        sender = 'mykola@example.com'
        recipient = 'grisha@example.com'

        context = {"name": name,}

        text_content = render_to_string(
            template_name="related_to_email/send_contact_email.txt",
            context=context
        )

        html_content = render_to_string(
            template_name="related_to_email/send_contact_email.html",
            context=context
        )
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=sender,
            to=[recipient],
            headers={"List-Unsubscribe": "<mailto:unsub@example.com>"},
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()

        self.stdout.write(self.style.SUCCESS("Email sent"))
