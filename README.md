# FastAPI Creative Approval Service 
This project accepts image uploads such as PNG, JPEG and small GIF and validates them based on rules that returns either APPROVED, REJECTED ot REQUIRES_REVIEW.
This service is designed to use deterministic and lightweight heuristics and does not reuire external paid services or heavy ML.

## Required Dependencies 
* Python 3.11+
* FastAPI
* Pillow
* python-multipart
* Uvicorn
* pytest


You'll need to be using Python 3.11+
If you do not already have this, run:
  ```bash
brew install python@3.11
```

## Running Locally
It's recommended to use a virtual environment rather than global. The virtual enviroment prevents interference from other python projects and keeps your packages and dependencies contained in one environment.
Use the following commands to build and run locally and virtually.
 First clone the repo:
  ```bash
git clone https://github.com/yusurmusse/fastapi-creative-approval-project
cd <fastapi-creative-approval-project>
```
Create a virtual environment:
  ```bash
python3 -m venv venv
```
Then activate the virtual enviroment:

For Linux/Mac run:
  ```bash
source venv/bin/activate
```
For Windows run:
  ```bash
venv\Scripts\activate
```
> ℹ️ When activated your bash script should look like: **(venv) ➜ project_name**

Install the required dependencies:
  ```bash
pip install -r requirements.txt
```
Run FastAPI locally using this command:
  ```bash
uvicorn src.main:app --reload
```

## Running in Docker
You'll need to build a docker image:
  ```bash
docker build -t <insert_docker_image_name> .
```
Then run the container:
  ```bash
docker run -p 8000:8000 <insert_docker_image_name>
```
The API will be available at <http://localhost:8000> 
The health status will be available at <http://localhost:8000/health>
OpenAPI docs are avaialable at <http://localhost:8000/docs>

## Rules I Implemented
1. Format Checker: Only accepts PNG and JPEG and rejects all other unsupported format
2. GIF Size Checker: Small GIFs are allowed but oversized GIFs are rejected. Input requires small GIFs only.
3. Minimum Size Checker: Rejects images smaller than 300x250 pixels.
4. Ratio Size Checker: Ratio has to be between 0.7-2.5. Any figure outside this would be flagged as REQUIRES_REVIEW.
5. Legality and Contrast Checker: Images that are too dark or low in contrast will be flagged up as REQUIRES_REVIEW.

> ℹ️ Rules were interpreted from the docs provided. Clause: *“Posters and other promotional media in public places… must comply with rules ensuring ads are honest, **clear**, and not likely to cause harm or offence.”*

## Design Decisions and Trade-offs
* For simplicity of this project, ML was not used but instead deterministic heuristics to be easy to use offline too
* Rules 4 and 5 above are dependent on each use case hence why it REQUIRES_REVIEW. It's not automatically blocked or rejected and needs manual checking.
* The figures used to calculate ratio and image sizes are rough estimates used for simplicity for this project.
* Brightness and contrast of images can be further evaluated and analysed.
* Optional use case of OpenAI integration can be used in the project. If I were to implement OpenAI, I would make it summarise the policy docs to given more reasoning to my rules as to why it gave the given reponse status.












