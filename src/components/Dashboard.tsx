import React, { useState, useEffect } from 'react';
import { ShoppingCart, TrendingUp, Package } from 'lucide-react';
import FileUpload from './FileUpload';
import StoreLayout from './StoreLayout';
import SalesChart from './SalesChart';
import { fetchAnalytics } from '../lib/api';
import { formatCurrency } from '../lib/utils';

const Dashboard: React.FC = () => {
  const [analyticsData, setAnalyticsData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const loadAnalytics = async () => {
    try {
      const data = await fetchAnalytics();
      setAnalyticsData(data);
    } catch (error) {
      console.error('Failed to load analytics:', error);
    } finally {
      setLoading(false);
    }
  };



  const handleUploadComplete = () => {
    loadAnalytics();
  };

  return (
    <div className="space-y-6">
      {/* Stats Overview */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <ShoppingCart className="h-6 w-6 text-gray-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Total Orders
                  </dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {loading ? '...' : analyticsData?.analytics.metrics?.total_orders || 0}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <TrendingUp className="h-6 w-6 text-gray-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Average Order Value
                  </dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {loading ? '...' : formatCurrency(analyticsData?.analytics.metrics?.average_order_value || 0)}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Package className="h-6 w-6 text-gray-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Total Products
                  </dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {loading ? '...' : analyticsData?.analytics.metrics?.total_products || 0}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* File Upload Section */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">
          Upload Store Data
        </h2>
        <FileUpload onUploadComplete={handleUploadComplete} />
      </div>

      {/* Charts and Layout Section */}
      <div className="grid grid-rows-1 lg:grid-rows-2 gap-6">
        <StoreLayout data={analyticsData?.data} loading={loading} />
        <SalesChart data={analyticsData?.analytics.sub_category_analysis} loading={loading} />
      </div>
    </div>
  );
};

export default Dashboard;