Learning: Udemy
Course: Amazon Bedrock - The Complete Guide to AWS Generative AI
Author: Alex Dan
GitHub: https://github.com/alexhddev/Bedrock_course.git


Section 2 - Introduction to Amazon Bedrock & Tools setup
	Amazon Bedrock - Console overview
	Setup for SDK access
	Create IAM user and configure

	===> py\src\intro\steps.txt
    
	python environment setup

	#### Create environment
	
	```
	cd py
	python3 -m venv .venv
	```
	.venv folder will be created
	add ".venv" in .gitignore file

	# Activate environment
	# Windows
	.venv\Scripts\activate

	# Linux
	source .venv/bin/activate

	pip install -r requirements.txt

	# List all Foundation Models
	python3 py/src/intro/starter.py

Section 3: Working with Text Models

	# Test Tokens in a prompt
	https://platform.openai.com/tokenizer

	Text Model Parameters
		Temperature - controls the randomness or creativity of the model:
			* 0 - more deterministic results
			* 1 - more creative results
		High temperature - bigger risk of nonsensical / irrelevant content / halucinations
		
	# Generic Prompt
	python3 py/src/text/generate.py

	# Text Summarization
	python3 py/src/text/summary.py
	
	# Mini Chat
	python3 py/src/text/no_history_chat.py
	python3 py/src/text/history_chat.py


Section 4: Working with Image Models
	python3 py/src/images/stability.py

	python3 py/src/images/titan/generate.py
	python3 py/src/images/titan/inpaint.py

Section 5: Amazon Bedrock Embedding Models

# Simple Embedding 
python3 py/src/embed/sample.py

Text Embedding:
python3 py/src/embed/text.py

Image Embedding:
cd py/src/embed
python3 image.py

Vector Database:
	* Pinecone
	* Chroma
	* Redis
	* Amazon OpenSearch Service
	* Amazon Aurora PostgreSQL


Section 7: Project RAG

Local RAG app and LangChain
	Local RAG App - Chat with your data
	Integrate Bedrock with LangChain

LangChain
	LangChain is a framework for developing applications powered by language models
	Integrates with external data and vector databases
	Implement abstractions 

First Chain
	Go inside PY folder
		pip install -r requirements.txt
		python3 first_chain.py

Retrieval Augmented Generation
	RAG is the processs of optimizing the output of a large language model, so it references an authoritative knowledge base outside of its training data sources before generating a response

	RAG extends the capabilities of LLMs to specific domains or an organization's internal knowledge base, all without the need to retrain the model.
Basic RAG app
    Make sure if "faiss-cpu" library added in the requirements.txt
	pip install -r requirements.txt
	python3 py/src/langchain/basic_rag.py
Document App
	Make sure if "pypdf" library added in the requirements.txt
	pip install -r requirements.txt
	cd py/src/langchain
	python3 pdf_rag.py

Section 8: Summary API
<Diagram>
Create py/src/services/text folder
<Structure of POST request>
Modularize the "text" folder
	goto py/src/services/text folder
	create new file "__init__.py"
Test case
	create new file "summary.test.py"
	python3 py/src/services/text/summary.test.py

Create Lambda function "py-text-function"
	Change handler name from "lambda_function.lambda_handler" to "lambda_function.handler" in "Runtime Settings"
	Set timeout to 30 sec
	Permission -> Update existing Permission to get access to Bedrock service (policy.json attached)
Test Lambda
	Test event - use "test_event.json"
API Gateway and Lambda Integration
	New REST API - "SummaryApi"
		Craete resource POST "text"
		Create Method - POST 
		Lambda -> "py-text-function" (Enable Lambda Proxy Integration)
		Deploy the API - "prod" stage

Section 9: Image API
<Diagram>
Create py/src/services/image folder
Create s3 bucket to store the result image
Create py/src/services/image/image.py file
Modularize the "text" folder
	goto py/src/services/text folder
	create new file "__init__.py"
Test case
	create new file "image.test.py"
	python3 py/src/services/image/image.test.py
Create Lambda function "py-image-function"
	Change handler name from "lambda_function.lambda_handler" to "lambda_function.handler" in "Runtime Settings"
	Set timeout to 30 sec
	Permission -> Update existing Permission to get access to Bedrock service (policy.json attached)
Test Lambda
	Test Event - use "event.json"
API Gateway and Lambda Integration
	New REST API  -  "ImageApi"
		Craete resource POST "image"
		Create Method - POST 
		Lambda -> "py-image-function" (Enable Lambda Proxy Integration)
		Deploy the API - "prod" stage
VS Code - Extension
	REST Client -> Huachao Mao
		Create file "request.http"
			POST <API Gateway URL>
			Content-Type: application/json

			{
				"description": "a cat on a wall"
			}
			###
		Click on "Send Request button"

Section 10: Bedrock Knowledge bases
Bedrock Knowledge base is not free. Charge hourly based.
As of now KB supports only Anthropic Cluade Model
Create s3 bucket - "kbs3bucket"
	Upload the PDF 
Create Knowledge base
	Bedrock -> Orchectration -> Knowledge bases -> Create Knowledge base
				Name: "MyKB"
				IAM Permission: Create New role
				Data source: Select s3 bucket
				Embedding Model: Titan Embedding Model
				Vector Database: Quick Create new vector store (Amazon OpenSearch)
	Sync the Database
	Test the Knowledge base by selecting the Cluade model
	Note down the Knowledge base ID created
Create Lambda function locally
	Create folder & file "py/src/services/rag/rag.py"
	Note down 
		we are going to use "bedrock-agent-runtime" this time with RAG instead of "bedrock-runtime"
		modelArn format
	Test Lambda file "rag.test.py"
Create Lambda function in AWS - "py-rag-function"
	timeout
	Permission (policy.json)
	Create Test event (event.json)

API Gateway and Lambda Integration
	New REST API  -  "RAGApi"
		Craete resource POST "rag"
		Create Method - POST 
		Lambda -> "py-rag-function" (Enable Lambda Proxy Integration)
		Deploy the API - "prod" stage
VS Code - Extension
	REST Client -> Huachao Mao
		Create file "request.http"
			POST <API Gateway URL>
			Content-Type: application/json

			{
				"question": "your question here"
			}
			###
		Click on "Send Request button"
Clean up 
	Delete the Knowledge base created before
	Amazon OpenSearch service
		Serverless -> Collections -> Select the Collection and delete
			
Section 11: Bedrock custom Models
Very costly
Fine tuning
	Fine tuning of a base model -> custom model
	Fine-tuning trains a pretrained model on a new dataset without training from scratch
	<Diagram>
	<Example>
	Base Model vs Custom Model
		Base Model - Pay on request
		Custom Model - Training Job + Provisioned Throughput
			Feasible for complex use cases
			No worrried about the data privacy
			Can be used as any model - by model ID
	Build Custom Model
		Bedrock -> Foundation Models -> Custom Models
			Models -> Customize Model -> Create Fine-Tuning Job
				Select Source Model - Amazon Titan Text G1 - Lite 
				Model name - "MyCustomModel"
				Job Name - "MyJob"
				Input Data -> Input s3 bucket (json file with "prompt" and "completion" struture)
				Output Data -> Output s3 bucket to store the custom model
				Select Service Role
				"Create Fine-tuning job" button
				Note: After this custom model is created, you need to purchase Provisioned Throughput to be able to use this model
	Provisioned Throughput
		Bedrock -> Assessment & deployment -> Provisioned Throughput



