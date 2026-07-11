import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

import { AppSidebar } from './components/layout/AppSidebar';
import { Header } from './components/layout/Header';

import { DashboardPage } from './pages/DashboardPage';
import { StudentsPage } from './pages/StudentsPage';
import { StudentDetailPage } from './pages/StudentDetailPage';
import { ReviewQueuePage } from './pages/ReviewQueuePage';
import { AnalyticsPage } from './pages/AnalyticsPage';
import { ReportsPage } from './pages/ReportsPage';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

// Helper component to resolve dynamic headers based on route
const AppLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const location = useLocation();
  
  const getHeaderTitle = (pathname: string) => {
    if (pathname === '/') return 'Co-Pilot Overview';
    if (pathname === '/students') return 'Student Registry Database';
    if (pathname.startsWith('/students/')) return 'Focused Student Workspace';
    if (pathname === '/reviews') return 'Advisor Review Queue';
    if (pathname === '/analytics') return 'Cohort Risk Trends & Metrics';
    if (pathname === '/reports') return 'Intervention Reports Panel';
    return 'EduPilot AI Workspace';
  };

  return (
    <div className="flex bg-slate-50 min-h-screen text-slate-800 antialiased font-sans">
      <AppSidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <Header title={getHeaderTitle(location.pathname)} />
        <div className="flex-1 overflow-y-auto">
          {children}
        </div>
      </div>
    </div>
  );
};

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AppLayout>
          <Routes>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/students" element={<StudentsPage />} />
            <Route path="/students/:id" element={<StudentDetailPage />} />
            <Route path="/reviews" element={<ReviewQueuePage />} />
            <Route path="/analytics" element={<AnalyticsPage />} />
            <Route path="/reports" element={<ReportsPage />} />
          </Routes>
        </AppLayout>
      </BrowserRouter>
    </QueryClientProvider>
  );
}
