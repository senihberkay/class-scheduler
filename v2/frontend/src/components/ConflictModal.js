import React from 'react';
import { AlertTriangle, X, Clock, MapPin } from 'lucide-react';

const ConflictModal = ({ conflicts, onClose }) => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[80vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div className="flex items-center space-x-3">
            <AlertTriangle className="h-6 w-6 text-red-500" />
            <div>
              <h2 className="text-xl font-semibold text-gray-900">Ders Çakışması Tespit Edildi</h2>
              <p className="text-sm text-gray-600">{conflicts.length} çakışma bulundu</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="h-6 w-6" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-[60vh]">
          <div className="space-y-4">
            {conflicts.map((conflict, index) => (
              <div key={index} className="border border-red-200 rounded-lg p-4 bg-red-50">
                <div className="flex items-start space-x-3">
                  <AlertTriangle className="h-5 w-5 text-red-500 mt-0.5" />
                  <div className="flex-1">
                    <h3 className="font-medium text-gray-900 mb-2">
                      {conflict.course1} ↔ {conflict.course2}
                    </h3>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {/* İlk ders */}
                      <div className="bg-white rounded p-3 border border-red-200">
                        <div className="font-medium text-sm text-gray-900 mb-1">
                          {conflict.course1}
                        </div>
                        <div className="flex items-center space-x-2 text-xs text-gray-600 mb-1">
                          <Clock className="h-3 w-3" />
                          <span>{conflict.time1}</span>
                        </div>
                        <div className="flex items-center space-x-2 text-xs text-gray-600">
                          <MapPin className="h-3 w-3" />
                          <span>{conflict.room1}</span>
                        </div>
                      </div>
                      
                      {/* İkinci ders */}
                      <div className="bg-white rounded p-3 border border-red-200">
                        <div className="font-medium text-sm text-gray-900 mb-1">
                          {conflict.course2}
                        </div>
                        <div className="flex items-center space-x-2 text-xs text-gray-600 mb-1">
                          <Clock className="h-3 w-3" />
                          <span>{conflict.time2}</span>
                        </div>
                        <div className="flex items-center space-x-2 text-xs text-gray-600">
                          <MapPin className="h-3 w-3" />
                          <span>{conflict.room2}</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="mt-3 text-xs text-gray-600">
                      <span className="font-medium">Gün:</span> {conflict.day}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-gray-200 bg-gray-50">
          <div className="flex items-center justify-between">
            <div className="text-sm text-gray-600">
              Çakışmaları çözmek için ders seçimlerinizi gözden geçirin.
            </div>
            <button
              onClick={onClose}
              className="bg-ozu-blue text-white px-4 py-2 rounded-lg hover:bg-ozu-light-blue transition-colors"
            >
              Anladım
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ConflictModal;
