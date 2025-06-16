from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI()

# Allow CORS (Optional for frontend or AI Agent integration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Mock database
users = {
    "marktan@email.com": {
        "verified": False,
        "orders": [
            {"id": "ORD123", "item": "Running Shoes", "status": "Delivered"},
            {"id": "ORD124", "item": "Wireless Headphones", "status": "Delivered"}
        ]
    }
}

# Request Models
class EmailInput(BaseModel):
    email: str

class RefundRequest(BaseModel):
    order_id: str
    reason: str
    preferred_resolution: str
    user_email: str

# Endpoints

@app.post("/api/send-verification")
async def send_verification(data: EmailInput):
    email = data.email
    if email not in users:
        raise HTTPException(status_code=404, detail="User not found")
    # Simulate sending verification
    return {"message": f"Verification email sent to {email}", "status": "success"}

@app.get("/api/verify-user")
async def verify_user(email: str):
    if email in users:
        users[email]["verified"] = True
        return {"message": "User verified", "status": "success"}
    raise HTTPException(status_code=404, detail="User not found")

@app.get("/api/orders")
async def list_orders(email: str):
    user = users.get(email)
    if user and user["verified"]:
        return {"orders": user["orders"]}
    raise HTTPException(status_code=403, detail="User not verified or not found")

@app.post("/api/refund")
async def initiate_refund(data: RefundRequest):
    if data.user_email not in users:
        raise HTTPException(status_code=404, detail="User not found")

    # Simulate refund process
    print(f"Refund requested for Order {data.order_id}")
    print(f"- Reason: {data.reason}")
    print(f"- Resolution: {data.preferred_resolution}")

    return {
        "message": "Refund request received",
        "order_id": data.order_id,
        "status": "processing"
    }

# For local testing
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
