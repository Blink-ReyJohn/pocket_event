from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Allow CORS (for external integrations like Zendesk)
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
    },
    "katrina.yu@email.com": {
        "verified": False,
        "orders": [
            {"id": "ORD125", "item": "Pediatric Appointment", "status": "Confirmed"}
        ]
    }
}

# Refund request schema
class RefundRequest(BaseModel):
    order_id: str
    reason: str
    preferred_resolution: str

# ✅ Send verification email (GET with email in query string)
@app.get("/api/send-verification")
async def send_verification(email: str):
    if email not in users:
        raise HTTPException(status_code=404, detail="User not found")
    print(f"Verification email sent to {email}")
    return {"message": f"Verification email sent to {email}", "status": "success"}

# ✅ Verify user (GET with email in query string)
@app.get("/api/verify-user")
async def verify_user(email: str):
    if email in users:
        users[email]["verified"] = True
        return {"message": "User verified", "status": "success"}
    raise HTTPException(status_code=404, detail="User not found")

# ✅ List orders (GET with email in query string)
@app.get("/api/orders")
async def list_orders(email: str):
    user = users.get(email)
    if user and user["verified"]:
        return {"orders": user["orders"]}
    raise HTTPException(status_code=403, detail="User not verified or not found")

# ✅ Initiate refund (POST with body)
@app.post("/api/refund")
async def initiate_refund(data: RefundRequest):
    user_email = None

    # Search across users for the order
    for email, user_data in users.items():
        for order in user_data["orders"]:
            if order["id"] == data.order_id:
                user_email = email
                break
        if user_email:
            break

    if not user_email:
        raise HTTPException(status_code=404, detail="Order ID not found")

    # Simulate refund process
    print(f"Refund for Order {data.order_id} by {user_email}")
    print(f"- Reason: {data.reason}")
    print(f"- Resolution: {data.preferred_resolution}")

    return {
        "message": "Refund request received",
        "order_id": data.order_id,
        "user_email": user_email,
        "status": "processing"
    }

# For local dev/testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
