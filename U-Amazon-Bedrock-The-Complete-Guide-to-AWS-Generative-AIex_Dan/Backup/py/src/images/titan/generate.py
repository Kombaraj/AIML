import boto3
import json
import base64

client = boto3.client(service_name='bedrock-runtime', region_name="us-west-2")

stability_image_config = json.dumps({
    "taskType": "TEXT_IMAGE",
    "textToImageParams": {
        "text": "White color cat sitting on a wooden table",      
    },
    "imageGenerationConfig": {
        "numberOfImages": 1,
        "height": 512,
        "width": 512,
        "cfgScale": 8.0,
    }
})

response = client.invoke_model(
    body=stability_image_config, 
    modelId="amazon.titan-image-generator-v1", 
    accept="application/json", 
    contentType="application/json")

response_body = json.loads(response.get("body").read())
base64_image = response_body.get("images")[0]

base_64_image = base64.b64decode(base64_image)

file_path = "cat.png"
with open(file_path, "wb") as f:
    f.write(base_64_image)

# AWS_ACCOUNT=$(aws sts get-caller-identity --query "Account" --output text)
# aws s3 mb s3://learn-ai-${AWS_ACCOUNT} --region us-west-2
# aws s3 cp cat.png s3://learn-ai-${AWS_ACCOUNT} --region us-west-2