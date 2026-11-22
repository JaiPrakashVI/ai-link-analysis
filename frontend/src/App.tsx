import { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { UrlInput } from './components/UrlInput';
import { TelemetryBar } from './components/TelemetryBar';
import { SeoAuditTab } from './components/SeoAuditTab';
import { CompetitorsTab } from './components/CompetitorsTab';
import { QueriesTab } from './components/QueriesTab';
import { SeoStrategyTab } from './components/SeoStrategyTab';
import { ServicesTab } from './components/ServicesTab';
import { AudienceTab } from './components/AudienceTab';
import type { LinkAnalysisResponse, ApiError } from './types';
import {
  FileCheck2,
  Users2,
  SearchCode,
  KeyRound,
  BriefcaseBusiness,
  Target,
  AlertTriangle,
  Loader2,
} from 'lucide-react';

type TabKey = 'audit' | 'competitors' | 'queries' | 'strategy' | 'services' | 'audience';

const DEFAULT_API_URL = 'https://ai-link-analysis-nwkt.onrender.com';

export default function App() {
  const [apiUrl, setApiUrl] = useState<string>(() => {
    return localStorage.getItem('linkpulse_api_url') || DEFAULT_API_URL;
  });

  const [isLoading, setIsLoading] = useState(false);
  const [currentUrl, setCurrentUrl] = useState('');
  const [data, setData] = useState<LinkAnalysisResponse | null>(null);
  const [error, setError] = useState<ApiError | null>(null);
  const [activeTab, setActiveTab] = useState<TabKey>('audit');
  const [isBackendHealthy, setIsBackendHealthy] = useState<boolean | null>(null);

  // Check health on load or when apiUrl changes
  useEffect(() => {
    localStorage.setItem('linkpulse_api_url', apiUrl);

    const checkHealth = async () => {
      try {
        const res = await fetch(`${apiUrl}/health`);
        if (res.ok) {
          setIsBackendHealthy(true);
        } else {
          setIsBackendHealthy(false);
        }
      } catch {
        setIsBackendHealthy(false);
      }
    };

    checkHealth();
  }, [apiUrl]);

  const handleAnalyze = async (url: string) => {
    setIsLoading(true);
    setError(null);
    setCurrentUrl(url);

    try {
      const res = await fetch(`${apiUrl}/link-analysis`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
      });

      const responseJson = await res.json();

      if (!res.ok) {
        setError({
          detail: responseJson.detail || 'Failed to complete link analysis.',
          error_code: responseJson.error_code || `HTTP_${res.status}`,
        });
        setData(null);
      } else {
        setData(responseJson);
        setActiveTab('audit');
      }
    } catch (err: any) {
      setError({
        detail:
          err.message ||
          'Network connection error reaching backend server. Please verify your connection or Render instance.',
        error_code: 'CLIENT_NETWORK_ERROR',
      });
      setData(null);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRefresh = () => {
    if (currentUrl) {
      handleAnalyze(currentUrl);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#FBFBFD]">
      {/* Header */}
      <Header
        apiUrl={apiUrl}
        setApiUrl={setApiUrl}
        isBackendHealthy={isBackendHealthy}
      />

      {/* Main Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
        
        {/* Search Hero */}
        <UrlInput onAnalyze={handleAnalyze} isLoading={isLoading} />

        {/* Loading Indicator State */}
        {isLoading && (
          <div className="max-w-xl mx-auto my-12 bg-white rounded-3xl border border-ink-200/90 shadow-ios p-8 text-center animate-in fade-in zoom-in-95 duration-200">
            <div className="w-12 h-12 rounded-2xl bg-orange-50 text-orange-600 flex items-center justify-center mx-auto mb-4 border border-orange-200">
              <Loader2 className="w-6 h-6 animate-spin" />
            </div>
            <h3 className="text-base font-bold text-ink-900 mb-1">
              Analyzing Website Architecture
            </h3>
            <p className="text-xs text-ink-500 mb-6 font-normal">
              Running SSRF validation, DOM pre-extraction, and Gemini structured reasoning...
            </p>

            <div className="space-y-2 text-xs font-mono text-ink-600 max-w-sm mx-auto text-left">
              <div className="flex items-center space-x-2">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                <span>1. DNS inspection &amp; SSRF address check</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                <span>2. Deterministic SEO tag extraction &amp; alt audit</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="w-1.5 h-1.5 rounded-full bg-orange-500 animate-pulse" />
                <span>3. Google Gemini structured synthesis &amp; fallback</span>
              </div>
            </div>
          </div>
        )}

        {/* Error State Banner */}
        {error && !isLoading && (
          <div className="max-w-2xl mx-auto my-8 bg-white rounded-2xl border border-rose-200 shadow-ios p-6">
            <div className="flex items-start space-x-3.5">
              <div className="w-9 h-9 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center flex-shrink-0 border border-rose-200">
                <AlertTriangle className="w-5 h-5 stroke-[2.2]" />
              </div>
              <div className="flex-1">
                <div className="flex items-center space-x-2 mb-1">
                  <h3 className="text-sm font-bold text-rose-950">
                    Analysis Request Failed
                  </h3>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-rose-100 text-rose-800 font-semibold">
                    {error.error_code}
                  </span>
                </div>
                <p className="text-xs text-rose-800 leading-relaxed font-normal">
                  {error.detail}
                </p>
                
                {error.error_code === 'SSRF_PROHIBITED_DESTINATION' && (
                  <p className="text-[11px] text-ink-500 mt-2">
                    Security Policy: Loopback addresses (127.0.0.1, localhost) and private RFC 1918 subnets cannot be scanned.
                  </p>
                )}
                {error.error_code === 'NON_HTML_CONTENT' && (
                  <p className="text-[11px] text-ink-500 mt-2">
                    Media Policy: Link analysis requires an HTML document. PDF files, images, and raw binaries cannot be audited.
                  </p>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Analysis Results View */}
        {data && !isLoading && (
          <div className="animate-in fade-in duration-300">
            {/* Top Telemetry & Brand Strip */}
            <TelemetryBar
              metadata={data.metadata}
              brand={data.brand}
              website={data.website}
              onRefresh={handleRefresh}
              fullData={data}
            />

            {/* iOS-Style Segmented Navigation Tab Bar */}
            <div className="flex items-center justify-start overflow-x-auto p-1.5 bg-white rounded-2xl border border-ink-200/90 shadow-subtle mb-8 max-w-full no-scrollbar">
              <button
                onClick={() => setActiveTab('audit')}
                className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all cursor-pointer ${
                  activeTab === 'audit'
                    ? 'bg-orange-500 text-white shadow-sm shadow-orange-500/20'
                    : 'text-ink-600 hover:text-ink-900 hover:bg-ink-50'
                }`}
              >
                <FileCheck2 className="w-3.5 h-3.5" />
                <span>Technical SEO Audit</span>
                {data.technical_seo_audit.images_missing_alt > 0 && (
                  <span className={`text-[10px] font-mono px-1.5 py-0.2 rounded-full ${
                    activeTab === 'audit' ? 'bg-white/20 text-white' : 'bg-orange-100 text-orange-700'
                  }`}>
                    {data.technical_seo_audit.images_missing_alt} alerts
                  </span>
                )}
              </button>

              <button
                onClick={() => setActiveTab('competitors')}
                className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all cursor-pointer ${
                  activeTab === 'competitors'
                    ? 'bg-orange-500 text-white shadow-sm shadow-orange-500/20'
                    : 'text-ink-600 hover:text-ink-900 hover:bg-ink-50'
                }`}
              >
                <Users2 className="w-3.5 h-3.5" />
                <span>Competitors ({data.analysis.competitor_analysis.competitors.length})</span>
              </button>

              <button
                onClick={() => setActiveTab('queries')}
                className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all cursor-pointer ${
                  activeTab === 'queries'
                    ? 'bg-orange-500 text-white shadow-sm shadow-orange-500/20'
                    : 'text-ink-600 hover:text-ink-900 hover:bg-ink-50'
                }`}
              >
                <SearchCode className="w-3.5 h-3.5" />
                <span>Search Queries (5)</span>
              </button>

              <button
                onClick={() => setActiveTab('strategy')}
                className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all cursor-pointer ${
                  activeTab === 'strategy'
                    ? 'bg-orange-500 text-white shadow-sm shadow-orange-500/20'
                    : 'text-ink-600 hover:text-ink-900 hover:bg-ink-50'
                }`}
              >
                <KeyRound className="w-3.5 h-3.5" />
                <span>SEO Strategy &amp; Title</span>
              </button>

              <button
                onClick={() => setActiveTab('services')}
                className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all cursor-pointer ${
                  activeTab === 'services'
                    ? 'bg-orange-500 text-white shadow-sm shadow-orange-500/20'
                    : 'text-ink-600 hover:text-ink-900 hover:bg-ink-50'
                }`}
              >
                <BriefcaseBusiness className="w-3.5 h-3.5" />
                <span>Services ({data.analysis.top_services.length})</span>
              </button>

              <button
                onClick={() => setActiveTab('audience')}
                className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all cursor-pointer ${
                  activeTab === 'audience'
                    ? 'bg-orange-500 text-white shadow-sm shadow-orange-500/20'
                    : 'text-ink-600 hover:text-ink-900 hover:bg-ink-50'
                }`}
              >
                <Target className="w-3.5 h-3.5" />
                <span>Target Audience</span>
              </button>
            </div>

            {/* Active Tab Panel */}
            <div className="transition-all">
              {activeTab === 'audit' && (
                <SeoAuditTab audit={data.technical_seo_audit} />
              )}
              {activeTab === 'competitors' && (
                <CompetitorsTab data={data.analysis.competitor_analysis} />
              )}
              {activeTab === 'queries' && (
                <QueriesTab queries={data.analysis.target_search_queries} />
              )}
              {activeTab === 'strategy' && (
                <SeoStrategyTab
                  seo={data.analysis.seo_improvements}
                  currentTitle={data.technical_seo_audit.title}
                />
              )}
              {activeTab === 'services' && (
                <ServicesTab services={data.analysis.top_services} />
              )}
              {activeTab === 'audience' && (
                <AudienceTab audience={data.analysis.target_audience} />
              )}
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-ink-200/80 bg-white py-6 mt-16 text-center text-xs text-ink-500">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="flex items-center space-x-2">
            <span className="font-bold text-ink-900">LinkPulse Engine</span>
            <span>&bull;</span>
            <span>Powered by Google Gemini 3.1 &amp; FastAPI</span>
          </div>

          <div className="flex items-center space-x-4 text-ink-400">
            <span className="font-mono">Sub-5ms TTL Cache Active</span>
            <span>&bull;</span>
            <a
              href="https://ai-link-analysis-nwkt.onrender.com/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="text-orange-600 hover:underline font-medium"
            >
              Swagger API Docs
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
