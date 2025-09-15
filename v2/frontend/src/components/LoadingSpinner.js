import React from 'react';
import { Loader2 } from 'lucide-react';

const LoadingSpinner = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="text-center">
        <Loader2 className="h-12 w-12 text-ozu-red animate-spin mx-auto mb-4" />
        <h2 className="text-xl font-semibold text-gray-900 mb-2">Yükleniyor...</h2>
        <p className="text-gray-600">Dersler yükleniyor, lütfen bekleyin.</p>
      </div>
    </div>
  );
};

export default LoadingSpinner;
