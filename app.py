from distutils.log import error
from lib2to3.pgen2 import token
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import mysql.connector
import uvicorn
import json
from datetime import datetime
import time



def timestamp(dt):
    return time.mktime(dt.timetuple()) + dt.microsecond / 1e6

app = FastAPI(title="Token Management")

class UserIN(BaseModel):
    tokenid: int = Field(...)
    count: int = Field(...)


class BaggageCount(BaseModel):
    count: int = Field(...)


class UserOUtToken(BaseModel):
    tokenid: int


class UserOUT(BaseModel):
    tokenid: int
    count: int
    status: bool
    time:float


@app.get('/')
async def index():
    return {"Hello": "Docker"}


@app.get('/getUser', response_model=List[UserOUT])
async def get_all_user():
    mydb = mysql.connector.connect(user="root",
            host="127.0.0.1", database="mysql", port=3306)    
    cursor = mydb.cursor()
    query = "select * FROM token"
    cursor.execute(query)
    
    results = cursor.fetchall()

    row_headers=[x[0] for x in cursor.description] 
    json_data=[]
    for result in results:
        json_data.append(dict(zip(row_headers,result)))
    
    cursor.close()
    return json_data

    
    
    
@app.get("/getActiveToken", response_model=List[UserOUtToken])
async def get_active_token():
    mydb = mysql.connector.connect(user="root",
            host="127.0.0.1", database="mysql", port=3306)    

    cursor = mydb.cursor()

    query = "SELECT tokenid FROM token WHERE STATUS =TRUE"
    cursor.execute(query)
    results = cursor.fetchall()
    row_headers=[x[0] for x in cursor.description]
    row_headers = row_headers * len(results)
    json_data=[]
    for result in results:
        json_data.append(dict(zip(row_headers,result)))




    cursor.close()
    return json_data
    


@app.get('/getAvailableToken', response_model=BaggageCount)
async def get_available_token():
    mydb = mysql.connector.connect(user="root",
            host="127.0.0.1", database="mysql", port=3306)    

    cursor = mydb.cursor()
    query = "SELECT COUNT(tokenid) as count FROM token WHERE STATUS =FALSE"
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    return {"count":result[0]}


@app.get("/getUser/{id}", response_model=UserOUT)
async def get_by_id(id: int = -1):
    
    mydb = mysql.connector.connect(user="root",
            host="127.0.0.1", database="mysql", port=3306)    

    cursor = mydb.cursor()
    query = "SELECT * FROM token WHERE tokenid=" + str(id)
    cursor.execute(query)
    result = cursor.fetchone()
    row_headers=[x[0] for x in cursor.description] 
    
    dic = {}
    for i in range(len(result)):
        dic[row_headers[i]] = result[i]
        
    
    if result is None:
        raise HTTPException(status_code=404, detail="Data not found")

    return dic


@app.post('/createUser', response_model=UserOUT)
async def create_user(r: UserIN):
    mydb = mysql.connector.connect(user="root",
            host="127.0.0.1", database="mysql", port=3306)    
    cursor = mydb.cursor()
    
    query = "INSERT INTO token (tokenid,count,status,time) VALUES (%s,%s,%s,%s)" 

    cursor.execute(query, (r.tokenid, r.count, 1, 50.05))
    mydb.commit()
    mydb.close()

    return await get_by_id(r.tokenid)


@app.delete('/delete/{id}')
async def delete_by_id(id: int):
    mydb = mysql.connector.connect(user="root",
            host="127.0.0.1", database="mysql", port=3306)    
    cursor = mydb.cursor()
    query = "DELETE FROM token where tokenid=" + str(id)

    cursor.execute(query)
    mydb.commit()
    mydb.close()
    return {"Message": "Successfully deleted"}
    


@app.put('/updateBaggageCount/{id}', response_model=UserOUT)
async def update_baggage_count(id: int, r: BaggageCount = Depends()):
    mydb = mysql.connector.connect(user="root",
            host="127.0.0.1", database="mysql", port=3306)    
    cursor = mydb.cursor()
    query = "UPDATE token set count="+str(r.count) + ", time="+ str(timestamp(datetime.now()))+" WHERE tokenid="+str(id)
    cursor.execute(query)
    mydb.commit()
    mydb.close()
    

    return await get_by_id(id)



