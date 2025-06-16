from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Enable CORS (optional if connecting from Zendesk or browser client)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Simulated database
users = {
    "marktan@email.com": {
        "verified": True,
        "orders": [
            {"id": "ORD123", "item": "Running Shoes", "status": "Delivered"},
            {"id": "ORD124", "item": "Wireless Headphones", "status": "Delivered"}
        ]
    },
    "katrina.yu@email.com": {
        "verified": True,
        "orders": [
            {"id": "ORD125", "item": "Pediatric Appointment", "status": "Confirmed"}
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

# API to send verification (simulated)
@app.post("/api/send-verification")
async def send_verification(data: EmailInput):
    email = data.email
    if email not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"Verification email sent to {email}", "status": "success"}

# API to verify user manually (for demo/testing)
@app.get("/api/verify-user")
async def verify_user(email: str):
    if email in users:
        users[email]["verified"] = True
        return {"message": "User verified", "status": "success"}
    raise HTTPException(status_code=404, detail="User not found")

# API to list orders if user is verified
@app.get("/api/orders")
async def list_orders(email: str):
    user = users.get(email)
    if user and user["verified"]:
        return {"orders": user["orders"]}
    raise HTTPException(status_code=403, detail="User not verified or not found")

# API to initiate refund based only on order_id
@app.post("/api/refund")
async def initiate_refund(data: RefundRequest):
    user_email = None

    # Search for the order ID across all users
    for email, user_data in users.items():
        for order in user_data["orders"]:
            if order["id"] == data.order_id:
                user_email = email
                break
        if user_email:
            break

    if not user_email:
        raise HTTPException(status_code=404, detail="Order ID not found")

    # Simulate refund processing
    print(f"Refund requested for Order {data.order_id}")
    print(f"- Found associated user: {user_email}")
    print(f"- Reason: {data.reason}")
    print(f"- Resolution: {data.preferred_resolution}")

    return {
        "message": "Refund request received",
        "order_id": data.order_id,
        "user_email": user_email,
        "status": "processing"
    }

# Local run command
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
