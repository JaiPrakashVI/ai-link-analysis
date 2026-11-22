import React, { useState } from 'react';
import { Globe, ArrowRight, Loader2, Sparkles } from 'lucide-react';

interface UrlInputProps {
  onAnalyze: (url: string) => void;
  isLoading: boolean;
}

const SAMPLE_URLS = [
  { label: 'Dxora CREST', url: 'https://crest.dxora.com' },
  { label: 'Stripe', url: 'https://stripe.com' },
  { label: 'Linear', url: 'https://linear.app' },
  { label: 'Vercel', url: 'https://vercel.com' },
];

export const UrlInput: React.FC<UrlInputProps> = ({ onAnalyze, isLoading }) => {
  const [inputUrl, setInputUrl] = useState('');
  const [validationError, setValidationError] = useState<string | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setValidationError(null);

    let trimmed = inputUrl.trim();
    if (!trimmed) {
      setValidationError('Please enter a website URL.');
      return;
    }

    if (!trimmed.startsWith('http://') && !trimmed.startsWith('https://')) {
      trimmed = `https://${trimmed}`;
    }

    try {
      new URL(trimmed);
      onAnalyze(trimmed);
    } catch {
      setValidationError('Please enter a valid web address (e.g. example.com).');
    }
  };

  const handleSelectSample = (url: string) => {
    setInputUrl(url);
    setValidationError(null);
    onAnalyze(url);
  };

  return (
    <div className="w-full max-w-3xl mx-auto text-center py-6 sm:py-10">
      
      {/* Category Pill */}
      <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full text-xs font-semibold bg-orange-50 text-orange-600 border border-orange-200/60 mb-4 shadow-xs">
        <Sparkles className="w-3.5 h-3.5" />
        <span>Autonomous Website & Market Intelligence</span>
      </div>

      {/* Main Headline */}
      <h1 className="text-3xl sm:text-5xl font-extrabold text-ink-900 tracking-tight leading-[1.15] mb-4">
        Instant SEO audit &amp; <br className="hidden sm:inline" />
        <span className="text-transparent bg-clip-text bg-gradient-to-r from-orange-600 to-orange-500">
          competitive intelligence
        </span>
      </h1>

      <p className="text-sm sm:text-base text-ink-500 max-w-xl mx-auto mb-8 font-normal leading-relaxed">
        Input any public domain to extract deterministic technical SEO facts, benchmark direct competitors, and map high-intent search queries.
      </p>

      {/* Search Bar Container */}
      <form onSubmit={handleSubmit} className="relative max-w-2xl mx-auto mb-4">
        <div className="flex items-center bg-white rounded-2xl border border-ink-200 p-2 shadow-ios hover:border-ink-300 focus-within:border-orange-500 focus-within:ring-4 focus-within:ring-orange-500/10 transition-all">
          <div className="pl-3 pr-2 text-ink-400">
            <Globe className="w-5 h-5" />
          </div>
          
          <input
            type="text"
            value={inputUrl}
            onChange={(e) => {
              setInputUrl(e.target.value);
              if (validationError) setValidationError(null);
            }}
            placeholder="https://crest.dxora.com"
            disabled={isLoading}
            className="w-full py-2.5 px-2 text-sm sm:text-base font-medium text-ink-900 placeholder-ink-400 focus:outline-none bg-transparent"
          />

          <button
            type="submit"
            disabled={isLoading}
            className="flex-shrink-0 flex items-center space-x-2 px-5 py-3 rounded-xl bg-orange-500 text-white text-xs sm:text-sm font-semibold hover:bg-orange-600 active:scale-[0.98] transition-all shadow-sm shadow-orange-500/25 disabled:opacity-60 disabled:cursor-not-allowed cursor-pointer"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Auditing...</span>
              </>
            ) : (
              <>
                <span>Analyze Link</span>
                <ArrowRight className="w-4 h-4 stroke-[2.5]" />
              </>
            )}
          </button>
        </div>

        {validationError && (
          <p className="text-left text-xs font-medium text-rose-500 mt-2 px-3">
            {validationError}
          </p>
        )}
      </form>

      {/* Quick sample pills */}
      <div className="flex flex-wrap items-center justify-center gap-2 pt-2">
        <span className="text-xs text-ink-400 font-medium mr-1">Sample audits:</span>
        {SAMPLE_URLS.map((sample) => (
          <button
            key={sample.url}
            type="button"
            disabled={isLoading}
            onClick={() => handleSelectSample(sample.url)}
            className="text-xs font-medium px-2.5 py-1 rounded-lg bg-white border border-ink-200 text-ink-600 hover:text-orange-600 hover:border-orange-300 hover:bg-orange-50/50 transition-all shadow-2xs disabled:opacity-50"
          >
            {sample.label}
          </button>
        ))}
      </div>
    </div>
  );
};
