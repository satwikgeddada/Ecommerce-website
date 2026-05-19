import React from 'react';
import { Star, ShieldCheck, Truck, RotateCcw } from 'lucide-react';

export default function ProductDetail({ product, onAddToCart, onBuyNow }) {
  if (!product) return null;

  return (
    <div className="bg-white rounded-3xl shadow-sm border border-slate-100 overflow-hidden">
      <div className="flex flex-col md:flex-row">
        {/* Left: Image Section */}
        <div className="md:w-1/2 p-8 bg-slate-50 flex items-center justify-center border-r border-slate-100">
          <img 
            src={product.image} 
            alt={product.name} 
            className="max-h-[500px] object-contain hover:scale-105 transition-transform duration-500" 
          />
        </div>

        {/* Right: Details Section */}
        <div className="md:w-1/2 p-10">
          <div className="mb-6">
            <span className="text-xs font-black text-mint-600 bg-mint-50 px-3 py-1 rounded-full uppercase tracking-widest">
              {product.category}
            </span>
            <h1 className="text-3xl font-black text-slate-900 mt-4 leading-tight">{product.name}</h1>
            <div className="flex items-center mt-4 space-x-4">
              <div className="flex items-center bg-green-600 text-white px-2 py-0.5 rounded-lg text-sm font-bold">
                <span>4.5</span>
                <Star className="h-3 w-3 fill-current ml-1" />
              </div>
              <span className="text-slate-400 font-bold text-sm underline cursor-pointer">1,248 Ratings & 452 Reviews</span>
            </div>
          </div>

          <div className="mb-8">
            <div className="flex items-end space-x-3">
              <span className="text-4xl font-black text-slate-900">₹{product.price.toLocaleString('en-IN')}</span>
              <span className="text-slate-400 line-through text-lg font-bold">₹{(product.price * 1.4).toLocaleString('en-IN')}</span>
              <span className="text-green-600 font-black text-lg">40% off</span>
            </div>
            <p className="text-slate-500 text-sm mt-2 font-medium italic">Includes all taxes and delivery fees</p>
          </div>

          <div className="space-y-6 mb-10">
            <div className="flex items-center space-x-4 text-slate-700">
              <div className="p-3 bg-slate-100 rounded-2xl">
                <Truck className="h-5 w-5" />
              </div>
              <div>
                <p className="text-sm font-black">Free Express Delivery</p>
                <p className="text-xs text-slate-400 font-bold">Guaranteed by Tomorrow, 11 AM</p>
              </div>
            </div>
            <div className="flex items-center space-x-4 text-slate-700">
              <div className="p-3 bg-slate-100 rounded-2xl">
                <RotateCcw className="h-5 w-5" />
              </div>
              <div>
                <p className="text-sm font-black">7 Days Replacement</p>
                <p className="text-xs text-slate-400 font-bold">Easy returns if item is damaged/faulty</p>
              </div>
            </div>
            <div className="flex items-center space-x-4 text-slate-700">
              <div className="p-3 bg-slate-100 rounded-2xl">
                <ShieldCheck className="h-5 w-5" />
              </div>
              <div>
                <p className="text-sm font-black">1 Year ShopMint Warranty</p>
                <p className="text-xs text-slate-400 font-bold">Authorized Service Center Support</p>
              </div>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row gap-4">
            <button 
              onClick={() => onAddToCart(product)}
              disabled={product.stock === 0}
              className="flex-1 bg-slate-900 text-mint-400 py-4 rounded-2xl font-black text-sm tracking-widest hover:bg-slate-800 transition-all disabled:bg-slate-200 disabled:text-slate-400"
            >
              {product.stock > 0 ? 'ADD TO BAG' : 'OUT OF STOCK'}
            </button>
            <button 
              onClick={() => onBuyNow(product)}
              disabled={product.stock === 0}
              className="flex-1 bg-mint-500 text-slate-950 py-4 rounded-2xl font-black text-sm tracking-widest shadow-xl shadow-mint-500/20 hover:bg-mint-600 transition-all disabled:bg-slate-200 disabled:text-slate-400"
            >
              BUY NOW
            </button>
          </div>
          
          <div className="mt-10 border-t border-slate-100 pt-8">
            <h3 className="text-sm font-black text-slate-900 mb-4 uppercase tracking-widest">Product Description</h3>
            <p className="text-slate-500 text-sm leading-relaxed font-medium">
              Experience excellence with the {product.name}. Designed for those who demand the best, this {product.category.toLowerCase()} masterpiece combines cutting-edge technology with elegant aesthetics. Whether you're upgrading your lifestyle or gifting a loved one, ShopMint ensures premium quality and unmatched reliability.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
