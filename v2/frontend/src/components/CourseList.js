import React, { useState } from 'react';
import { Search, BookOpen, Clock, User } from 'lucide-react';

const CourseList = ({ courses, selectedCourses, onCourseSelection, onRemoveCourse }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDay, setSelectedDay] = useState('');
  const [expandedCourses, setExpandedCourses] = useState(new Set());

  // Mevcut günleri al
  const availableDays = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar'];

  // Arama ve gün filtresi - course ve section seviyesinde
  const filteredCourses = courses.map(course => {
    // Metin filtresi
    const matchesSearch = course.code.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         course.name.toLowerCase().includes(searchTerm.toLowerCase());
    
    if (!matchesSearch) return null;
    
    // Section'ları gün filtresine göre filtrele
    const filteredSections = course.sections.filter(section => {
      if (selectedDay === '') return true;
      return section.schedule.some(slot => slot.day === selectedDay);
    });
    
    // Eğer hiç section kalmadıysa course'u gösterme
    if (filteredSections.length === 0 && selectedDay !== '') return null;
    
    return {
      ...course,
      sections: filteredSections
    };
  }).filter(course => course !== null);

  // Ders genişletme/daraltma
  const toggleCourseExpansion = (courseCode) => {
    const newExpanded = new Set(expandedCourses);
    if (newExpanded.has(courseCode)) {
      newExpanded.delete(courseCode);
    } else {
      newExpanded.add(courseCode);
    }
    setExpandedCourses(newExpanded);
  };

  // Seçili ders kontrolü
  const isCourseSelected = (course, section) => {
    return selectedCourses.some(c => 
      c.code === course.code && c.section === section.section
    );
  };

  // Gelişmiş renk oluşturma sistemi
  const getCourseColor = (courseCode) => {
    const colors = [
      'bg-blue-100 text-blue-800',
      'bg-green-100 text-green-800',
      'bg-purple-100 text-purple-800',
      'bg-orange-100 text-orange-800',
      'bg-red-100 text-red-800',
      'bg-yellow-100 text-yellow-800',
      'bg-indigo-100 text-indigo-800',
      'bg-pink-100 text-pink-800',
      'bg-teal-100 text-teal-800',
      'bg-cyan-100 text-cyan-800',
      'bg-lime-100 text-lime-800',
      'bg-amber-100 text-amber-800',
      'bg-emerald-100 text-emerald-800',
      'bg-violet-100 text-violet-800',
      'bg-rose-100 text-rose-800',
      'bg-sky-100 text-sky-800'
    ];
    
    // Ders koduna göre tutarlı renk seçimi
    let hash = 0;
    for (let i = 0; i < courseCode.length; i++) {
      hash = courseCode.charCodeAt(i) + ((hash << 5) - hash);
    }
    const index = Math.abs(hash) % colors.length;
    return colors[index];
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900 mb-3">Dersler</h2>
        
        {/* Arama */}
        <div className="relative mb-3">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
          <input
            type="text"
            placeholder="Ders ara..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-ozu-red focus:border-transparent"
          />
        </div>

        {/* Gün Filtresi */}
        <div className="relative">
          <select
            value={selectedDay}
            onChange={(e) => setSelectedDay(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-ozu-red focus:border-transparent bg-white text-gray-700"
          >
            <option value="">Tüm günler</option>
            {availableDays.map(day => (
              <option key={day} value={day}>{day}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Ders Listesi - Seçili dersler bölümünü kaldırdık */}
      <div className="max-h-96 overflow-y-auto">
        {filteredCourses.length === 0 ? (
          <div className="p-4 text-center text-gray-500">
            Ders bulunamadı
          </div>
        ) : (
          <div className="divide-y divide-gray-200">
            {filteredCourses.map((course) => (
              <div key={course.code} className="p-4">
                <button
                  onClick={() => toggleCourseExpansion(course.code)}
                  className="w-full text-left flex items-center justify-between hover:bg-gray-50 p-2 rounded transition-colors"
                >
                  <div className="flex items-center space-x-3">
                    <BookOpen className="h-5 w-5 text-gray-400" />
                    <div>
                      <div className="font-medium text-gray-900">{course.code}</div>
                      <div className="text-sm text-gray-600">{course.name}</div>
                    </div>
                  </div>
                  <div className={`text-xs px-2 py-1 rounded-full ${getCourseColor(course.code)}`}>
                    {course.sections.length} 
                  </div>
                </button>

                {expandedCourses.has(course.code) && (
                  <div className="mt-3 space-y-2">
                    {course.sections.map((section, index) => (
                      <div
                        key={index}
                        className={`p-3 rounded-lg border cursor-pointer transition-colors ${
                          isCourseSelected(course, section)
                            ? 'border-ozu-red bg-ozu-red bg-opacity-10'
                            : 'border-gray-200 hover:border-gray-300'
                        }`}
                        onClick={() => onCourseSelection(course, section)}
                      >
                        <div className="flex items-center justify-between mb-2">
                          <div className="font-medium text-gray-900">{section.section}</div>
                          <div className="text-xs text-gray-500">
                            {(() => {
                              // OzU ders sistemi: Her ders 50dk, teneffüs 10dk
                              const calculateActualDuration = (startTime, endTime) => {
                                const [startHour, startMin] = startTime.split(':').map(Number);
                                const [endHour, endMin] = endTime.split(':').map(Number);
                                
                                const startInMinutes = startHour * 60 + startMin;
                                const endInMinutes = endHour * 60 + endMin;
                                const totalDuration = endInMinutes - startInMinutes;
                                
                                // Kaç ders slotu olduğunu hesapla (her slot 50dk ders + 10dk teneffüs = 60dk)
                                const numberOfSlots = Math.ceil(totalDuration / 60);
                                
                                // Son slotta teneffüs yok, bu yüzden son 10dk'yı çıkar
                                const actualDuration = numberOfSlots * 50;
                                
                                return actualDuration;
                              };
                              
                              const totalActualMinutes = section.schedule.reduce((total, slot) => {
                                return total + calculateActualDuration(slot.start, slot.end);
                              }, 0);
                              
                              const hours = Math.floor(totalActualMinutes / 60);
                              const minutes = totalActualMinutes % 60;
                              
                              if (hours > 0 && minutes > 0) {
                                return `${hours}s ${minutes}dk`;
                              } else if (hours > 0) {
                                return `${hours} saat`;
                              } else {
                                return `${minutes} dakika`;
                              }
                            })()}
                          </div>
                        </div>
                        
                        <div className="flex items-center space-x-2 text-xs text-gray-600 mb-2">
                          <User className="h-3 w-3" />
                          <span>{section.instructor}</span>
                        </div>
                        
                        <div className="space-y-1">
                          {section.schedule.map((slot, slotIndex) => (
                            <div key={slotIndex} className="flex items-center space-x-2 text-xs text-gray-600">
                              <Clock className="h-3 w-3" />
                              <span>{slot.day} {slot.start} - {slot.end}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default CourseList;
