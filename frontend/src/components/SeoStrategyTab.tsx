import React from 'react';
import type { SeoImprovements } from '../types';
import { Key, Layers } from 'lucide-react';

interface SeoStrategyTabProps {
  seo: SeoImprovements;
  currentTitle?: string | null;
}

const getContentTypeBadge = (type: string) => {
  switch (type) {
    case 'Service Landing Page':
      return 'bg-blue-50 text-blue-700 border-blue-200';
    case 'Industry Page':
      return 'bg-purple-50 text-purple-700 border-purple-200';
    case 'FAQ':
      return 'bg-amber-50 text-amber-700 border-amber-200';
    case 'Blog Topic':
      return 'bg-emerald-50 text-emerald-700 border-emerald-200';
    case 'Location Page':
      return 'bg-rose-50 text-rose-700 border-rose-200';
    default:
      return 'bg-orange-50 text-orange-700 border-orange-200';
  }
};

export const SeoStrategyTab: React.FC<SeoStrategyTabProps> = ({ seo, currentTitle }) => {
  return (
    <div className="space-y-8">
      
      {/* Title & Meta Recommendation Card */}
      <div className="bg-white rounded-2xl border border-ink-200/90 p-6 shadow-subtle space-y-5">
        <div>
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-orange-600 uppercase tracking-wider block">
              Optimized Document Title
            </span>
            {currentTitle && (
              <span className="text-[11px] font-mono text-ink-400">
                Current: {currentTitle.length} chars → Recommended: {seo.recommended_title.length} chars
              </span>
            )}
          </div>

          {currentTitle && (
            <div className="p-3 bg-ink-50 rounded-xl border border-ink-200 mb-2 text-xs text-ink-500">
              <span className="font-semibold text-ink-700">Current Title on Page: </span>
              {currentTitle}
            </div>
          )}

          <div className="p-4 bg-orange-50/50 rounded-2xl border border-orange-200/80 mb-3">
            <div className="text-base font-bold text-ink-900 tracking-tight mb-1">
              {seo.recommended_title}
            </div>
            <span className="text-[11px] font-mono text-orange-700 font-semibold">
              Recommended Title ({seo.recommended_title.length} characters)
            </span>
          </div>

          <div className="text-xs text-ink-600 bg-ink-50 p-3 rounded-xl border border-ink-200 leading-relaxed">
            <span className="font-semibold text-ink-900">Rationale: </span>
            {seo.title_rationale}
          </div>
        </div>

        {/* Meta Description */}
        <div className="pt-4 border-t border-ink-100">
          <span className="text-xs font-bold text-ink-500 uppercase tracking-wider block mb-2">
            Recommended Meta Description
          </span>
          <p className="text-sm text-ink-800 bg-ink-50/70 p-3.5 rounded-xl border border-ink-200 leading-relaxed font-normal">
            {seo.meta_description}
          </p>
          <span className="text-[11px] font-mono text-ink-400 mt-1 block">
            Length: {seo.meta_description.length} characters
          </span>
        </div>
      </div>

      {/* Semantic Keyword Clusters */}
      <div className="bg-white rounded-2xl border border-ink-200/90 p-6 shadow-subtle space-y-6">
        <h3 className="text-base font-bold text-ink-900 flex items-center space-x-2">
          <Key className="w-4 h-4 text-orange-500" />
          <span>Semantic Keyword Architecture</span>
        </h3>

        {/* Primary Keyword */}
        <div>
          <span className="text-xs font-bold text-ink-400 uppercase tracking-wider block mb-2">
            Primary Target Keyword
          </span>
          <div className="inline-flex items-center px-4 py-2 rounded-xl bg-orange-50 text-orange-700 border border-orange-200 text-sm font-bold tracking-tight shadow-2xs">
            {seo.primary_keyword}
          </div>
        </div>

        {/* Secondary Keywords */}
        <div>
          <span className="text-xs font-bold text-ink-400 uppercase tracking-wider block mb-2">
            Secondary &amp; Thematic Keywords
          </span>
          <div className="flex flex-wrap gap-2">
            {seo.secondary_keywords.map((kw, idx) => (
              <span
                key={idx}
                className="px-3 py-1.5 rounded-xl bg-ink-50 text-xs font-medium text-ink-800 border border-ink-200"
              >
                {kw}
              </span>
            ))}
          </div>
        </div>

        {/* Long-tail Keywords */}
        <div>
          <span className="text-xs font-bold text-ink-400 uppercase tracking-wider block mb-2">
            High-Conversion Long-Tail Queries
          </span>
          <div className="flex flex-wrap gap-2">
            {seo.long_tail_keywords.map((kw, idx) => (
              <span
                key={idx}
                className="px-3 py-1.5 rounded-xl bg-ink-50 text-xs font-medium text-ink-800 border border-ink-200 font-mono"
              >
                {kw}
              </span>
            ))}
          </div>
        </div>

        {/* Business Keywords */}
        <div>
          <span className="text-xs font-bold text-ink-400 uppercase tracking-wider block mb-2">
            Commercial Brand Terms
          </span>
          <div className="flex flex-wrap gap-2">
            {seo.business_keywords.map((kw, idx) => (
              <span
                key={idx}
                className="px-3 py-1.5 rounded-xl bg-ink-100 text-xs font-semibold text-ink-700 border border-ink-200"
              >
                {kw}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Supporting Content Assets */}
      <div>
        <h3 className="text-base font-bold text-ink-900 mb-4 flex items-center space-x-2">
          <Layers className="w-4 h-4 text-orange-500" />
          <span>Recommended Content Expansion Blueprints ({seo.supporting_content.length})</span>
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {seo.supporting_content.map((content, idx) => (
            <div
              key={idx}
              className="bg-white rounded-2xl border border-ink-200/90 p-5 shadow-subtle hover:shadow-ios transition-all"
            >
              <div className="flex items-center justify-between mb-2">
                <span
                  className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full border ${getContentTypeBadge(
                    content.type
                  )}`}
                >
                  {content.type}
                </span>
                <span className="text-[11px] font-mono text-ink-400 font-medium">Blueprint #{idx + 1}</span>
              </div>

              <h4 className="text-sm font-bold text-ink-900 mb-2 leading-snug">
                {content.title}
              </h4>
              <p className="text-xs text-ink-600 leading-relaxed font-normal">
                {content.description}
              </p>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
};
