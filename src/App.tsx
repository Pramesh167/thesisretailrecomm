import React from 'react';
import { LayoutDashboard, ShoppingCart, TrendingUp } from 'lucide-react';
import Dashboard from './components/Dashboard';

function App() {
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Navigation */}
      <nav className="bg-gray-800 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <div className="flex-shrink-0 flex items-center">
                <LayoutDashboard className="h-8 w-8 text-indigo-400 animate-bounce" />
                <span className="ml-2 text-xl font-bold">
                  Retail Store Optimizer
                </span>
              </div>
              <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                <a
                  href="#"
                  className="border-indigo-700 text-white inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium hover:text-indigo-300 hover:border-indigo-300"
                >
                  Dashboard
                </a>
                {/* Uncomment and modify the following if needed */}
                {/* <a
                  href="#"
                  className="border-transparent text-gray-400 hover:border-gray-300 hover:text-gray-200 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                >
                  Products
                </a>
                <a
                  href="#"
                  className="border-transparent text-gray-400 hover:border-gray-300 hover:text-gray-200 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                >
                  Analytics
                </a> */}
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Dashboard />
      </main>
    </div>
  );
}

export default App;
