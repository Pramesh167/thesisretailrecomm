// import React, { useState, useEffect } from 'react';
// import { ShoppingCart, TrendingUp, Package } from 'lucide-react';
// import FileUpload from './FileUpload';
// import StoreLayout from './StoreLayout';
// import SalesChart from './SalesChart';
// import { fetchAnalytics } from '../lib/api';
// import { formatCurrency } from '../lib/utils';

// const Dashboard: React.FC = () => {
//   const [analyticsData, setAnalyticsData] = useState<any>(null);
//   const [loading, setLoading] = useState(true);

//   const loadAnalytics = async () => {
//     try {
//       const data = await fetchAnalytics();
//       setAnalyticsData(data);
//     } catch (error) {
//       console.error('Failed to load analytics:', error);
//     } finally {
//       setLoading(false);
//     }
//   };



//   const handleUploadComplete = () => {
//     loadAnalytics();
//   };

//   return (
//     <div className="space-y-6">
//       {/* Stats Overview */}
//       <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
//         <div className="bg-white overflow-hidden shadow rounded-lg">
//           <div className="p-5">
//             <div className="flex items-center">
//               <div className="flex-shrink-0">
//                 <ShoppingCart className="h-6 w-6 text-gray-400" />
//               </div>
//               <div className="ml-5 w-0 flex-1">
//                 <dl>
//                   <dt className="text-sm font-medium text-gray-500 truncate">
//                     Total Orders
//                   </dt>
//                   <dd className="text-lg font-medium text-gray-900">
//                     {loading ? '...' : analyticsData?.analytics.metrics?.total_orders || 0}
//                   </dd>
//                 </dl>
//               </div>
//             </div>
//           </div>
//         </div>

//         <div className="bg-white overflow-hidden shadow rounded-lg">
//           <div className="p-5">
//             <div className="flex items-center">
//               <div className="flex-shrink-0">
//                 <TrendingUp className="h-6 w-6 text-gray-400" />
//               </div>
//               <div className="ml-5 w-0 flex-1">
//                 <dl>
//                   <dt className="text-sm font-medium text-gray-500 truncate">
//                     Average Order Value
//                   </dt>
//                   <dd className="text-lg font-medium text-gray-900">
//                     {loading ? '...' : formatCurrency(analyticsData?.analytics.metrics?.average_order_value || 0)}
//                   </dd>
//                 </dl>
//               </div>
//             </div>
//           </div>
//         </div>

//         <div className="bg-white overflow-hidden shadow rounded-lg">
//           <div className="p-5">
//             <div className="flex items-center">
//               <div className="flex-shrink-0">
//                 <Package className="h-6 w-6 text-gray-400" />
//               </div>
//               <div className="ml-5 w-0 flex-1">
//                 <dl>
//                   <dt className="text-sm font-medium text-gray-500 truncate">
//                     Total Products
//                   </dt>
//                   <dd className="text-lg font-medium text-gray-900">
//                     {loading ? '...' : analyticsData?.analytics.metrics?.total_products || 0}
//                   </dd>
//                 </dl>
//               </div>
//             </div>
//           </div>
//         </div>
//       </div>

//       {/* File Upload Section */}
//       <div className="bg-white shadow rounded-lg p-6">
//         <h2 className="text-lg font-medium text-gray-900 mb-4">
//           Upload Store Data
//         </h2>
//         <FileUpload onUploadComplete={handleUploadComplete} />
//       </div>

//       {/* Charts and Layout Section */}
//       <div className="grid grid-rows-1 lg:grid-rows-2 gap-6">
//         <StoreLayout data={analyticsData?.data} loading={loading} />
//         <SalesChart data={analyticsData?.analytics.sub_category_analysis} loading={loading} />
//       </div>
//     </div>
//   );
// };

// export default Dashboard;


import React, { useState, useEffect } from 'react';
import { ShoppingCart, TrendingUp, Package } from 'lucide-react';
import { motion } from 'framer-motion';
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

  const cardVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  };

  const StatCard = ({ icon: Icon, title, value, color }: {
    icon: any;
    title: string;
    value: string | number;
    color: string;
  }) => (
    <motion.div
      variants={cardVariants}
      initial="hidden"
      animate="visible"
      whileHover={{ scale: 1.02 }}
      transition={{ duration: 0.3 }}
      className={`bg-gray-800/90 backdrop-blur-lg overflow-hidden shadow-lg rounded-xl border border-${color}-500/20 transition-all duration-300 hover:bg-gray-700/90 hover:shadow-xl hover:border-${color}-400/30`}
    >
      <div className="p-6">
        <div className="flex items-center">
          <div className={`flex-shrink-0 p-3 bg-${color}-500/10 rounded-lg`}>
            <Icon className={`h-6 w-6 text-${color}-400`} />
          </div>
          <div className="ml-5 w-0 flex-1">
            <dl>
              <dt className={`text-sm font-medium text-${color}-300 truncate mb-1`}>
                {title}
              </dt>
              <dd className={`text-2xl font-bold text-${color}-200`}>
                {loading ? 
                  <div className="animate-pulse h-8 w-24 bg-gray-700 rounded" /> 
                  : value
                }
              </dd>
            </dl>
          </div>
        </div>
      </div>
    </motion.div>
  );

  return (
    <div className="space-y-8 p-6">
      {/* Stats Overview */}
      <motion.div 
        className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3"
        initial="hidden"
        animate="visible"
        variants={{
          hidden: { opacity: 0 },
          visible: {
            opacity: 1,
            transition: {
              staggerChildren: 0.1
            }
          }
        }}
      >
        <StatCard
          icon={ShoppingCart}
          title="Total Orders"
          value={analyticsData?.analytics.metrics?.total_orders || 0}
          color="yellow"
        />
        <StatCard
          icon={TrendingUp}
          title="Average Order Value"
          value={formatCurrency(analyticsData?.analytics.metrics?.average_order_value || 0)}
          color="green"
        />
        <StatCard
          icon={Package}
          title="Total Products"
          value={analyticsData?.analytics.metrics?.total_products || 0}
          color="blue"
        />
      </motion.div>

      {/* File Upload Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="bg-gray-800/90 backdrop-blur-lg shadow-lg rounded-xl border border-yellow-500/20 p-8 transition-all duration-300 hover:bg-gray-700/90 hover:shadow-xl hover:border-yellow-400/30"
      >
        <h2 className="text-xl font-bold text-yellow-300 mb-6">
          Upload Store Data
        </h2>
        <FileUpload onUploadComplete={handleUploadComplete} />
      </motion.div>

      {/* Charts and Layout Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="grid grid-rows-1 lg:grid-rows-2 gap-8"
      >
        <div className="bg-gray-800/90 backdrop-blur-lg rounded-xl border border-blue-500/20 p-6 transition-all duration-300 hover:shadow-xl hover:border-blue-400/30">
          <StoreLayout data={analyticsData?.data} loading={loading} />
        </div>
        <div className="bg-gray-800/90 backdrop-blur-lg rounded-xl border border-green-500/20 p-6 transition-all duration-300 hover:shadow-xl hover:border-green-400/30">
          <SalesChart data={analyticsData?.analytics.sub_category_analysis} loading={loading} />
        </div>
      </motion.div>
    </div>
  );
};

export default Dashboard;