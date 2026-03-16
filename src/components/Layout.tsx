import { Link, Outlet, useLocation } from 'react-router-dom';
import { Briefcase, ChevronRight, Home, Menu, X } from 'lucide-react';
import { useState } from 'react';
import { companyInfo, jobs } from '../data';

export default function Layout() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const location = useLocation();

  const toggleMobileMenu = () => setIsMobileMenuOpen(!isMobileMenuOpen);
  const closeMobileMenu = () => setIsMobileMenuOpen(false);

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col md:flex-row font-sans text-slate-900">
      {/* Mobile Header */}
      <header className="md:hidden bg-white border-b border-slate-200 p-4 flex items-center justify-between sticky top-0 z-20">
        <Link to="/" className="flex items-center gap-2" onClick={closeMobileMenu}>
          <img src={companyInfo.logo} alt={companyInfo.name} className="h-8 object-contain" referrerPolicy="no-referrer" />
        </Link>
        <button onClick={toggleMobileMenu} className="p-2 text-slate-500 hover:text-slate-900 focus:outline-none">
          <Menu size={24} />
        </button>
      </header>

      {/* Sidebar */}
      <aside
        className={`
          fixed inset-y-0 left-0 z-40 w-64 bg-white border-r border-slate-200 transform transition-transform duration-300 ease-in-out md:relative md:translate-x-0 flex flex-col
          ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full'}
        `}
      >
        <div className="p-4 flex items-center justify-between md:hidden border-b border-slate-100">
          <Link to="/" onClick={closeMobileMenu}>
            <img src={companyInfo.logo} alt={companyInfo.name} className="h-8 object-contain" referrerPolicy="no-referrer" />
          </Link>
          <button onClick={closeMobileMenu} className="p-2 text-slate-500 hover:text-slate-900 focus:outline-none">
            <X size={24} />
          </button>
        </div>
        <div className="p-6 hidden md:block border-b border-slate-100">
          <Link to="/" className="block">
            <img src={companyInfo.logo} alt={companyInfo.name} className="h-10 object-contain" referrerPolicy="no-referrer" />
          </Link>
        </div>

        <nav className="flex-1 overflow-y-auto py-6 px-4 space-y-8">
          <div>
            <h3 className="px-3 text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Company</h3>
            <ul className="space-y-1">
              <li>
                <Link
                  to="/"
                  onClick={closeMobileMenu}
                  className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                    location.pathname === '/'
                      ? 'bg-blue-50 text-blue-700'
                      : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                  }`}
                >
                  <Home size={18} />
                  Overview
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="px-3 text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Open Positions</h3>
            <ul className="space-y-1">
              {jobs.map((job) => {
                const isActive = location.pathname === `/jobs/${job.id}`;
                return (
                  <li key={job.id}>
                    <Link
                      to={`/jobs/${job.id}`}
                      onClick={closeMobileMenu}
                      className={`group flex items-center justify-between px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                        isActive
                          ? 'bg-blue-50 text-blue-700'
                          : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                      }`}
                    >
                      <div className="flex min-w-0 items-center gap-3">
                        <Briefcase size={18} className={`shrink-0 ${isActive ? 'text-blue-500' : 'text-slate-400 group-hover:text-slate-600'}`} />
                        <span className="truncate">{job.title}</span>
                      </div>
                      <ChevronRight size={16} className={`shrink-0 ${isActive ? 'text-blue-500' : 'text-slate-300 opacity-0 group-hover:opacity-100 transition-opacity'}`} />
                    </Link>
                  </li>
                );
              })}
            </ul>
          </div>
        </nav>
        
        <div className="p-4 border-t border-slate-100 text-xs text-slate-400 text-center">
          &copy; {new Date().getFullYear()} Mobigator Technology Group
        </div>
      </aside>

      {/* Mobile Overlay */}
      {isMobileMenuOpen && (
        <div 
          className="fixed inset-0 bg-slate-900/20 backdrop-blur-sm z-30 md:hidden"
          onClick={closeMobileMenu}
        />
      )}

      {/* Main Content */}
      <main className="flex-1 min-w-0 overflow-y-auto flex flex-col">
        <div className="flex-1 max-w-4xl w-full mx-auto p-6 md:p-10 lg:p-12">
          <Outlet />
        </div>

        {/* Footer */}
        <footer className="bg-white border-t border-slate-200 py-8 px-6 mt-auto">
          <div className="max-w-4xl mx-auto text-center text-sm text-slate-500 space-y-2">
            <p>
              11/F, Suite B, KPP, 55 King Yip Street<br />
              Kwun Tong, Hong Kong
            </p>
            <p>Tel (852) 5668 3298 &nbsp;|&nbsp; Fax (852) 2524 9050</p>
            <p>
              <a href="mailto:jobs@mobigator.com" className="hover:text-blue-600 transition-colors">jobs@mobigator.com</a>
              {' '}&bull;{' '}
              <a href="https://www.mobigator.com" target="_blank" rel="noopener noreferrer" className="hover:text-blue-600 transition-colors">www.mobigator.com</a>
            </p>
          </div>
        </footer>
      </main>
    </div>
  );
}
