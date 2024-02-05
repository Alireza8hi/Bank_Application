from email.message import EmailMessage
import smtplib


def send_email(sender_email, sender_password, receiver_email, subject, body):
    message = EmailMessage()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.set_content(body)
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()

            server.login(sender_email, sender_password)

            server.send_message(message)
            return True

    except Exception as e:
        print("خطا در ارسال ایمیل:", str(e))
        return False


'''nima.1381.zamani@gmail.com
Nima5977@@@'''

"""# email = database_connector.get_email()--------------------------------------------------------------------------
email = "alireza8pc8@gmail.com"
subject = "ثبت نام در همراه بانک"
body = "ثبت نام شما در همراه بانک با موفقیت انجام شد."
email_phone_number.send_email("nima.1381.zamani@gmail.com", "Nima5977@@@", email, subject, body)"""

"""# email = database_connector.get_email()--------------------------------------------------------------------------
email = "alireza8pc8@gmail.com"
subject = "انتقال وجه در همراه بانک"
body = f"واریزی جدید.\n destination account number: {destination_account_number}\n amount: {amount}"
email_phone_number.send_email("nima.1381.zamani@gmail.com", "Nima5977@@@", email, subject, body)

# email = database_connector.get_email()--------------------------------------------------------------------------
email = "alireza8pc8@gmail.com"
subject = "انتقال وجه در همراه بانک"
body = f"دریافتی جدید.\n destination account number: {destination_account_number}\n amount: {amount}"
email_phone_number.send_email("nima.1381.zamani@gmail.com", "Nima5977@@@", email, subject, body)"""