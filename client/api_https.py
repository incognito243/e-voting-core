from fastapi import FastAPI, HTTPException
from entity.voting_server import VotingServer
from fastapi.middleware.cors import CORSMiddleware
from entity.user import User
from pydantic import BaseModel
import os

class CreateVotingServerRequest(BaseModel):
    number_of_candidates: int
    maximum_number_of_voters: int
    server_name: str

class CreateUserRequest(BaseModel):
    user_name: str

class CreateUserResponse(BaseModel):
    user_id: str

class VoteRequest(BaseModel):
    user_id: str
    server_id: str
    candidate_id: int

class OpenVoteRequest(BaseModel):
    server_id: str
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for servers and users
voting_servers = {}
users = {}

value_a = os.environ.get("ECC_A")
value_b = os.environ.get("ECC_B")
value_p = os.environ.get("ECC_P")
value_order = os.environ.get("ECC_ORDER")

@app.post("/internal/v1/create_voting_server")
def create_voting_server(request: CreateVotingServerRequest):
    server_id = f"server_{request.server_name}_{len(voting_servers) + 1}"
    voting_servers[server_id] = VotingServer(
        _number_of_candidate=request.number_of_candidates,
        maximum_number_of_voter=request.maximum_number_of_voters,
        value_a=int(value_a),
        value_b=int(value_b),
        value_p=int(value_p),
        value_order=int(value_order),
    )
    return {"server_id": server_id}

@app.get("/internal/v1/voting_server/is_exist/{server_id}")
def voting_server_is_exist(server_id: str):
    if server_id in voting_servers:
        return {"exists": True}
    else:
        return {"exists": False}

@app.post("/internal/v1/create_user")
def create_user(request: CreateUserRequest):
    user_id = f"user_{request.user_name}_{len(users) + 1}"
    users[user_id] = User(request.user_name)
    return CreateUserResponse(user_id=user_id)

@app.get("/internal/v1/is_exist/{user_id}")
def is_exist(user_id: str):
    if user_id in users:
        return {"exists": True}
    else:
        return {"exists": False}

@app.post("/internal/v1/vote")
def vote(request: VoteRequest):
    if request.server_id not in voting_servers:
        raise HTTPException(status_code=404, detail="Voting server not found")
    if request.user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    server = voting_servers[request.server_id]
    user = users[request.user_id]

    try:
        user_vote = user.vote(request.candidate_id, server.get_public_key())
        server.cast_vote(user_vote)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": "Vote cast successfully"}

@app.post("/internal/v1/open_vote")
def open_vote(request: OpenVoteRequest):
    if request.server_id not in voting_servers:
        raise HTTPException(status_code=404, detail="Voting server not found")

    server = voting_servers[request.server_id]
    try:
        results = server.open_vote()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"results": results}

@app.get("/internal/v1/publish_result/{server_id}")
def publish_result(server_id: str):
    if server_id not in voting_servers:
        raise HTTPException(status_code=404, detail="Voting server not found")

    server = voting_servers[server_id]
    return server.public_result()