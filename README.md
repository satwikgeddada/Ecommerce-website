# ShopMint 💻

ShopMint is a modern, full-stack e-commerce application. It features a sleek, responsive design and a robust set of functionalities for a complete online shopping experience.

## 🚀 Features

### Frontend (React + Tailwind CSS)
- **User-Interface**: Clean, professional, and familiar interface.
- **Dynamic Catalog**: Browse through 80+ products across 7 categories (Electronics, Mobiles, Fashion, Appliances, Sports, Books, Toys).
- **Advanced Routing**: Seamless navigation between the home catalog and detailed product pages using `react-router-dom`.
- **Product Details**: Comprehensive view with high-res images, pricing logic (discounts), trust badges, and immersive descriptions.
- **Real-time Search & Filtering**: Instant search bar and category-based sidebar filtering.
- **Persistent Cart System**: Manage your shopping bag with local storage persistence.
- **Secure Checkout Simulation**: A dedicated checkout modal with form validation and stock level checks.

### Backend (FastAPI)
- **In-Memory Database**: High-performance inventory management that resets on server restart.
- **RESTful API**: Clean endpoints for fetching products and processing checkouts.
- **Stock Validation**: Prevents overselling by checking inventory levels during checkout.
- **Order Generation**: Generates unique ShopMint order IDs (e.g., `SMXXXXXX`) upon successful purchase.
- **CORS Enabled**: Configured for seamless communication with the React frontend.

---

## 🛠️ Tech Stack

- **Frontend**: React.js, Tailwind CSS, Lucide React (Icons), Axios, React Router.
- **Backend**: Python, FastAPI, Pydantic, Uvicorn.
- **Images**: High-quality, verified Unsplash direct links.

---

## 📂 Project Structure

```
ShopMint/
├── backend/                  # FastAPI Application
│   ├── main.py               # API routes, Models & In-Memory DB
│   ├── requirements.txt      # Python dependencies
│   └── README.md             # Backend setup guide
│
└── frontend/                 # React Application
    ├── public/               # Static assets
    ├── src/
    │   ├── components/       # Reusable UI (Navbar, ProductCard, ProductDetail)
    │   ├── App.js            # Main routing & state logic
    │   ├── index.css         # Tailwind & global styles
    │   └── index.js          # Entry point
    ├── package.json          # Node.js dependencies
    └── tailwind.config.js    # Theme configuration
```

---

## 🏁 Getting Started

Follow these steps to get the project running on your local machine.

### 1. Prerequisites
- Python 3.8+
- Node.js (v14 or higher)
- npm or yarn

### 2. Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the server:
   ```bash
   uvicorn main:app --reload
   ```
   The backend will be available at `http://localhost:8000`.

### 3. Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the React app:
   ```bash
   npm start
   ```
   The application will open automatically at `http://localhost:3000`.

---

## 📜 License

This project is open-source and available for educational purposes. Feel free to clone, modify, and learn!

**ShopMint - Your Premium Shopping Destination** 
