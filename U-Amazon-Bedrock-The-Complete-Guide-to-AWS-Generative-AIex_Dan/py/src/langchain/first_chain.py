from langchain_aws import BedrockLLM as Bedrock
from langchain_core.prompts import ChatPromptTemplate
import boto3

AWS_REGION = "us-west-2"

bedrock = boto3.client(service_name="bedrock-runtime", region_name=AWS_REGION)

model = Bedrock(model_id="amazon.titan-text-express-v1", client=bedrock)


# def invoke_model():
#     response = model.invoke("What is the highest mountain in the world?")
#     print(response)


def fist_chain():
    template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Write a short description of the animal provided by the user",
            ),
            ("human", "{animal_name}"),
        ]
    )
    chain = template.pipe(model)

    response = chain.invoke({"animal_name": "Tiger"})
    print(response)


fist_chain()
