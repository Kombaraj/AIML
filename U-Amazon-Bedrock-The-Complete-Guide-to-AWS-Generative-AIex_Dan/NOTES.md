Learning: Udemy
Course: Amazon Bedrock - The Complete Guide to AWS Generative AI
Author: Alex Dan
GitHub: https://github.com/alexhddev/Bedrock_course.git


Section 2 - Introduction to Amazon Bedrock & Tools setup


===> py\src\intro\steps.txt

python environment setup

#### Create environment
```
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
	py/src/images/stability.py

	py/src/images/titan/generate.py
	py/src/images/titan/inpaint.py

Section 5: Amazon Bedrock Embedding Models

py/src/embed/sample.py

Text Embedding:
python3 \src\embed\text.py

Image Embedding:
python3 \src\embed\image.py

Vector Database:


Section 7: Project RAG

Local RAG app and LangChain

	Local RAG App - Chat with your data
	Integrate Bedrock with LangChain
	
First Chain
	Go inside PY folder
		pip install -r requirements.txt
		python3 first_chain.py
Basic RAG app
    Make sure if "faiss-cpu" library added in the requirements.txt
	pip install -r requirements.txt
	python3 basic_rag.py
Document App
	Make sure if "pypdf" library added in the requirements.txt
	pip install -r requirements.txt
	python3 pdf_rag.py

Section 8: Summary API
PY/src/services/text

