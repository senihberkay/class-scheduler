import React from 'react';
import { BookOpen, Users } from 'lucide-react';
import logo from '../assets/ozu_schedule_logo.png';

const Header = () => {
  return (
    <header className="sticky top-0 z-50 bg-ozu-red shadow-sm border-b border-ozu-red-dark">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <img src={logo} alt="OZUchedule Logo" className="h-14 w-40" />
              <div>
              </div>
            </div>
          </div>
          
          <div className="flex items-center space-x-6 text-sm text-white text-opacity-90">
            <a 
              href="https://www.ozyegin.edu.tr/tr/acilan-dersler" 
              target="_blank" 
              rel="noopener noreferrer"
              className="flex items-center space-x-2 hover:text-white transition-colors duration-200 cursor-pointer"
            >
              <BookOpen className="h-4 w-4" />
              <span>Ders Kataloğu</span>
            </a>
            <a 
              href="https://sis.ozyegin.edu.tr/" 
              target="_blank" 
              rel="noopener noreferrer"
              className="flex items-center space-x-2 hover:text-white transition-colors duration-200 cursor-pointer"
            >
              <Users className="h-4 w-4" />
              <span>Öğrenci Portalı</span>
            </a>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;