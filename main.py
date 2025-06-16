from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Mock DB
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

# ✅ List Orders
@app.get("/api/orders")
async def list_orders(email: str):
    user = users.get(email)
    if user:
        return {"orders": user["orders"]}
    raise HTTPException(status_code=404, detail="User not found")

# ✅ Refund via URL Params
@app.get("/api/refund")
async def initiate_refund(
    user_id: str,
    order_id: str,
    reason_of_refund: str,
    preferred_resolution: str
):
    user = users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    order_found = any(order["id"] == order_id for order in user["orders"])
    if not order_found:
        raise HTTPException(status_code=404, detail="Order not found for this user")

    print(f"Refund request from {user_id}")
    print(f"- Order ID: {order_id}")
    print(f"- Reason: {reason_of_refund}")
    print(f"- Resolution: {preferred_resolution}")

    return {
        "message": "Refund request submitted",
        "user_id": user_id,
        "order_id": order_id,
        "reason": reason_of_refund,
        "resolution": preferred_resolution,
        "status": "processing"
    }

# Local dev
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
