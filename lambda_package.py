import json
from PIL import Image  
import io
import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get the S3 bucket and key from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Read the image from S3
    response = s3.get_object(Bucket=bucket, Key=key)
    image_content = response['Body'].read()

    # Resize the image
    image = Image.open(io.BytesIO(image_content))
    resized_image = image.resize((300, 300))
   
   # Save the resized image back to S3
    resized_key = f"resized/{key}"
    output_buffer = io.BytesIO()
    resized_image.save(output_buffer, format="JPEG")
    s3.put_object(Body=output_buffer.getvalue(), Bucket=bucket, Key=resized_key)

    return {
        'statusCode': 200,
        'body': json.dumps('Image resized successfully!')
    }
