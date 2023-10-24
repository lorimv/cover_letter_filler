"""responsible for sending emails
"""
import base64
from email.message import EmailMessage

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from . import credentials
from .config_handler import get_config_value

# this is the module that will auto-send follow up emails when -m is called
# im thinking it will take arguments from tracker module that returns company name & email & job title


def send_mail(company_name, position_name, app_date, company_email):
    """Sends follow-up email, according to function parameters

    Args:
        company_name (str): name of company
        position_name (str): name of position
        app_date (str): date application was originally sent
        company_email (str): company's email address

    Returns:
        ???: draft of email ig? need to read documentation again

    """
    MY_NAME = get_config_value('Mailer', 'myName')  # TODO get name (query() in config_handler?)
    # MY_EMAIL = get_config_value('Mailer', 'myEmail')

    # TODO maybe ask for confirmation before sending an email jic

    try:
        # The following code block is the writer/sender for follow-up emails
        service = build('gmail', 'v1', credentials=credentials)

        message = EmailMessage()  # maybe this could be stored in a file, more accessible for user to edit
        message.set_content('Hello ' + company_name + ',\n\n'  # (and would take up less space)

                            'My name is ' + MY_NAME + '. I am writing to follow up on my application for the ' +
                            position_name + ' role at ' + company_name + ' on ' + app_date + '.\n\n'
                            'I remain excited about the possibility of joining your team and '
                            'contributing to its success. I believe my knowledge of Agile methodologies and passion for development '
                            ' make me a strong candidate for the position, and I would love to discuss '
                            'the opportunity even further.\n\n'

                            'Please let me know of any questions I can answer or additional information '
                            'I can provide. Thank you for your consideration. I look forward to speaking soon!\n\n'

                            'Warm regards,\n' +
                            MY_NAME)
                            # TODO read text from txt file as fstring?

        message['To'] = company_email
        # message['From'] = MY_EMAIL
        message['Subject'] = 'Application for ' + position_name + ' at ' + company_name

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {
            'raw': encoded_message
        }

        # send_message = service.users().messages().send(  # TODO uncomment these!
        #                userId='me', body=create_message).execute()
        print("email sent!!!")
        print("just kidding. debug !")
        print(company_name)
        print(company_email)
        print(app_date)
    except HttpError as e:
        print(e)
        print("Invalid email!")
        print('Manual follow up required')
        print('Company: ' + company_name)
        print('Position: ' + position_name)
        send_message = None
    return None  # dummy return (sick of sending emails while testing)
    return send_message
