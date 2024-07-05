import boto3
from botocore.exceptions import NoCredentialsError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email import encoders


def download_file_from_s3(s3_client, bucket_name, s3_filename):
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=s3_filename)
        return response["Body"].read()
    except NoCredentialsError:
        print("Credentials not available")
        return None


def send_email_with_attachment(
    ses_client, sender, recipient, subject, body, attachment, filename
):
    try:
        # Create a multipart/mixed parent container.
        msg = MIMEMultipart("mixed")
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = recipient

        # Create a multipart/alternative child container.
        msg_body = MIMEMultipart("alternative")
        textpart = MIMEText(body, "plain")
        msg_body.attach(textpart)

        # Attach the multipart/alternative child container to the multipart/mixed
        # parent container.
        msg.attach(msg_body)

        # Define the attachment part and encode it using base64.
        att = MIMEApplication(attachment, Name=filename)
        att["Content-Disposition"] = 'attachment; filename="{}"'.format(filename)
        encoders.encode_base64(att)

        # Attach the attachment to the parent container.
        msg.attach(att)

        # Send the email.
        response = ses_client.send_raw_email(
            Source=sender,
            Destinations=[recipient],
            RawMessage={"Data": msg.as_string()},
        )
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
