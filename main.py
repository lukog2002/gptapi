from fastapi import FastAPI , Request 
from fastapi.middleware.cors import CORSMiddleware
from dbconfig import insertData , retrieveAllData , deleteApp
import json 
import openai 
import time
openai.api_key = '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'
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def getGptResponse(prompt) : 
    # Returning a sampling string as a response 
    # time.sleep(5)
    # return f"""
    #     Elon Musk is a co-founder of six companies, namely Tesla, SpaceX, and Boring Company. His ownership in Tesla amounts to around 23% through stock and options, but he has utilized over 50% of his shares as collateral for loans.Elon Musk is a co-founder of six companies, namely Tesla, SpaceX, and Boring Company. His ownership in Tesla amounts to around 23% through stock and options, but he has utilized over 50% of his shares as collateral for loans.
    # """
    response = openai.Completion.create(
        engine = 'text-davinci-003' , 
        prompt = prompt , 
        temperature = 0.7 , 
        max_tokens=100
    )
    res = response.choices[0].text
    print(res)
    return res

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post('/' , tags=["lukog"]) 
async def root(request : Request) : 
    data = await request.json() 
    return {"print" : "pong"} 

@app.post('/createapp')
async def postDetails(request : Request) : 
    data = await request.json() 
    responseText = getGptResponse(data['prompt'])
    data['response'] = responseText
    if insertData(data) == "inserted" : 
        return {"msg" : "inserted" , "response" : responseText}
    return {"msg" : "app-name exits" } 

@app.post('/output') 
async def getOutput(request : Request) : 
    prompt = await request.json() 
    responseText = getGptResponse(prompt)
    return {"status" : "success" , "response" : responseText} 

@app.post('/deleteapp/{appname}')
def delete_app(appname : str , request : Request) : 
    deleteApp(appname)
    return {"msg" : "deleted"}

@app.get('/getallapps')
async def getAllApps() : 
    data = retrieveAllData()
    return json.dumps(data)

