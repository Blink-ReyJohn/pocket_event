from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Enable CORS (e.g., for Zendesk AI integration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Simulated database
users = {
    "marktan@email.com": {
        "orders": [
            {"id": "ORD123", "item": "Running Shoes", "status": "Delivered"},
            {"id": "ORD124", "item": "Wireless Headphones", "status": "Delivered"}
        ]
    },
    "katrina.yu@email.com": {
        "orders": [
            {"id": "ORD125", "item": "Pediatric Appointment", "status": "Confirmed"}
        ]
    }
}

# Refund payload
class RefundRequest(BaseModel):
    user_id: str
    order_id: str
    reason_of_refund: str
    preferred_resolution: str

# ✅ List orders
@app.get("/api/orders")
async def list_orders(email: str):
    user = users.get(email)
    if user:
        return {"orders": user["orders"]}
    raise HTTPException(status_code=404, detail="User not found")

# ✅ Process refund
@app.post("/api/refund")
async def initiate_refund(data: RefundRequest):
    user = users.get(data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    order_found = any(order["id"] == data.order_id for order in user["orders"])
    if not order_found:
        raise HTTPException(status_code=404, detail="Order not found for this user")

    print(f"Refund request from {data.user_id}")
    print(f"- Order ID: {data.order_id}")
    print(f"- Reason: {data.reason_of_refund}")
    print(f"- Preferred Resolution: {data.preferred_resolution}")

    return {
        "message": "Refund request submitted",
        "user_id": data.user_id,
        "order_id": data.order_id,
        "reason": data.reason_of_refund,
        "resolution": data.preferred_resolution,
        "status": "processing"
    }

# Run locally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
