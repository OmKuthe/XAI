// components/LoadingSpinner.jsx
const LoadingSpinner = () => {
    return (
      <div className="flex flex-col items-center justify-center py-16">
        <div className="relative">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600"></div>
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-2xl">🎯</span>
          </div>
        </div>
        <p className="text-gray-600 mt-4 font-medium">Analyzing your preferences...</p>
        <p className="text-gray-400 text-sm mt-2">Using AI to find the best matches</p>
      </div>
    );
  };
  
  export default LoadingSpinner;