import React from 'react';
import { Calendar, BookOpen, Users } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <Calendar className="h-8 w-8 text-ozu-blue" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">OZUchedule</h1>
                <p className="text-sm text-gray-600">V2 - Yeni Nesil Ders Programı</p>
              </div>
            </div>
          </div>
          
          <div className="flex items-center space-x-6 text-sm text-gray-600">
            <div className="flex items-center space-x-2">
              <BookOpen className="h-4 w-4" />
              <span>Ders Kataloğu</span>
            </div>
            <div className="flex items-center space-x-2">
              <Users className="h-4 w-4" />
              <span>Öğrenci Portalı</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
