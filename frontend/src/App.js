import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Routes, Route, useNavigate, useParams, Link } from 'react-router-dom';
import Navbar from './components/Navbar';
import ProductCard from './components/ProductCard';
import ProductDetail from './components/ProductDetail';
import { ChevronLeft } from 'lucide-react';

const BACKEND_URL = "http://127.0.0.1:8000/api";
const categories = ["All", "Electronics", "Mobiles", "Fashion", "Appliances", "Sports", "Books", "Toys"];

function HomePage({ products, selectedCategory, setSelectedCategory, searchQuery, addToCart, setShowCheckout }) {
  const filteredProducts = products.filter(p => {
    const matchesSearch = p.name.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === "All" || p.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  return (
    <main className="max-w-6xl w-full mx-auto px-4 py-8 flex flex-col md:flex-row gap-8 flex-1">
      <aside className="w-full md:w-64 flex-shrink-0">
        <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 sticky top-24">
          <h3 className="text-xs uppercase font-black text-slate-400 tracking-widest mb-6">Explore Categories</h3>
          <nav className="space-y-1">
            {categories.map(cat => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`w-full text-left px-4 py-3 rounded-xl font-bold text-sm transition ${selectedCategory === cat ? 'bg-mint-500 text-slate-950 shadow-md translate-x-1' : 'text-slate-500 hover:bg-slate-50 hover:text-slate-900'}`}
              >
                {cat === "All" ? "🔥 Trending All" : cat}
              </button>
            ))}
          </nav>
        </div>
      </aside>

      <div className="flex-1">
        <div className="flex items-center justify-between mb-8">
          <h2 className="text-2xl font-black text-slate-900 flex items-center gap-2">
            {selectedCategory} <span className="text-slate-300 font-normal">({filteredProducts.length})</span>
          </h2>
          <div className="text-sm font-bold text-mint-600 bg-mint-50 px-3 py-1 rounded-full border border-mint-100">
            ⚡ LIVE DEALS
          </div>
        </div>
        
        {filteredProducts.length === 0 ? (
          <div className="bg-white p-16 text-center rounded-3xl border border-dashed border-slate-200 text-slate-400 shadow-sm">
            <p className="text-lg font-bold mb-2">No items found</p>
            <p className="text-sm">Try adjusting your search or category filter.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredProducts.map(product => (
              <Link to={`/product/${product.id}`} key={product.id}>
                <ProductCard product={product} onAddToCart={(e, p) => { e.preventDefault(); addToCart(p); }} />
              </Link>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}

function ProductPage({ products, addToCart, buyNow }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const product = products.find(p => p.id === parseInt(id));

  if (!product) return <div className="text-center py-20 font-bold">Loading product details...</div>;

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <button 
        onClick={() => navigate(-1)} 
        className="flex items-center space-x-2 text-slate-500 font-bold mb-6 hover:text-slate-900 transition-colors"
      >
        <ChevronLeft className="h-5 w-5" />
        <span>Back to Catalog</span>
      </button>
      <ProductDetail product={product} onAddToCart={addToCart} onBuyNow={buyNow} />
    </div>
  );
}

export default function App() {
  const [products, setProducts] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [searchQuery, setSearchQuery] = useState("");
  const [cart, setCart] = useState(() => {
    const savedCart = localStorage.getItem('shopmint_cart');
    return savedCart ? JSON.parse(savedCart) : [];
  });
  
  const [showCheckout, setShowCheckout] = useState(false);
  const [shippingInfo, setShippingInfo] = useState({ name: "", address: "", phone: "" });

  useEffect(() => {
    localStorage.setItem('shopmint_cart', JSON.stringify(cart));
  }, [cart]);

  const fetchProducts = async () => {
    try {
      const res = await axios.get(`${BACKEND_URL}/products`);
      setProducts(res.data);
    } catch (err) {
      console.error("Backend offline or connection failed.", err);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  const addToCart = (product) => {
    const existing = cart.find(item => item.id === product.id);
    const currentQty = existing ? existing.quantity : 0;

    if (currentQty >= product.stock) {
      alert(`Stock boundary reached. Only ${product.stock} available items left.`);
      return;
    }

    if (existing) {
      setCart(cart.map(item => item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item));
    } else {
      setCart([...cart, { ...product, quantity: 1 }]);
    }
  };

  const buyNow = (product) => {
    const existing = cart.find(item => item.id === product.id);
    if (!existing) {
      if (product.stock > 0) {
        setCart([...cart, { ...product, quantity: 1 }]);
      } else {
        alert("Out of stock!");
        return;
      }
    }
    setShowCheckout(true);
  };

  const removeFromCart = (id) => {
    setCart(cart.filter(item => item.id !== id));
  };

  const updateQuantity = (id, delta, maxStock) => {
    setCart(cart.map(item => {
      if (item.id === id) {
        const newQty = item.quantity + delta;
        if (newQty > maxStock) {
          alert(`Maximum stock validation failed: only ${maxStock} available.`);
          return item;
        }
        return newQty > 0 ? { ...item, quantity: newQty } : null;
      }
      return item;
    }).filter(Boolean));
  };

  const handleCheckout = async (e) => {
    e.preventDefault();
    const payload = {
      items: cart.map(item => ({ product_id: item.id, quantity: item.quantity })),
      ...shippingInfo
    };

    try {
      const res = await axios.post(`${BACKEND_URL}/checkout`, payload);
      alert(`🎉 Checkout Success!\n\nOrder ID: ${res.data.order_id}\nTotal Paid: ₹${res.data.amount_paid.toLocaleString('en-IN')}\n\n${res.data.message}`);
      setCart([]);
      setShowCheckout(false);
      fetchProducts();
    } catch (err) {
      alert(err.response?.data?.detail || "Checkout execution halted due to server error.");
    }
  };

  const cartTotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  const totalItems = cart.reduce((a, b) => a + b.quantity, 0);

  return (
    <Router>
      <div className="min-h-screen flex flex-col bg-slate-50">
        <Navbar 
          searchQuery={searchQuery} 
          setSearchQuery={setSearchQuery} 
          cartCount={totalItems} 
          onCartClick={() => setShowCheckout(true)} 
        />

        <Routes>
          <Route path="/" element={
            <HomePage 
              products={products}
              selectedCategory={selectedCategory}
              setSelectedCategory={setSelectedCategory}
              searchQuery={searchQuery}
              addToCart={addToCart}
              setShowCheckout={setShowCheckout}
            />
          } />
          <Route path="/product/:id" element={
            <ProductPage products={products} addToCart={addToCart} buyNow={buyNow} />
          } />
        </Routes>

        {/* Checkout Modal */}
        {showCheckout && (
          <div className="fixed inset-0 bg-slate-950/60 backdrop-blur-md flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-3xl max-w-md w-full p-8 shadow-2xl border border-slate-100">
              <h2 className="text-2xl font-black mb-6 text-slate-900 flex items-center gap-3">
                Secure Checkout 🛡️
              </h2>
              {cart.length === 0 ? (
                <div className="text-center py-8">
                  <p className="text-lg font-bold text-slate-900 mb-2">Checkout Complete!</p>
                  <p className="text-sm text-slate-500 mb-6">Your order is being processed by ShopMint Gateway.</p>
                  <button type="button" onClick={() => setShowCheckout(false)} className="w-full bg-slate-950 text-white py-4 rounded-2xl text-sm font-black shadow-lg">BACK TO SHOPPING</button>
                </div>
              ) : (
                <form onSubmit={handleCheckout} className="space-y-5">
                  <div className="max-h-40 overflow-y-auto mb-4 divide-y divide-slate-50 border-b border-slate-50">
                     {cart.map(item => (
                        <div key={item.id} className="py-3 flex justify-between items-center">
                           <div className="w-3/5">
                              <p className="text-xs font-bold truncate">{item.name}</p>
                              <p className="text-[10px] text-slate-400 font-bold">₹{item.price.toLocaleString()}</p>
                           </div>
                           <div className="flex items-center space-x-2 bg-slate-50 rounded-lg p-1">
                              <button type="button" onClick={() => updateQuantity(item.id, -1, item.stock)} className="w-5 h-5 bg-white shadow-sm rounded flex items-center justify-center font-black">-</button>
                              <span className="text-xs font-black">{item.quantity}</span>
                              <button type="button" onClick={() => updateQuantity(item.id, 1, item.stock)} className="w-5 h-5 bg-white shadow-sm rounded flex items-center justify-center font-black">+</button>
                           </div>
                        </div>
                     ))}
                  </div>
                  <div>
                    <label className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5 ml-1">Recipient Name</label>
                    <input required type="text" className="w-full bg-slate-50 border border-slate-100 p-4 rounded-2xl text-sm font-bold focus:ring-4 focus:ring-mint-500/20 focus:bg-white focus:outline-none transition-all" value={shippingInfo.name} onChange={e => setShippingInfo({...shippingInfo, name: e.target.value})} placeholder="John Doe" />
                  </div>
                  <div>
                    <label className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5 ml-1">Delivery Address</label>
                    <textarea required rows="2" className="w-full bg-slate-50 border border-slate-100 p-4 rounded-2xl text-sm font-bold focus:ring-4 focus:ring-mint-500/20 focus:bg-white focus:outline-none transition-all" value={shippingInfo.address} onChange={e => setShippingInfo({...shippingInfo, address: e.target.value})} placeholder="Flat No, Street, Landmark..."></textarea>
                  </div>
                  <div>
                    <label className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5 ml-1">Phone Number</label>
                    <input required type="tel" className="w-full bg-slate-50 border border-slate-100 p-4 rounded-2xl text-sm font-bold focus:ring-4 focus:ring-mint-500/20 focus:bg-white focus:outline-none transition-all" value={shippingInfo.phone} onChange={e => setShippingInfo({...shippingInfo, phone: e.target.value})} placeholder="+91 XXXXX XXXXX" />
                  </div>
                  <div className="bg-mint-500/10 p-5 rounded-2xl border border-mint-500/20 flex justify-between items-center">
                    <span className="text-xs font-black text-mint-800 uppercase tracking-widest">Total Amount</span>
                    <span className="text-xl font-black text-slate-900">₹{cartTotal.toLocaleString('en-IN')}</span>
                  </div>
                  <div className="flex space-x-4 pt-4">
                    <button type="button" onClick={() => setShowCheckout(false)} className="w-1/2 border border-slate-100 py-4 rounded-2xl text-sm font-black text-slate-400 hover:bg-slate-50 transition-all">CANCEL</button>
                    <button type="submit" className="w-1/2 bg-slate-950 text-mint-400 py-4 rounded-2xl text-sm font-black hover:scale-105 transition-all shadow-xl">PAY NOW</button>
                  </div>
                </form>
              )}
            </div>
          </div>
        )}
      </div>
    </Router>
  );
}
