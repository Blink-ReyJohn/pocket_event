from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS (e.g., for Zendesk or frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Mock database
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

# ✅ List orders by user
@app.get("/api/orders")
async def list_orders(email: str):
    user = users.get(email)
    if user:
        return {"orders": user["orders"]}
    raise HTTPException(status_code=404, detail="User not found")

# ✅ Refund request via URL params
@app.get("/api/refund")
async def initiate_refund(
    order_id: str,
    reason_of_refund: str,
    preferred_resolution: str
):
    # Find which user owns the order
    for email, data in users.items():
        for order in data["orders"]:
            if order["id"] == order_id:
                print(f"Refund request from {email}")
                print(f"- Order ID: {order_id}")
                print(f"- Reason: {reason_of_refund}")
                print(f"- Resolution: {preferred_resolution}")

                return {
                    "message": "Refund request submitted",
                    "user_id": email,
                    "order_id": order_id,
                    "reason": reason_of_refund,
                    "resolution": preferred_resolution,
                    "status": "processing"
                }

    raise HTTPException(status_code=404, detail="Order ID not found for any user")

# Mock transactions database
transactions = [
    {
        "transaction_id": "TXN001",
        "email": "carlos.reyes@email.com",
        "amount": 5000,
        "due_date": "2025-06-30",
        "status": "Paid",
        "discrepancy": False
    },
    {
        "transaction_id": "TXN002",
        "email": "carlos.reyes@email.com",
        "amount": 5000,
        "due_date": "2025-07-30",
        "status": "Unpaid",
        "discrepancy": False
    }
]

# GET: List a user's loan transactions
@app.get("/api/loans")
async def list_loans(email: str):
    if email not in users:
        raise HTTPException(status_code=404, detail="User not found.")
    
    user_loans = [txn for txn in transactions if txn["email"] == email]
    
    if not user_loans:
        raise HTTPException(status_code=404, detail="No loan records found for this user.")
    
    return {"loans": user_loans}

# POST: Flag a loan transaction as having a discrepancy
@app.post("/api/loans/discrepancy")
async def report_discrepancy(email: str, transaction_id: str):
    if email not in users:
        raise HTTPException(status_code=404, detail="User not found.")

    for txn in transactions:
        if txn["transaction_id"] == transaction_id and txn["email"] == email:
            txn["discrepancy"] = True
            return {
                "message": "Discrepancy flagged for manual review.",
                "transaction_id": transaction_id,
                "status": "flagged"
            }
    
    raise HTTPException(status_code=404, detail="Transaction not found for this user.")

# Local dev runner
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
