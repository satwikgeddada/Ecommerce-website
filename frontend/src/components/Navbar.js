import React from 'react';

export default function Navbar({ searchQuery, setSearchQuery, cartCount, onCartClick }) {
  return (
    <header className="bg-slate-950 text-white sticky top-0 z-50 py-4 shadow-2xl">
      <div className="max-w-6xl mx-auto flex items-center justify-between px-4 gap-6">
        <div className="flex items-center space-x-12 flex-1">
          <h1 className="text-3xl font-black tracking-tighter text-white cursor-pointer select-none">
            Shop<span className="text-mint-400">Mint</span>
          </h1>
          <div className="hidden md:block flex-1 max-w-xl relative group">
            <input 
              type="text" 
              placeholder="Search premium gadgets, fashion, books..."
              className="w-full py-3 pl-6 pr-12 rounded-2xl bg-slate-900 text-white text-sm font-bold focus:outline-none focus:ring-4 focus:ring-mint-500/30 border border-slate-800 transition-all group-hover:bg-slate-800"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <div className="absolute right-4 top-3 text-slate-500 font-black">/</div>
          </div>
        </div>
        <div className="flex items-center space-x-6">
          <button 
            onClick={onCartClick}
            className="bg-mint-500 text-slate-950 px-6 py-3 font-black rounded-2xl shadow-xl hover:scale-105 active:scale-95 transition-all flex items-center space-x-3 relative"
          >
            <span className="text-sm tracking-widest">BAG</span>
            <span className="bg-slate-950 text-mint-400 text-[10px] rounded-lg px-2 py-0.5 font-black">
              {cartCount}
            </span>
          </button>
        </div>
      </div>
    </header>
  );
}
