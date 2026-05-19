from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uuid

app = FastAPI(title="ShopMint Backend - In-Memory DB")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Comprehensive In-Memory Database (~100 items)
# Using direct, verified Unsplash image IDs for maximum reliability
INVENTORY = {
    # ELECTRONICS (1-12)
    1: {"id": 1, "name": "MintBook Air Pro (16GB/512GB SSD)", "price": 89999, "stock": 4, "category": "Electronics", "image": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500"},
    2: {"id": 2, "name": "ShopMint Pods Wireless ANC Headphones", "price": 14999, "stock": 8, "category": "Electronics", "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500"},
    3: {"id": 3, "name": "MintWatch Chrono Series 2 (GPS)", "price": 34999, "stock": 5, "category": "Electronics", "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500"},
    4: {"id": 4, "name": "ShopMint Ergo Mechanical Keyboard", "price": 6499, "stock": 12, "category": "Electronics", "image": "https://images.unsplash.com/photo-1511467687858-23d96c32e4ae?w=500"},
    5: {"id": 5, "name": "MintSound Atmos Soundbar", "price": 24999, "stock": 6, "category": "Electronics", "image": "https://images.unsplash.com/photo-1545454675-3531b543be5d?w=500"},
    6: {"id": 6, "name": "MintCam DSLR 4K Camera", "price": 75999, "stock": 3, "category": "Electronics", "image": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=500"},
    7: {"id": 7, "name": "MintTab Pro 12.9-inch", "price": 69999, "stock": 7, "category": "Electronics", "image": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=500"},
    8: {"id": 8, "name": "ShopMint Precision Wireless Mouse", "price": 2499, "stock": 20, "category": "Electronics", "image": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=500"},
    9: {"id": 9, "name": "MintLink Mesh Wi-Fi 6 Router", "price": 12999, "stock": 10, "category": "Electronics", "image": "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=500"},
    10: {"id": 10, "name": "MintMonitor 32-inch 4K UHD", "price": 42999, "stock": 5, "category": "Electronics", "image": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=500"},
    11: {"id": 11, "name": "MintPower 20000mAh Power Bank", "price": 2999, "stock": 15, "category": "Electronics", "image": "https://images.unsplash.com/photo-1621330396173-e41b1cafd17f?w=500"},
    12: {"id": 12, "name": "MintHub 10-in-1 USB-C Dock", "price": 5499, "stock": 8, "category": "Electronics", "image": "https://images.unsplash.com/photo-1468495244123-6a6c332eeede?w=500"},

    # MOBILES (13-24)
    13: {"id": 13, "name": "MintPhone 16 Pro Max Ultra", "price": 119999, "stock": 3, "category": "Mobiles", "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500"},
    14: {"id": 14, "name": "MintPhone 15 (128GB)", "price": 69999, "stock": 10, "category": "Mobiles", "image": "https://images.unsplash.com/photo-1523206489230-c012c64b2b48?w=500"},
    15: {"id": 15, "name": "MintPhone SE 2024", "price": 32999, "stock": 15, "category": "Mobiles", "image": "https://images.unsplash.com/photo-1592890288564-76628a30a657?w=500"},
    16: {"id": 16, "name": "MintPhone Flip Foldable", "price": 84999, "stock": 4, "category": "Mobiles", "image": "https://images.unsplash.com/photo-1592890288564-76628a30a657?w=500"},
    17: {"id": 17, "name": "MintPhone Fold Pro", "price": 149999, "stock": 2, "category": "Mobiles", "image": "https://images.unsplash.com/photo-1580910051074-3eb6948865c5?w=500"},
    18: {"id": 18, "name": "MintPhone Lite (64GB)", "price": 19999, "stock": 25, "category": "Mobiles", "image": "https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?w=500"},
    19: {"id": 19, "name": "MintPhone Neo 5G", "price": 27999, "stock": 12, "category": "Mobiles", "image": "https://images.unsplash.com/photo-1546054454-aa26e2b734c7?w=500"},
    20: {"id": 20, "name": "MintPhone Prime Edition", "price": 45999, "stock": 8, "category": "Mobiles", "image": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500"},
    21: {"id": 21, "name": "MintPhone Ultra S", "price": 99999, "stock": 5, "category": "Mobiles", "image": "https://images.unsplash.com/photo-1567581935884-3349723552ca?w=500"},
    22: {"id": 22, "name": "MintPhone Vision AI", "price": 54999, "stock": 6, "category": "Mobiles", "image": "https://images.unsplash.com/photo-1574757565909-b493722e04d3?w=500"},
    23: {"id": 23, "name": "MintPhone Z Crystal", "price": 72999, "stock": 3, "category": "Mobiles", "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500"},
    24: {"id": 24, "name": "MintPhone X Classic", "price": 49999, "stock": 10, "category": "Mobiles", "image": "https://images.unsplash.com/photo-1525598912003-663126343e1f?w=500"},

    # FASHION (25-36)
    25: {"id": 25, "name": "Premium Slim-Fit Denim Jacket", "price": 3499, "stock": 15, "category": "Fashion", "image": "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=500"},
    26: {"id": 26, "name": "Classic Minimalist Leather Chronograph", "price": 5999, "stock": 7, "category": "Fashion", "image": "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=500"},
    27: {"id": 27, "name": "Organic Cotton Crew Neck T-Shirt", "price": 999, "stock": 30, "category": "Fashion", "image": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500"},
    28: {"id": 28, "name": "Slim Fit Stretch Chinos", "price": 2499, "stock": 20, "category": "Fashion", "image": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=500"},
    29: {"id": 29, "name": "Handcrafted Leather Chelsea Boots", "price": 7999, "stock": 5, "category": "Fashion", "image": "https://images.unsplash.com/photo-1638247025967-b4e38f787b76?w=500"},
    30: {"id": 30, "name": "Pure Silk Patterned Scarf", "price": 1499, "stock": 12, "category": "Fashion", "image": "https://images.unsplash.com/photo-1520903920243-00d872a2d1c9?w=500"},
    31: {"id": 31, "name": "Merino Woolen Sweater", "price": 3999, "stock": 10, "category": "Fashion", "image": "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=500"},
    32: {"id": 32, "name": "Pro-Run Breathable Sneakers", "price": 4999, "stock": 18, "category": "Fashion", "image": "https://images.unsplash.com/photo-1542291026-7eec264c2744?w=500"},
    33: {"id": 33, "name": "Tailored Three-Piece Formal Suit", "price": 15999, "stock": 4, "category": "Fashion", "image": "https://images.unsplash.com/photo-1594932224030-9409841f393e?w=500"},
    34: {"id": 34, "name": "Streetwear Oversized Hoodie", "price": 2999, "stock": 22, "category": "Fashion", "image": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=500"},
    35: {"id": 35, "name": "Floral Summer Chiffon Dress", "price": 3299, "stock": 15, "category": "Fashion", "image": "https://images.unsplash.com/photo-1585487000160-6ebcfceb0d03?w=500"},
    36: {"id": 36, "name": "Urban Explorer Cargo Pants", "price": 2799, "stock": 20, "category": "Fashion", "image": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=500"},

    # APPLIANCES (37-48)
    37: {"id": 37, "name": "Smart Frost-Free Double Door Refrigerator", "price": 45990, "stock": 2, "category": "Appliances", "image": "https://images.unsplash.com/photo-1571175432248-5212dad51025?w=500"},
    38: {"id": 38, "name": "Intelligent Inverter Front Load Washer", "price": 38990, "stock": 4, "category": "Appliances", "image": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=500"},
    39: {"id": 39, "name": "Digital Convection Microwave Oven", "price": 12499, "stock": 8, "category": "Appliances", "image": "https://images.unsplash.com/photo-1574269909862-7e1d70bb8078?w=500"},
    40: {"id": 40, "name": "Split AC with Inverter Technology", "price": 32999, "stock": 5, "category": "Appliances", "image": "https://images.unsplash.com/photo-1631541909061-71e349d1f203?w=500"},
    41: {"id": 41, "name": "Cordless Stick Vacuum Cleaner", "price": 18999, "stock": 6, "category": "Appliances", "image": "https://images.unsplash.com/photo-1527515637462-cff94eecc1ac?w=500"},
    42: {"id": 42, "name": "HEPA Filter Smart Air Purifier", "price": 14999, "stock": 10, "category": "Appliances", "image": "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=500"},
    43: {"id": 43, "name": "Built-in Efficient Dishwasher", "price": 42999, "stock": 3, "category": "Appliances", "image": "https://images.unsplash.com/photo-1584622781564-1d9876a13d1a?w=500"},
    44: {"id": 44, "name": "Automatic Bean-to-Cup Coffee Maker", "price": 24999, "stock": 7, "category": "Appliances", "image": "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=500"},
    45: {"id": 45, "name": "Retro Style 2-Slice Toaster", "price": 3499, "stock": 15, "category": "Appliances", "image": "https://images.unsplash.com/photo-1584905066893-7d5c142ba4e1?w=500"},
    46: {"id": 46, "name": "Fast-Boil Electric Glass Kettle", "price": 2999, "stock": 20, "category": "Appliances", "image": "https://images.unsplash.com/photo-1594212699903-ec8a3eca50f5?w=500"},
    47: {"id": 47, "name": "Portable Induction Cooktop", "price": 4999, "stock": 12, "category": "Appliances", "image": "https://images.unsplash.com/photo-1583248356463-e3170e179e8c?w=500"},
    48: {"id": 48, "name": "Pro-Master Food Processor", "price": 8999, "stock": 10, "category": "Appliances", "image": "https://images.unsplash.com/photo-1591130901020-ef93581c8fb9?w=500"},

    # SPORTS (49-60)
    49: {"id": 49, "name": "Carbon Fiber Road Bike", "price": 124999, "stock": 2, "category": "Sports", "image": "https://images.unsplash.com/photo-1485965120184-e220f721d03e?w=500"},
    50: {"id": 50, "name": "Professional Indoor Treadmill", "price": 54999, "stock": 4, "category": "Sports", "image": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=500"},
    51: {"id": 51, "name": "Adjustable Dumbbell Set (20kg)", "price": 8999, "stock": 12, "category": "Sports", "image": "https://images.unsplash.com/photo-1583454110551-21f2fa2ec617?w=500"},
    52: {"id": 52, "name": "Premium Yoga Mat with Carry Strap", "price": 1999, "stock": 25, "category": "Sports", "image": "https://images.unsplash.com/photo-1592432676556-311736332152?w=500"},
    53: {"id": 53, "name": "Official Size Match Football", "price": 2499, "stock": 18, "category": "Sports", "image": "https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=500"},
    54: {"id": 54, "name": "Tennis Racket Graphite Series", "price": 5499, "stock": 10, "category": "Sports", "image": "https://images.unsplash.com/photo-1592709823125-a191f07a2a5e?w=500"},
    55: {"id": 55, "name": "Outdoor Camping Tent (4 Person)", "price": 12999, "stock": 6, "category": "Sports", "image": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=500"},
    56: {"id": 56, "name": "High-Impact Basketball Shoes", "price": 6999, "stock": 15, "category": "Sports", "image": "https://images.unsplash.com/photo-1515955656352-a1fa3ffcd111?w=500"},
    57: {"id": 57, "name": "Speed Skipping Rope with Counter", "price": 799, "stock": 40, "category": "Sports", "image": "https://images.unsplash.com/photo-1544033527-b192daee1f5b?w=500"},
    58: {"id": 58, "name": "Hydration Bladder Backpack", "price": 3499, "stock": 10, "category": "Sports", "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500"},
    59: {"id": 59, "name": "Pro-Grip Badminton Set", "price": 2999, "stock": 12, "category": "Sports", "image": "https://images.unsplash.com/photo-1626225967045-97a3a2a62ae5?w=500"},
    60: {"id": 60, "name": "Swimming Goggles Anti-Fog", "price": 999, "stock": 30, "category": "Sports", "image": "https://images.unsplash.com/photo-1518173946687-a4c8892bbd9f?w=500"},

    # BOOKS (61-72)
    61: {"id": 61, "name": "The Alchemist - Paulo Coelho", "price": 499, "stock": 50, "category": "Books", "image": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=500"},
    62: {"id": 62, "name": "Atomic Habits - James Clear", "price": 599, "stock": 45, "category": "Books", "image": "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=500"},
    63: {"id": 63, "name": "Thinking, Fast and Slow", "price": 699, "stock": 30, "category": "Books", "image": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=500"},
    64: {"id": 64, "name": "Sapiens: A Brief History of Humankind", "price": 799, "stock": 25, "category": "Books", "image": "https://images.unsplash.com/photo-1585829645821-30dc5a47e273?w=500"},
    65: {"id": 65, "name": "The Great Gatsby - F. Scott Fitzgerald", "price": 399, "stock": 20, "category": "Books", "image": "https://images.unsplash.com/photo-1543004218-ee141104975a?w=500"},
    66: {"id": 66, "name": "1984 - George Orwell", "price": 349, "stock": 40, "category": "Books", "image": "https://images.unsplash.com/photo-1541963463532-d68292c34b19?w=500"},
    67: {"id": 67, "name": "Brave New World - Aldous Huxley", "price": 449, "stock": 15, "category": "Books", "image": "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=500"},
    68: {"id": 68, "name": "The Psychology of Money", "price": 549, "stock": 35, "category": "Books", "image": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=500"},
    69: {"id": 69, "name": "Man's Search for Meaning", "price": 499, "stock": 20, "category": "Books", "image": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=500"},
    70: {"id": 70, "name": "Dune - Frank Herbert", "price": 649, "stock": 30, "category": "Books", "image": "https://images.unsplash.com/photo-1506466010722-395aa2bef877?w=500"},
    71: {"id": 71, "name": "The Subtle Art of Not Giving a F*ck", "price": 599, "stock": 50, "category": "Books", "image": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=500"},
    72: {"id": 72, "name": "Educated - Tara Westover", "price": 549, "stock": 20, "category": "Books", "image": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=500"},

    # TOYS (73-84)
    73: {"id": 73, "name": "Remote Controlled Racing Drone", "price": 4999, "stock": 8, "category": "Toys", "image": "https://images.unsplash.com/photo-1508614589041-895b88991e3e?w=500"},
    74: {"id": 74, "name": "Educational Robotic Arm Kit", "price": 3499, "stock": 10, "category": "Toys", "image": "https://images.unsplash.com/photo-1558023784-f8341393cb03?w=500"},
    75: {"id": 75, "name": "Interlocking Space Station Blocks", "price": 2499, "stock": 15, "category": "Toys", "image": "https://images.unsplash.com/photo-1585366119957-e9730b6d0f60?w=500"},
    76: {"id": 76, "name": "High-Speed RC Drift Car", "price": 3999, "stock": 12, "category": "Toys", "image": "https://images.unsplash.com/photo-1594787318286-3d835c1d207f?w=500"},
    77: {"id": 77, "name": "3D Crystal Architecture Puzzle", "price": 1299, "stock": 20, "category": "Toys", "image": "https://images.unsplash.com/photo-1515488764276-beab7607c1e6?w=500"},
    78: {"id": 78, "name": "Plush Intelligent Teddy Bear", "price": 1999, "stock": 25, "category": "Toys", "image": "https://images.unsplash.com/photo-1559454403-b8fb88521f11?w=500"},
    79: {"id": 79, "name": "Magic Science Experiment Kit", "price": 1499, "stock": 30, "category": "Toys", "image": "https://images.unsplash.com/photo-1530651788726-1dbf58eeef1f?w=500"},
    80: {"id": 80, "name": "Professional Chess Tournament Set", "price": 2999, "stock": 15, "category": "Toys", "image": "https://images.unsplash.com/photo-1528819622765-d6bcf132f793?w=500"},
    81: {"id": 81, "name": "Art & Craft Deluxe Easel Set", "price": 4599, "stock": 8, "category": "Toys", "image": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=500"},
    82: {"id": 82, "name": "Retro Arcade Handheld Console", "price": 2499, "stock": 20, "category": "Toys", "image": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=500"},
    83: {"id": 83, "name": "Interactive Solar System Globe", "price": 3299, "stock": 10, "category": "Toys", "image": "https://images.unsplash.com/photo-1454165833024-587ad22d9b71?w=500"},
    84: {"id": 84, "name": "Inflatable Indoor Play Castle", "price": 5999, "stock": 5, "category": "Toys", "image": "https://images.unsplash.com/photo-1473091534298-04dcbce3278c?w=500"}
}

class CartItem(BaseModel):
    product_id: int
    quantity: int

class CheckoutRequest(BaseModel):
    items: List[CartItem]
    name: str
    address: str
    phone: str

@app.get("/api/products")
def get_products():
    return list(INVENTORY.values())

@app.post("/api/checkout")
def checkout(order_data: CheckoutRequest):
    for item in order_data.items:
        if item.product_id not in INVENTORY:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found.")
        
        current_stock = INVENTORY[item.product_id]["stock"]
        if item.quantity > current_stock:
            raise HTTPException(
                status_code=400, 
                detail=f"Only {current_stock} units left for {INVENTORY[item.product_id]['name']}."
            )
    
    total_bill = 0
    for item in order_data.items:
        INVENTORY[item.product_id]["stock"] -= item.quantity
        total_bill += INVENTORY[item.product_id]["price"] * item.quantity
        
    order_id = f"SM{uuid.uuid4().hex[:8].upper()}"
    return {
        "status": "Success",
        "message": "Payment secure and authorized via ShopMint Gateway!",
        "order_id": order_id,
        "amount_paid": total_bill,
        "delivery_to": order_data.name
    }
