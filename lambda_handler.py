import csv
import boto3
from datetime import datetime

def lambda_handler(event, context):

    # Initialize variables with descriptive names
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    error_bucket_name = 'bucket_name' # provide a unique name for error buckets

    # Create an S3 client object for better performance (optional)
    s3_client = boto3.client('s3')  # Consider using client for bulk operations

    try:
        # Download CSV file, handle potential exceptions
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        csv_file_data = response['Body'].read().decode('utf-8').splitlines()

    except Exception as e:
        print(f"Error downloading CSV file: {e}")
        # Handle download error (e.g., log error, send notification)
        return {
            'statusCode': 500,
            'body': f"Error downloading CSV file: {e}"
        }

    # Initialize error flag and validation lists
    error_found = False
    valid_product_lines = ['Bakery', 'Meat', 'Dairy']
    valid_currencies = ['USD', 'MXN', 'CAD']

    # Process CSV content line by line
    for row_num, row in enumerate(csv.reader(csv_file_data[1:], delimiter=','), start=2):
        print(f'Processing row {row_num}: {row}')

        # Implement your custom validation logic here (replace TODO)
        # For example: check product line and currency validity
        if row[1] not in valid_product_lines or row[2] not in valid_currencies:
            error_found = True
            # Handle error per row (e.g., log error, move to error bucket)

    # Handle overall outcome (no errors or errors encountered)
    if not error_found:
        print("CSV file processed successfully!")
        # Implement success logic (e.g., log success, perform subsequent actions)
        return {
            'statusCode': 200,
            'body': 'CSV file processed successfully!'
        }
    else:
        print("Errors found in CSV file.")
        # Implement error handling logic for the entire file (e.g., move entire file to error bucket)
        # Move file to error bucket (optional):
        # s3_client.copy_object(Bucket=error_bucket_name, Key=object_key, CopySource={'Bucket': bucket_name, 'Key': object_key})

    return {
        'statusCode': 400,  # Updated to indicate processing error
        'body': 'Errors found in CSV file.'
    }
