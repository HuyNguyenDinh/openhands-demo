from behave import given, when, then
from fastapi.testclient import TestClient
import uuid
from app.main import app
from app.database.config import Base, engine, get_db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

def before_scenario(context, scenario):
    context.client = TestClient(app)
    context.tokens = {}

@given('the push notification service is running')
def step_impl(context):
    response = context.client.get("/docs")
    assert response.status_code == 200

@when('I register a new {platform} token with the following details')
def step_impl(context, platform):
    row = context.table[0]
    context.token_data = {
        "user_id": row["user_id"],
        "token": row["token"],
        "platform": row["platform"]
    }
    context.response = context.client.post("/api/v1/tokens", json=context.token_data)

@then('the response status code should be {status_code:d}')
def step_impl(context, status_code):
    assert context.response.status_code == status_code

@then('the response should contain the token details')
def step_impl(context):
    data = context.response.json()
    assert data["user_id"] == context.token_data["user_id"]
    assert data["token"] == context.token_data["token"]
    assert data["platform"] == context.token_data["platform"]
    assert uuid.UUID(data["id"])
    context.token_id = data["id"]

@then('the token should be stored in the database')
def step_impl(context):
    response = context.client.get(f"/api/v1/tokens/{context.token_data['user_id']}")
    assert response.status_code == 200
    tokens = response.json()
    assert any(
        token["id"] == context.token_id
        for token in tokens
    )

@given('the following tokens exist for user "{user_id}"')
def step_impl(context, user_id):
    for row in context.table:
        token_data = {
            "user_id": user_id,
            "token": row["token"],
            "platform": row["platform"]
        }
        response = context.client.post("/api/v1/tokens", json=token_data)
        assert response.status_code == 200
        context.tokens[response.json()["id"]] = token_data

@when('I request all tokens for user "{user_id}"')
def step_impl(context, user_id):
    context.response = context.client.get(f"/api/v1/tokens/{user_id}")

@then('the response should contain {count:d} tokens')
def step_impl(context, count):
    data = context.response.json()
    assert len(data) == count

@then('the tokens should match the stored tokens')
def step_impl(context):
    data = context.response.json()
    stored_tokens = set(token["token"] for token in data)
    expected_tokens = set(token["token"] for token in context.tokens.values())
    assert stored_tokens == expected_tokens

@given('a token exists with the following details')
def step_impl(context):
    row = context.table[0]
    token_data = {
        "user_id": row["user_id"],
        "token": row["token"],
        "platform": row["platform"]
    }
    response = context.client.post("/api/v1/tokens", json=token_data)
    assert response.status_code == 200
    context.token_id = response.json()["id"]
    context.token_data = token_data

@when('I delete the token')
def step_impl(context):
    context.response = context.client.delete(f"/api/v1/tokens/{context.token_id}")

@then('the token should be removed from the database')
def step_impl(context):
    response = context.client.get(f"/api/v1/tokens/{context.token_data['user_id']}")
    assert response.status_code == 200
    tokens = response.json()
    assert not any(
        token["id"] == context.token_id
        for token in tokens
    )

@when('I register the same token again')
def step_impl(context):
    context.response = context.client.post("/api/v1/tokens", json=context.token_data)

@then('the response should contain the same token ID')
def step_impl(context):
    data = context.response.json()
    assert data["id"] == context.token_id

@when('I try to delete a non-existent token')
def step_impl(context):
    non_existent_id = str(uuid.uuid4())
    context.response = context.client.delete(f"/api/v1/tokens/{non_existent_id}")

@when('I register a token with an invalid platform')
def step_impl(context):
    row = context.table[0]
    token_data = {
        "user_id": row["user_id"],
        "token": row["token"],
        "platform": row["platform"]
    }
    context.response = context.client.post("/api/v1/tokens", json=token_data)