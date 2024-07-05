from fastapi import APIRouter, Depends, HTTPException
from typing import Dict

import boto3
from aws_function.custom_aws import download_file_from_s3, send_email_with_attachment
from aws_function.custom_excel import modify_worksheet

from db import (
    get_cell_table,
)

router = APIRouter()


@router.post("/submit")
async def receive_form_data(data: Dict, collection=Depends(get_cell_table)):
    try:
        # Print the from data send from frontend.
        print(data["hardware"])
        print(data["software"])

        # Query the cell_table from MongoDB
        cell_table_list = await collection.find({}, {"_id": 0}).to_list(None)
        if not cell_table_list:
            raise HTTPException(status_code=404, detail="Cell table not found")
        print(cell_table_list)

        # Result Dictionary
        result_dict = {}
        source_dict = data["software"]
        source_list = cell_table_list

        # Merge the list and dictionary
        for item in source_list:
            name = item["name"]
            cell = item["cell"]
            if name in source_dict:
                result_dict[cell] = source_dict[name]

        # Print the result
        print(result_dict)

        # Send a mail via AWS
        cdn_info = {
            "bucket_name": "software-application-templates",
            "s3_filename": "software_application_template_v1.xlsx",
        }

        mail_info = {
            "sender": "fs_foxconn_mcd_gitee@outlook.com",
            "recipient": "kun-che.lee@ftc-foxconn.com",
            "subject": "Software Application System",
            "body": "Please find the attached Excel file.",
        }

        application_content = result_dict

        data = {
            "cdn_info": cdn_info,
            "mail_info": mail_info,
            "application_content": application_content,
        }

        # Send the mail attached with application via AWS
        bucket_name = data["cdn_info"]["bucket_name"]
        s3_filename = data["cdn_info"]["s3_filename"]
        sender = data["mail_info"]["sender"]
        recipient = data["mail_info"]["recipient"]
        subject = data["mail_info"]["subject"]
        body = data["mail_info"]["body"]

        # Define modifications
        modifications = data["application_content"]

        # Download file from S3
        s3_client = boto3.client("s3")
        file_content = download_file_from_s3(s3_client, bucket_name, s3_filename)
        if file_content is None:
            return

        # Modify the worksheet
        modified_content = modify_worksheet(file_content, modifications)

        # Send email with attachment
        ses_client = boto3.client("ses")
        response = send_email_with_attachment(
            ses_client, sender, recipient, subject, body, modified_content, s3_filename
        )
        if response:
            print("Email sent! Message ID:", response["MessageId"])

        # Example: return the received data with a message
        return {"message": "Data received successfully!"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
