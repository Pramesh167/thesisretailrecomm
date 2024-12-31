import React, { useState } from 'react';
import { LayoutGrid, DoorOpen, ArrowRight } from 'lucide-react';

interface StoreLayoutProps {
  data?: Record<string, { 
    section: number; 
    priority: string; 
    category: string;
    sub_category: string;
    products: Array<{
      name: string;
      id: string;
    }> ;
  }>;
  loading?: boolean;
}

const StoreLayout: React.FC<StoreLayoutProps> = ({ data, loading }) => {
  const [selectedAisle, setSelectedAisle] = useState<number | null>(null);

  // Group data by section and priority
  const sections = Array.from({ length: 16 }, (_, index) => {
    const productsInSection = data
      ? Object.entries(data).filter(([_, value]) => value.section === index)
      : [];
    
    const totalProducts = productsInSection.reduce((acc, [_, value]) => 
      acc + (value.products?.length || 0), 0);

    // Generate dynamic aisle name based on the most common product or category
    const aisleName = getAisleName(productsInSection);

    return {
      id: index,
      aisleName,
      products: productsInSection,
      totalProducts,
      priority: determineSectionPriority(productsInSection)
    };
  });

  function getAisleName(productsInSection: any[]) {
    const productNames = productsInSection.flatMap(([_, value]) => value.products.map((product: any) => product.name));
    const categoryNames = productsInSection.flatMap(([_, value]) => value.sub_category);
    
    // Get the most common product name or category (whichever has more occurrences)
    const mostCommonName = findMostCommonName(productNames) || findMostCommonName(categoryNames);
    return mostCommonName || "Uncategorized Aisle";
  }

  function findMostCommonName(arr: string[]) {
    if (arr.length === 0) return '';
    const frequencyMap: Record<string, number> = {};
    let maxCount = 0;
    let mostCommonName = '';
    
    arr.forEach(name => {
      frequencyMap[name] = (frequencyMap[name] || 0) + 1;
      if (frequencyMap[name] > maxCount) {
        maxCount = frequencyMap[name];
        mostCommonName = name;
      }
    });
    
    return mostCommonName;
  }

  function determineSectionPriority(products: any[]) {
    const priorities = products.map(([_, value]) => value.priority);
    if (priorities.includes('high')) return 'high';
    if (priorities.includes('medium')) return 'medium';
    return 'low';
  }

  const getPriorityColor = (priority: string) => {
    const priorityColors: Record<string, string> = {
      high: 'bg-red-100 hover:bg-red-200',
      medium: 'bg-yellow-100 hover:bg-yellow-200',
      low: 'bg-blue-100 hover:bg-blue-200',
    };
    return priorityColors[priority] || 'bg-gray-100';
  };

  const AisleView = ({ section }: { section: any }) => (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white rounded-lg p-6 w-3/4 h-3/4 overflow-auto">
        <div className="flex justify-between mb-4">
          <h3 className="text-lg font-medium text-gray-900">
            {section.aisleName} - Aisle {section.id + 1}
          </h3>
          <button
            className="text-gray-500 hover:text-gray-700"
            onClick={() => setSelectedAisle(null)}
          >
            ✕
          </button>
        </div>
        
        <div className="flex justify-between gap-4 h-full">
          {/* Left Rack */}
          <div className="w-1/2 bg-gray-100 p-4 rounded">
            <h4 className="text-md font-medium mb-2">Left Rack</h4>
            <div className="grid grid-cols-2 gap-2">
              {section.products.slice(0, Math.ceil(section.products.length / 2))
                .map(([productId, details]: [string, any]) => (
                  <div key={productId} className="bg-white p-2 rounded shadow">
                    <p className="text-sm font-medium">{details.products?.[0]?.name || productId}</p>
                    <p className="text-xs text-gray-500">Priority: {details.priority}</p>
                  </div>
              ))}
            </div>
          </div>
          
          {/* Right Rack */}
          <div className="w-1/2 bg-gray-100 p-4 rounded">
            <h4 className="text-md font-medium mb-2">Right Rack</h4>
            <div className="grid grid-cols-2 gap-2">
              {section.products.slice(Math.ceil(section.products.length / 2))
                .map(([productId, details]: [string, any]) => (
                  <div key={productId} className="bg-white p-2 rounded shadow">
                    <p className="text-sm font-medium">{details.products?.[0]?.name || productId}</p>
                    <p className="text-xs text-gray-500">Priority: {details.priority}</p>
                  </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center mb-4">
        <LayoutGrid className="h-6 w-6 text-indigo-600 mr-2" />
        <h2 className="text-lg font-medium text-gray-900">Store Layout Optimization</h2>
      </div>

      {loading ? (
        <div className="h-80 flex items-center justify-center">
          <p className="text-gray-500">Loading layout data...</p>
        </div>
      ) : (
        <>
          <div className="border rounded-lg p-4">
            {/* Entrance Area */}
            <div className="flex items-center justify-center mb-4 gap-2">
              <DoorOpen className="h-8 w-8 text-green-600" />
              <ArrowRight className="h-6 w-6 text-gray-400" />
              <span className="text-sm text-gray-600">Main Entrance</span>
            </div>

            {/* Store Grid */}
            <div className="grid grid-cols-4 gap-4">
              {sections.map((section) => (
                <div
                  key={section.id}
                  onClick={() => setSelectedAisle(section.id)}
                  className={`cursor-pointer rounded-lg p-4 ${getPriorityColor(section.priority)} 
                    transition-colors duration-200`}
                >
                  <div className="text-center">
                    <span className="text-sm font-medium text-gray-700">
                      {section.aisleName}
                    </span>
                    <p className="text-xs font-medium text-gray-500 mt-1">
                      {section.totalProducts} Products
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Aisle Detail View */}
          {selectedAisle !== null && (
            <AisleView section={sections[selectedAisle]} />
          )}
        </>
      )}
    </div>
  );
};

export default StoreLayout;
