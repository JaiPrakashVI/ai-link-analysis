import React, { useState } from 'react';
import { Activity, Settings } from 'lucide-react';

interface HeaderProps {
  apiUrl: string;
  setApiUrl: (url: string) => void;
  isBackendHealthy: boolean | null;
}

export const Header: React.FC<HeaderProps> = ({
  apiUrl,
  setApiUrl,
  isBackendHealthy,
}) => {
  const [showSettings, setShowSettings] = useState(false);
  const [tempUrl, setTempUrl] = useState(apiUrl);

  const handleSaveUrl = (e: React.FormEvent) => {
    e.preventDefault();
    setApiUrl(tempUrl.trim());
    setShowSettings(false);
  };

  return (
    <header className="border-b border-ink-200/80 bg-white/80 backdrop-blur-md sticky top-0 z-30 transition-all">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Brand identity */}
        <div className="flex items-center space-x-3">
          <div className="w-9 h-9 rounded-xl bg-orange-500 flex items-center justify-center shadow-sm shadow-orange-500/20">
            <Activity className="w-5 h-5 text-white stroke-[2.5]" />
          </div>
          <div className="flex items-center space-x-2">
            <span className="font-extrabold text-lg tracking-tight text-ink-900">
              Link<span className="text-orange-500">Pulse</span>
            </span>
            <span className="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-ink-100 text-ink-700 tracking-wide border border-ink-200">
              Enterprise
            </span>
          </div>
        </div>

        {/* Backend status & links */}
        <div className="flex items-center space-x-3">
          
          {/* Health indicator badge */}
          <div className="hidden sm:flex items-center space-x-2 px-3 py-1 rounded-full text-xs font-medium bg-ink-50 border border-ink-200/80">
            <span className="relative flex h-2 w-2">
              <span
                className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${
                  isBackendHealthy ? 'bg-emerald-400' : 'bg-amber-400'
                }`}
              ></span>
              <span
                className={`relative inline-flex rounded-full h-2 w-2 ${
                  isBackendHealthy ? 'bg-emerald-500' : 'bg-amber-500'
                }`}
              ></span>
            </span>
            <span className="text-ink-600 font-mono text-[11px]">
              {isBackendHealthy ? 'Backend Active' : 'Checking status...'}
            </span>
          </div>

          {/* Settings modal trigger */}
          <div className="relative">
            <button
              onClick={() => setShowSettings(!showSettings)}
              title="API Endpoint Configuration"
              className="p-2 rounded-lg text-ink-500 hover:text-ink-900 hover:bg-ink-100 transition-colors border border-transparent hover:border-ink-200"
            >
              <Settings className="w-4 h-4" />
            </button>

            {showSettings && (
              <div className="absolute right-0 mt-2 w-80 bg-white rounded-2xl shadow-ios p-4 border border-ink-200 z-50 animate-in fade-in zoom-in-95 duration-150">
                <div className="text-xs font-semibold text-ink-900 mb-1">API Backend Endpoint</div>
                <p className="text-[11px] text-ink-500 mb-3">
                  Default points to live Render deployment. Change to localhost for local testing.
                </p>
                <form onSubmit={handleSaveUrl} className="space-y-3">
                  <input
                    type="text"
                    value={tempUrl}
                    onChange={(e) => setTempUrl(e.target.value)}
                    className="w-full text-xs font-mono px-3 py-2 rounded-lg border border-ink-300 focus:outline-none focus:ring-2 focus:ring-orange-500/20 focus:border-orange-500"
                    placeholder="https://..."
                  />
                  <div className="flex justify-between items-center pt-1">
                    <button
                      type="button"
                      onClick={() => {
                        setTempUrl('https://ai-link-analysis-nwkt.onrender.com');
                      }}
                      className="text-[11px] text-orange-600 hover:underline"
                    >
                      Reset default
                    </button>
                    <button
                      type="submit"
                      className="px-3 py-1.5 bg-orange-500 text-white rounded-lg text-xs font-medium hover:bg-orange-600 transition-colors shadow-sm"
                    >
                      Apply
                    </button>
                  </div>
                </form>
              </div>
            )}
          </div>

          {/* GitHub link with vector icon */}
          <a
            href="https://github.com/JaiPrakashVI/ai-link-analysis"
            target="_blank"
            rel="noopener noreferrer"
            className="p-2 rounded-lg text-ink-500 hover:text-ink-900 hover:bg-ink-100 transition-colors border border-transparent hover:border-ink-200"
            title="View Source on GitHub"
          >
            <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24">
              <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
            </svg>
          </a>
        </div>
      </div>
    </header>
  );
};
