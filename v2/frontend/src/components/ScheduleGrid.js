import React from 'react';
import { Calendar, Clock, MapPin, User, X } from 'lucide-react';

const ScheduleGrid = ({ schedule, selectedCourses, onRemoveCourse }) => {
  const days = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma'];
  const timeSlots = [
    '08:40-09:30', '09:40-10:30', '10:40-11:30', '11:40-12:30',
    '12:40-13:30', '13:40-14:30', '14:40-15:30', '15:40-16:30',
    '16:40-17:30', '17:40-18:30'
  ];

  // Gelişmiş renk oluşturma sistemi
  const getCourseColor = (courseCode) => {
    const colors = [
      'bg-blue-500',
      'bg-green-500', 
      'bg-purple-500',
      'bg-orange-500',
      'bg-red-500',
      'bg-yellow-500',
      'bg-indigo-500',
      'bg-pink-500',
      'bg-teal-500',
      'bg-cyan-500',
      'bg-lime-500',
      'bg-amber-500',
      'bg-emerald-500',
      'bg-violet-500',
      'bg-rose-500',
      'bg-sky-500'
    ];
    
    let hash = 0;
    for (let i = 0; i < courseCode.length; i++) {
      hash = courseCode.charCodeAt(i) + ((hash << 5) - hash);
    }
    const index = Math.abs(hash) % colors.length;
    return colors[index];
  };

  // Saat slot'u için ders bulma - Seçilen derslerden kontrol et
  const getCoursesForTimeSlot = (day, timeSlot) => {
    const [startTime] = timeSlot.split('-');
    const courses = [];
    
    // Seçilen derslerden bu saatte olanları bul
    selectedCourses.forEach(course => {
      course.schedule.forEach(slot => {
        if (slot.day === day && slot.start === startTime) {
          courses.push({
            course_code: course.code,
            course_name: course.name,
            section: course.section,
            instructor: course.instructor,
            duration: slot.duration,
            start_time: slot.start,
            end_time: slot.end || '',  // Backend'den gelen end bilgisi
            room: slot.room,
            color: getCourseColor(course.code)
          });
        }
      });
    });
    
    return courses;
  };

  // Ders süresini hesapla - Gerçek süreye göre
  const getDurationHeight = (duration) => {
    return Math.max(1, duration) * 60; // 60px per hour
  };

  // CSS Grid için slot span hesaplama
  const getSlotSpan = (duration) => {
    return Math.max(1, duration); // 1 saat = 1 slot, 2 saat = 2 slot, 3 saat = 3 slot
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center space-x-2">
          <Calendar className="h-5 w-5 text-ozu-blue" />
          <h2 className="text-lg font-semibold text-gray-900">Haftalık Program</h2>
        </div>
        {selectedCourses.length > 0 && (
          <p className="text-sm text-gray-600 mt-1">
            {selectedCourses.length} ders seçildi
          </p>
        )}
      </div>

      {/* Program Grid */}
      <div className="overflow-x-auto">
        <div className="min-w-full">
          {/* Gün başlıkları */}
          <div className="grid grid-cols-6 border-b border-gray-200">
            <div className="p-3 bg-gray-50 border-r border-gray-200">
              <div className="text-sm font-medium text-gray-900">Saat</div>
            </div>
            {days.map((day) => (
              <div key={day} className="p-3 bg-gray-50 border-r border-gray-200 last:border-r-0">
                <div className="text-sm font-medium text-gray-900">{day}</div>
              </div>
            ))}
          </div>

          {/* Zaman slot'ları */}
          {timeSlots.map((timeSlot, timeIndex) => (
            <div key={timeIndex} className="grid grid-cols-6 border-b border-gray-200 last:border-b-0">
              {/* Saat */}
              <div className="p-3 border-r border-gray-200 bg-gray-50">
                <div className="text-xs text-gray-600">{timeSlot}</div>
              </div>
              
              {/* Günler */}
              {days.map((day) => {
                const courses = getCoursesForTimeSlot(day, timeSlot);
                
                return (
                  <div key={day} className="p-1 border-r border-gray-200 last:border-r-0 min-h-[60px] relative">
                    {courses.length > 0 ? (
                      <div className="space-y-1">
                        {courses.map((course, courseIndex) => (
                          <div
                            key={courseIndex}
                            className={`p-2 rounded text-white text-xs relative group ${course.color}`}
                            style={{
                              height: `${getDurationHeight(course.duration)}px`,
                              minHeight: '40px',
                              position: 'absolute',
                              top: '4px',
                              left: '4px',
                              right: '4px',
                              zIndex: 10
                            }}
                          >
                            <div className="font-medium">{course.course_code}</div>
                            <div className="text-xs opacity-90">{course.section}</div>
                            <div className="text-xs opacity-75 mt-1">
                              {course.start_time} - {course.end_time}
                            </div>
                            <div className="flex items-center space-x-1 mt-1 opacity-75">
                              <MapPin className="h-3 w-3" />
                              <span>{course.room}</span>
                            </div>
                            {/* Takvimdeki derslere silme butonu - Hover'da görünür */}
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                onRemoveCourse(course.course_code, course.section);
                              }}
                              className="absolute top-1 right-1 text-white hover:text-red-200 transition-colors opacity-0 group-hover:opacity-100 bg-black bg-opacity-20 rounded-full p-1"
                              title="Dersi kaldır"
                            >
                              <X className="h-3 w-3" />
                            </button>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div className="h-full flex items-center justify-center">
                        <div className="text-gray-300 text-xs">-</div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          ))}
        </div>
      </div>

      {/* Seçili dersler özeti */}
      {selectedCourses.length > 0 && (
        <div className="p-4 border-t border-gray-200 bg-gray-50">
          <h3 className="text-sm font-medium text-gray-700 mb-3">Seçili Dersler</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {selectedCourses.map((course, index) => (
              <div key={index} className="flex items-center space-x-3 p-2 bg-white rounded border relative group">
                <div className={`w-3 h-3 rounded-full ${getCourseColor(course.code)}`}></div>
                <div className="flex-1">
                  <div className="text-sm font-medium text-gray-900">{course.code}</div>
                  <div className="text-xs text-gray-600">{course.section}</div>
                </div>
                <div className="text-xs text-gray-500">
                  <User className="h-3 w-3 inline mr-1" />
                  {course.instructor}
                </div>
                {/* Çarpı butonu */}
                <button
                  onClick={() => onRemoveCourse(course.code, course.section)}
                  className="absolute top-1 right-1 text-gray-400 hover:text-red-500 transition-colors opacity-0 group-hover:opacity-100"
                  title="Dersi kaldır"
                >
                  <X className="h-4 w-4" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ScheduleGrid;
