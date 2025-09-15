import React, { useState, useRef, useEffect } from 'react';
import { Calendar, User, X, Download, Trash2, ChevronDown } from 'lucide-react';
import { toast } from 'react-hot-toast';
import html2canvas from 'html2canvas';

const ScheduleGrid = ({ schedule, selectedCourses, onRemoveCourse, onClearAll }) => {
  const [showExportDropdown, setShowExportDropdown] = useState(false);
  const [showTopExportDropdown, setShowTopExportDropdown] = useState(false);
  const scheduleGridRef = useRef(null);
  
  const days = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma'];
  const timeSlots = [
    '08:40-09:30', '09:40-10:30', '10:40-11:30', '11:40-12:30',
    '12:40-13:30', '13:40-14:30', '14:40-15:30', '15:40-16:30',
    '16:40-17:30', '17:40-18:30'
  ];

  // PNG export fonksiyonu
  const exportScheduleToPng = async () => {
    if (selectedCourses.length === 0) {
      alert('Önce ders seçmeniz gerekiyor!');
      return;
    }

    try {
      const gridElement = scheduleGridRef.current;
      if (!gridElement) {
        toast.error('Ders programı bulunamadı!');
        return;
      }

      toast.loading('PNG dosyası hazırlanıyor...', {
        duration: 2000,
        position: 'top-center',
      });

      // Scroll pozisyonunu sıfırla
      const originalScrollTop = gridElement.scrollTop;
      const originalScrollLeft = gridElement.scrollLeft;
      gridElement.scrollTop = 0;
      gridElement.scrollLeft = 0;

      const canvas = await html2canvas(gridElement, {
        scale: 1.5,
        useCORS: true,
        allowTaint: true,
        backgroundColor: '#ffffff',
        logging: false,
        width: gridElement.scrollWidth,
        height: gridElement.scrollHeight
      });

      // Scroll pozisyonunu geri yükle
      gridElement.scrollTop = originalScrollTop;
      gridElement.scrollLeft = originalScrollLeft;

      const link = document.createElement('a');
      link.download = `ders_programi_${new Date().toISOString().split('T')[0]}.png`;
      link.href = canvas.toDataURL('image/png', 0.95);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      toast.success('Ders programı başarıyla PNG olarak indirildi!', {
        duration: 3000,
        position: 'top-center',
      });
    } catch (error) {
      console.error('PNG export hatası:', error);
      toast.error('PNG dosyası oluşturulurken bir hata oluştu: ' + error.message);
    }
  };

  // Dropdown dışına tıklandığında kapatma
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (showExportDropdown && !event.target.closest('.export-dropdown')) {
        setShowExportDropdown(false);
      }
      if (showTopExportDropdown && !event.target.closest('.top-export-dropdown')) {
        setShowTopExportDropdown(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [showExportDropdown, showTopExportDropdown]);

  // Program export fonksiyonu
  const exportScheduleToTxt = () => {
    if (selectedCourses.length === 0) {
      alert('Önce ders seçmeniz gerekiyor!');
      return;
    }

    let content = '';
    content += '==============================================\n';
    content += '           HAFTALIK DERS PROGRAMI\n';
    content += '==============================================\n\n';
    
    // Toplam ders sayısı
    content += `Toplam Seçili Ders Sayısı: ${selectedCourses.length}\n\n`;
    
    // Ders listesi
    content += 'SEÇİLİ DERSLER:\n';
    content += '==============================================\n';
    selectedCourses.forEach((course, index) => {
      content += `${index + 1}. ${course.code} - ${course.name}\n`;
      content += `   Bölüm: ${course.section}\n`;
      content += `   Öğretim Görevlisi: ${course.instructor}\n`;
      content += '   Program:\n';
      
      course.schedule.forEach(slot => {
        const endTime = slot.end || (slot.duration > 1 ? 
          timeSlots[timeSlots.findIndex(ts => ts.startsWith(slot.start)) + slot.duration - 1]?.split('-')[1] || '' 
          : timeSlots.find(ts => ts.startsWith(slot.start))?.split('-')[1] || '');
        
        content += `     ${slot.day}: ${slot.start} - ${endTime}`;
        if (slot.duration > 1) {
          content += ` (${slot.duration} saat)`;
        }
        content += ` - ${slot.room}\n`;
      });
      content += '\n';
    });
    
    // Günlük program
    content += '\nGÜNLÜK PROGRAM:\n';
    content += '==============================================\n';
    
    days.forEach(day => {
      content += `\n${day.toUpperCase()}:\n`;
      content += '----------------------------------------------\n';
      
      let dayHasCourses = false;
      const daySchedule = [];
      
      // Bu günün derslerini topla ve saate göre sırala
      selectedCourses.forEach(course => {
        course.schedule.forEach(slot => {
          if (slot.day === day) {
            const endTime = slot.end || (slot.duration > 1 ? 
              timeSlots[timeSlots.findIndex(ts => ts.startsWith(slot.start)) + slot.duration - 1]?.split('-')[1] || '' 
              : timeSlots.find(ts => ts.startsWith(slot.start))?.split('-')[1] || '');
            
            daySchedule.push({
              start: slot.start,
              end: endTime,
              code: course.code,
              name: course.name,
              section: course.section,
              instructor: course.instructor,
              room: slot.room,
              duration: slot.duration
            });
            dayHasCourses = true;
          }
        });
      });
      
      if (dayHasCourses) {
        // Saate göre sırala
        daySchedule.sort((a, b) => a.start.localeCompare(b.start));
        
        daySchedule.forEach(slot => {
          content += `${slot.start} - ${slot.end}  ${slot.code} (${slot.section})\n`;
          content += `                    ${slot.name}\n`;
          content += `                    Öğr. Gör.: ${slot.instructor}\n`;
          content += `                    Oda: ${slot.room}`;
          if (slot.duration > 1) {
            content += ` (${slot.duration} saat)`;
          }
          content += '\n\n';
        });
      } else {
        content += 'Bu günde ders yok.\n\n';
      }
    });
    
    content += '\n==============================================\n';
    content += `Oluşturulma Tarihi: ${new Date().toLocaleString('tr-TR')}\n`;
    content += '==============================================\n';
    
    // Dosyayı indirilebilir hale getir
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `ders_programi_${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    
    // Başarı bildirimi
    toast.success('Ders programı başarıyla TXT olarak indirildi!', {
      duration: 3000,
      position: 'top-center',
    });
  };

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

  // Belirli bir time slot'un bir dersin devamı olup olmadığını kontrol et
  const isContinuationSlot = (day, timeSlot) => {
    const [currentStartTime] = timeSlot.split('-');
    
    // Seçilen derslerden bu günde daha önceki saatlerde başlayan dersler var mı?
    for (const course of selectedCourses) {
      for (const slot of course.schedule) {
        if (slot.day === day && slot.duration > 1) {
          // Bu dersin başlangıç saati mevcut slot'un başlangıcından önce mi?
          // Ve dersin süresi bu slot'u kapsıyor mu?
          
          const slotStartTime = slot.start; // Örnek: "13:40"
          
          // Eğer slot bu dersin başlangıç saati değilse ve dersin süresine dahilse
          if (slotStartTime !== currentStartTime) {
            // Zaman sırasını kontrol et - slot başlangıcından sonraki slotlar devam slot'u olabilir
            const timeSlotIndex = timeSlots.findIndex(ts => ts.startsWith(currentStartTime));
            const courseSlotIndex = timeSlots.findIndex(ts => ts.startsWith(slotStartTime));
            
            // Eğer mevcut slot, dersin başladığı slottan sonra ve dersin süresi kapsamında ise
            if (timeSlotIndex > courseSlotIndex && 
                timeSlotIndex <= courseSlotIndex + slot.duration - 1) {
              return {
                isContinuation: true,
                originalCourse: course,
                originalSlot: slot
              };
            }
          }
        }
      }
    }
    
    return { isContinuation: false };
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Calendar className="h-5 w-5 text-ozu-red" />
            <h2 className="text-lg font-semibold text-gray-900">Haftalık Program</h2>
          </div>
          {selectedCourses.length > 0 && (
            <div className="flex items-center space-x-2">
              <button
                onClick={onClearAll}
                className="flex items-center space-x-2 bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors text-sm"
                title="Tüm dersleri temizle"
              >
                <Trash2 className="h-4 w-4" />
                <span>Temizle</span>
              </button>
              
              {/* Top Export Dropdown */}
              <div className="relative top-export-dropdown">
                <button
                  onClick={() => setShowTopExportDropdown(!showTopExportDropdown)}
                  className="flex items-center space-x-2 bg-ozu-red text-white px-4 py-2 rounded-lg hover:bg-opacity-90 transition-colors text-sm"
                  title="Programı export et"
                >
                  <Download className="h-4 w-4" />
                  <span>Export</span>
                  <ChevronDown className="h-3 w-3" />
                </button>
                
                {showTopExportDropdown && (
                  <div className="absolute right-0 mt-1 w-36 bg-white rounded-md shadow-lg border border-gray-200 z-50">
                    <div className="py-1">
                      <button
                        onClick={() => {
                          exportScheduleToTxt();
                          setShowTopExportDropdown(false);
                        }}
                        className="flex items-center w-full px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
                      >
                        <Download className="h-4 w-4 mr-2" />
                        <span>as TXT</span>
                      </button>
                      <button
                        onClick={() => {
                          exportScheduleToPng();
                          setShowTopExportDropdown(false);
                        }}
                        className="flex items-center w-full px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
                      >
                        <Download className="h-4 w-4 mr-2" />
                        <span>as PNG</span>
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
        {selectedCourses.length > 0 && (
          <p className="text-sm text-gray-600 mt-1">
            {selectedCourses.length} ders seçildi
          </p>
        )}
      </div>

      {/* Program Grid */}
      <div className="overflow-x-auto" ref={scheduleGridRef}>
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
                const continuationInfo = isContinuationSlot(day, timeSlot);
                
                return (
                  <div key={day} className="p-1 border-r border-gray-200 last:border-r-0 min-h-[60px] relative">
                    {continuationInfo.isContinuation ? (
                      // Bu slot bir dersin devamı
                      <div
                        className={`p-2 rounded text-white text-xs relative ${getCourseColor(continuationInfo.originalCourse.code)}`}
                        style={{
                          height: '52px',
                          minHeight: '40px',
                          position: 'absolute',
                          top: '4px',
                          left: '4px',
                          right: '4px',
                          zIndex: 5,
                          opacity: 0.7,
                          border: '2px dashed rgba(255,255,255,0.4)',
                          borderTop: '2px solid rgba(255,255,255,0.6)'
                        }}
                      >
                        <div className="font-medium text-center opacity-90 text-xs">
                          {continuationInfo.originalCourse.code}
                        </div>
                        <div className="text-xs opacity-70 text-center">{continuationInfo.originalCourse.section}</div>
                        <div className="text-xs opacity-60 text-center mt-1">(devamı)</div>
                      </div>
                    ) : courses.length > 0 ? (
                      <div className="space-y-1">
                        {courses.map((course, courseIndex) => {
                          // Dersin gerçek yüksekliğini hesapla
                          const actualHeight = course.duration > 1 ? (course.duration * 60) : 52;
                          
                          return (
                            <div
                              key={courseIndex}
                              className={`p-2 rounded text-white text-xs relative group ${course.color}`}
                              style={{
                                height: `${actualHeight}px`,
                                minHeight: '40px',
                                position: 'absolute',
                                top: '4px',
                                left: '4px',
                                right: '4px',
                                zIndex: 10
                              }}
                            >
                              <div className="font-medium">{course.section}</div>
                              <div className="text-xs opacity-75 mt-1">
                                {course.start_time} - {course.end_time}
                              </div>
                              {course.duration > 1 && (
                                <div className="text-xs opacity-75 mt-1 font-medium">
                                  ({course.duration} saat)
                                </div>
                              )}
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
                          );
                        })}
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
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-medium text-gray-700">Seçili Dersler</h3>
            <div className="flex items-center space-x-2">
              <button
                onClick={onClearAll}
                className="flex items-center space-x-1 bg-red-600 text-white px-3 py-1.5 rounded text-xs hover:bg-red-700 transition-colors"
                title="Tüm dersleri temizle"
              >
                <Trash2 className="h-3 w-3" />
                <span>Temizle</span>
              </button>
              
              {/* Export Dropdown */}
              <div className="relative export-dropdown">
                <button
                  onClick={() => setShowExportDropdown(!showExportDropdown)}
                  className="flex items-center space-x-1 bg-green-600 text-white px-3 py-1.5 rounded text-xs hover:bg-green-700 transition-colors"
                  title="Programı export et"
                >
                  <Download className="h-3 w-3" />
                  <span>Export</span>
                  <ChevronDown className="h-3 w-3" />
                </button>
                
                {showExportDropdown && (
                  <div className="absolute right-0 mt-1 w-32 bg-white rounded-md shadow-lg border border-gray-200 z-50">
                    <div className="py-1">
                      <button
                        onClick={() => {
                          exportScheduleToTxt();
                          setShowExportDropdown(false);
                        }}
                        className="flex items-center w-full px-3 py-2 text-xs text-gray-700 hover:bg-gray-100 transition-colors"
                      >
                        <Download className="h-3 w-3 mr-2" />
                        <span>as TXT</span>
                      </button>
                      <button
                        onClick={() => {
                          exportScheduleToPng();
                          setShowExportDropdown(false);
                        }}
                        className="flex items-center w-full px-3 py-2 text-xs text-gray-700 hover:bg-gray-100 transition-colors"
                      >
                        <Download className="h-3 w-3 mr-2" />
                        <span>as PNG</span>
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
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
