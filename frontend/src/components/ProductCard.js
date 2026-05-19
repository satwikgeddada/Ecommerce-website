import React from 'react';

export default function ProductCard({ product, onAddToCart }) {
  return (
    <div className="bg-white p-4 rounded-xl shadow-sm border border-slate-100 hover:shadow-md transition duration-200 flex flex-col justify-between">
      <div className="bg-slate-50 rounded-lg p-2 mb-4">
        <img src={product.image} alt={product.name} className="h-44 w-full object-contain mix-blend-multiply" />
      </div>
      <div>
        <h3 className="font-semibold text-slate-800 text-sm line-clamp-2 h-10">{product.name}</h3>
        <p className="text-2xl font-black text-slate-900 mt-2">₹{product.price.toLocaleString('en-IN')}</p>
        <p className={`text-xs font-semibold mt-1.5 inline-block px-2 py-0.5 rounded ${product.stock > 0 ? 'bg-mint-50 text-mint-700' : 'bg-red-50 text-red-600'}`}>
          {product.stock > 0 ? `${product.stock} units left` : "Out of Stock"}
        </p>
      </div>
      <button 
        onClick={(e) => onAddToCart(e, product)}
        disabled={product.stock === 0}
        className="w-full mt-5 bg-slate-900 hover:bg-slate-800 text-white py-2.5 font-bold rounded-lg text-xs tracking-wider transition disabled:bg-slate-200 disabled:text-slate-400"
      >
        {product.stock > 0 ? "ADD TO CART" : "OUT OF STOCK"}
      </button>
    </div>
  );
}
