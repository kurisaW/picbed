import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def count_files(directory):
    file_count = 0
    for root, dirs, files in os.walk(directory):
        file_count += len(files)
    return file_count

def send_email(github_token, recipient, file_count):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    subject = 'File Count Reminder'
    content = f'The repository has {file_count} files.'

    message = MIMEText(content, 'plain', 'ascii')
    message['From'] = Header('GitHub Action')
    message['To'] = Header(recipient)
    message['Subject'] = Header(subject)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login('githubaction@gmail.com', github_token)
        server.sendmail('githubaction@gmail.com', recipient, message.as_string())
        server.quit()
        print("Email reminder sent to", recipient)
    except Exception as e:
        print("Failed to send email:", str(e))

repository_path = '.'  # Replace with the path to your repository if needed
file_limit = 999

file_count = count_files(repository_path)
if file_count > file_limit:
    github_token = os.environ.get('INPUT_GITHUB_TOKEN')
    default_email = os.environ.get('GITHUB_ACTOR') + '@users.noreply.github.com'

    send_email(github_token, default_email, file_count)
else:
    print("The repository has", file_count, "files. No reminder needed.")
