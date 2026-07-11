import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Users, 
  ClipboardCheck, 
  BarChart3, 
  FileSpreadsheet, 
  GraduationCap
} from 'lucide-react';
import { cn } from '../../lib/utils';

export const AppSidebar: React.FC = () => {
  const menuItems = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'Students', path: '/students', icon: Users },
    { name: 'Review Queue', path: '/reviews', icon: ClipboardCheck },
    { name: 'Analytics', path: '/analytics', icon: BarChart3 },
    { name: 'Reports', path: '/reports', icon: FileSpreadsheet },
  ];

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 text-slate-300 flex flex-col h-screen sticky top-0">
      {/* Brand Section */}
      <div className="p-6 border-b border-slate-800 flex items-center gap-3">
        <GraduationCap className="h-8 w-8 text-blue-500 animate-pulse" />
        <div>
          <h1 className="font-bold text-lg text-white tracking-wide">EduPilot AI</h1>
          <span className="text-xs text-slate-500 font-medium">Student Success Co-Pilot</span>
        </div>
      </div>

      {/* Navigation Menu */}
      <nav className="flex-1 px-4 py-6 space-y-1.5">
        {menuItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.name}
              to={item.path}
              className={({ isActive }) =>
                cn(
                  "flex items-center gap-3.5 px-4 py-3 rounded-xl font-medium transition-all duration-300 group",
                  isActive 
                    ? "bg-blue-600 text-white shadow-lg shadow-blue-600/10" 
                    : "text-slate-400 hover:bg-slate-800/60 hover:text-white"
                )
              }
            >
              <Icon className="h-5 w-5 transition-transform duration-300 group-hover:scale-110" />
              <span>{item.name}</span>
            </NavLink>
          );
        })}
      </nav>

      {/* Footer Info */}
      <div className="p-6 border-t border-slate-800 text-center">
        <p className="text-xs text-slate-600 font-medium">v1.0.0 © EduPilot AI</p>
      </div>
    </aside>
  );
};
