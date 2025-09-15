import React, { useState, useEffect } from 'react';
import { Toaster, toast } from 'react-hot-toast';
import axios from 'axios';
import Header from './components/Header';
import CourseList from './components/CourseList';
import ScheduleGrid from './components/ScheduleGrid';
import ConflictModal from './components/ConflictModal';
import LoadingSpinner from './components/LoadingSpinner';

// API base URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001';

function App() {
  const [courses, setCourses] = useState([]);
  const [selectedCourses, setSelectedCourses] = useState([]);
  const [schedule, setSchedule] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showConflicts, setShowConflicts] = useState(false);
  const [conflicts, setConflicts] = useState([]);

  // Dersleri yükle
  useEffect(() => {
    const fetchCourses = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`${API_BASE_URL}/courses`);
        setCourses(response.data.courses);
        setError(null);
      } catch (err) {
        console.error('Dersler yüklenirken hata:', err);
        setError('Dersler yüklenirken bir hata oluştu. Lütfen sayfayı yenileyin.');
      } finally {
        setLoading(false);
      }
    };

    fetchCourses();
  }, []);

  // Seçilen dersler değiştiğinde program oluştur
  useEffect(() => {
    if (selectedCourses.length > 0) {
      generateSchedule();
      checkConflicts();
    } else {
      setSchedule({});
      setConflicts([]);
    }
  }, [selectedCourses]);

  // Program oluştur
  const generateSchedule = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/generate-schedule`, {
        selected_courses: selectedCourses.map(course => course.code)
      });
      setSchedule(response.data.schedule);
    } catch (err) {
      console.error('Program oluşturulurken hata:', err);
    }
  };

  // Çakışma kontrolü
  const checkConflicts = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/check-conflicts`, {
        courses: selectedCourses.map(course => course.code)
      });
      
      if (response.data.has_conflicts) {
        setConflicts(response.data.conflicts);
        setShowConflicts(true);
      } else {
        setConflicts([]);
        setShowConflicts(false);
      }
    } catch (err) {
      console.error('Çakışma kontrolü yapılırken hata:', err);
    }
  };

  // Çakışma kontrolü fonksiyonu - Kendi ile çakışma kontrolünü düzelt
  const checkTimeConflict = (newCourse, newSection) => {
    const newSchedule = newSection.schedule;
    
    for (const selectedCourse of selectedCourses) {
      // Aynı dersin farklı section'ı ise çakışma sayma
      if (selectedCourse.code === newCourse.code) {
        continue;
      }
      
      for (const selectedSlot of selectedCourse.schedule) {
        for (const newSlot of newSchedule) {
          // Aynı gün ve saatte çakışma kontrolü
          if (selectedSlot.day === newSlot.day && selectedSlot.start === newSlot.start) {
            return {
              hasConflict: true,
              conflictDetails: {
                existingCourse: selectedCourse.code,
                existingSection: selectedCourse.section,
                newCourse: newCourse.code,
                newSection: newSection.section,
                day: selectedSlot.day,
                time: selectedSlot.start,
                room: selectedSlot.room
              }
            };
          }
        }
      }
    }
    
    return { hasConflict: false };
  };

  // Ders seçimi - Çakışma kontrolü ile
  const handleCourseSelection = (course, section) => {
    // Eğer aynı dersin farklı section'ı seçiliyorsa, önce onu kaldır
    const isSameCourseSelected = selectedCourses.some(c => c.code === course.code);
    
    if (isSameCourseSelected) {
      // Aynı dersin mevcut section'ını kaldır
      setSelectedCourses(prev => prev.filter(c => c.code !== course.code));
      toast.success(`${course.code} (${section.section}) ile değiştirildi!`);
      return;
    }
    
    // Çakışma kontrolü
    const conflictCheck = checkTimeConflict(course, section);
    
    if (conflictCheck.hasConflict) {
      // Çakışma varsa uyarı göster
      toast.error(
        `Çakışma tespit edildi! ${conflictCheck.conflictDetails.existingCourse} (${conflictCheck.conflictDetails.existingSection}) ve ${conflictCheck.conflictDetails.newCourse} (${conflictCheck.conflictDetails.newSection}) aynı saatte (${conflictCheck.conflictDetails.day} ${conflictCheck.conflictDetails.time})`,
        {
          duration: 5000,
          position: "top-center",
        }
      );
      return; // Dersi ekleme
    }
    
    // Çakışma yoksa dersi ekle
    setSelectedCourses(prev => [...prev, {
      code: course.code,
      name: course.name,
      section: section.section,
      instructor: section.instructor,
      schedule: section.schedule
    }]);
    
    // Başarı mesajı
    toast.success(`${course.code} (${section.section}) başarıyla eklendi!`);
  };

  // Ders kaldırma fonksiyonu
  const removeCourse = (courseCode, section) => {
    setSelectedCourses(prev => 
      prev.filter(c => !(c.code === courseCode && c.section === section))
    );
    toast.success(`${courseCode} (${section}) kaldırıldı!`);
  };

  // Tüm dersleri temizle
  const clearAllCourses = () => {
    if (selectedCourses.length === 0) {
      toast.error('Temizlenecek ders bulunamadı!');
      return;
    }
    
    const courseCount = selectedCourses.length;
    setSelectedCourses([]);
    setSchedule({});
    setConflicts([]);
    toast.success(`${courseCount} ders programdan temizlendi!`);
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Hata</h1>
          <p className="text-gray-600 mb-4">{error}</p>
          <button 
            onClick={() => window.location.reload()}
            className="bg-ozu-blue text-white px-4 py-2 rounded-lg hover:bg-ozu-light-blue transition-colors"
          >
            Sayfayı Yenile
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Toaster position="top-right" />
      
      <Header />
      
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sol Panel - Ders Listesi */}
          <div className="lg:col-span-1">
            <CourseList 
              courses={courses}
              selectedCourses={selectedCourses}
              onCourseSelection={handleCourseSelection}
              onRemoveCourse={removeCourse}
            />
          </div>
          
          {/* Ana Panel - Program Grid */}
          <div className="lg:col-span-3">
            <ScheduleGrid 
              schedule={schedule}
              selectedCourses={selectedCourses}
              onRemoveCourse={removeCourse}
              onClearAll={clearAllCourses}
            />
          </div>
        </div>
      </div>

      {/* Çakışma Modal */}
      {showConflicts && (
        <ConflictModal 
          conflicts={conflicts}
          onClose={() => setShowConflicts(false)}
        />
      )}
    </div>
  );
}

export default App;
