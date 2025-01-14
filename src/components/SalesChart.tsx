// import React from 'react';
// import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

// interface SalesChartProps {
//   data?: Record<string, { Sales: number; Profit: number; Quantity: number }>;
//   loading?: boolean;
// }

// const SalesChart: React.FC<SalesChartProps> = ({ data, loading }) => {
//   const chartData = data
//     ? Object.entries(data).map(([category, values]) => ({
//         category,
//         sales: values.Sales,
//         profit: values.Profit,
//       }))
//     : [];

//   return (
//     <div className="bg-white rounded-lg shadow p-6">
//       <h2 className="text-lg font-medium text-gray-900 mb-4">Sales by Category</h2>
//       <div className="h-80">
//         {loading ? (
//           <div className="h-full flex items-center justify-center">
//             <p className="text-gray-500">Loading data...</p>
//           </div>
//         ) : (
//           <ResponsiveContainer width="100%" height="100%">
//             <BarChart data={chartData}>
//               <CartesianGrid strokeDasharray="3 3" />
//               <XAxis dataKey="category" />
//               <YAxis />
//               <Tooltip />
//               <Legend />
//               <Bar dataKey="sales" fill="#4F46E5" name="Sales" />
//               <Bar dataKey="profit" fill="#10B981" name="Profit" />
//             </BarChart>
//           </ResponsiveContainer>
//         )}
//       </div>
//     </div>
//   );
// };

// export default SalesChart;


import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface SalesChartProps {
  data?: Record<string, { Sales: number; Profit: number; Quantity: number }>;
  loading?: boolean;
}

const SalesChart: React.FC<SalesChartProps> = ({ data, loading }) => {
  const chartData = data
    ? Object.entries(data).map(([category, values]) => ({
        category,
        sales: values.Sales,
        profit: values.Profit,
      }))
    : [];

  return (
    <div className="bg-gray-800 rounded-lg shadow p-6">
      <h2 className="text-lg font-medium text-gray-200 mb-4">Sales by Category</h2>
      <div className="h-80">
        {loading ? (
          <div className="h-full flex items-center justify-center">
            <p className="text-gray-400">Loading data...</p>
          </div>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} barCategoryGap="35%">
              <CartesianGrid strokeDasharray="3 3" stroke="#2d3748" />
              <XAxis dataKey="category" stroke="#cbd5e0" />
              <YAxis stroke="#cbd5e0" />
              <Tooltip
                contentStyle={{ backgroundColor: '#2d3748', border: 'none' }}
                itemStyle={{ color: '#e2e8f0' }}
                cursor={{ fill: '#1a202c' }}
              />
              <Legend wrapperStyle={{ color: '#cbd5e0' }} />
              <Bar dataKey="sales" fill="#4F46E5" name="Sales" />
              <Bar dataKey="profit" fill="#10B981" name="Profit" />
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
};

export default SalesChart;
