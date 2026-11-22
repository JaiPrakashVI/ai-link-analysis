import React from 'react';
import type { CompetitorAnalysis } from '../types';
import { ShieldCheck, Target, CheckCircle2, XCircle, Info, Sparkles } from 'lucide-react';

interface CompetitorsTabProps {
  data: CompetitorAnalysis;
}

export const CompetitorsTab: React.FC<CompetitorsTabProps> = ({ data }) => {
  return (
    <div className="space-y-8">
      
      {/* Brand Overview Banner */}
      <div className="bg-white rounded-2xl border border-ink-200/90 p-6 shadow-subtle">
        <div className="flex items-center space-x-2 text-xs font-semibold text-orange-600 uppercase tracking-wider mb-2">
          <Target className="w-4 h-4" />
          <span>Strategic Market Posture</span>
        </div>
        <p className="text-sm sm:text-base text-ink-900 font-medium leading-relaxed mb-4">
          {data.brand_overview}
        </p>

        {/* Main Products Pills */}
        <div className="pt-2">
          <span className="text-xs text-ink-500 font-semibold block mb-2">Primary Products &amp; Solutions:</span>
          <div className="flex flex-wrap gap-2">
            {data.main_products_and_services.map((prod, idx) => (
              <span
                key={idx}
                className="px-3 py-1 rounded-xl bg-ink-50 text-xs font-medium text-ink-800 border border-ink-200"
              >
                {prod}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Competitors Grid */}
      <div>
        <h3 className="text-base font-bold text-ink-900 mb-4 flex items-center justify-between">
          <span>Identified Market Competitors ({data.competitors.length})</span>
          <span className="text-xs font-normal text-ink-400">Benchmarked against industry footprints</span>
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {data.competitors.map((comp, idx) => (
            <div
              key={idx}
              className="bg-white rounded-2xl border border-ink-200/90 p-5 shadow-subtle hover:shadow-ios transition-all flex flex-col justify-between"
            >
              <div>
                <div className="flex items-start justify-between mb-3">
                  <h4 className="text-lg font-extrabold text-ink-900 tracking-tight">
                    {comp.name}
                  </h4>
                  <span className="text-[11px] font-mono px-2 py-0.5 rounded-full bg-ink-100 text-ink-600 font-semibold">
                    Peer #{idx + 1}
                  </span>
                </div>

                <div className="space-y-2 mb-4 text-xs">
                  <div>
                    <span className="font-semibold text-ink-500 block">Core Offering:</span>
                    <span className="text-ink-800 font-medium">{comp.main_service}</span>
                  </div>
                  <div>
                    <span className="font-semibold text-ink-500 block">Target Segment:</span>
                    <span className="text-ink-700">{comp.target_market}</span>
                  </div>
                </div>

                {/* Strengths */}
                <div className="mb-4">
                  <span className="text-[11px] font-bold text-emerald-700 uppercase tracking-wider block mb-1.5">
                    Competitive Strengths
                  </span>
                  <ul className="space-y-1.5">
                    {comp.strengths.map((str, sIdx) => (
                      <li key={sIdx} className="text-xs text-ink-700 flex items-start space-x-1.5">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 flex-shrink-0 mt-0.5" />
                        <span>{str}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Weaknesses / Gaps */}
                <div className="mb-4">
                  <span className="text-[11px] font-bold text-orange-700 uppercase tracking-wider block mb-1.5">
                    Observed Vulnerabilities &amp; Gaps
                  </span>
                  <ul className="space-y-1.5">
                    {comp.weaknesses_or_gaps.map((weak, wIdx) => (
                      <li key={wIdx} className="text-xs text-ink-700 flex items-start space-x-1.5">
                        <XCircle className="w-3.5 h-3.5 text-orange-500 flex-shrink-0 mt-0.5" />
                        <span>{weak}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Source Note Footer */}
              <div className="pt-3 border-t border-ink-100 text-[10px] text-ink-400 font-mono flex items-center space-x-1">
                <Info className="w-3 h-3 text-ink-400 flex-shrink-0" />
                <span className="truncate" title={comp.source_note}>{comp.source_note}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Brand Strengths & Opportunities */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* Your Strengths */}
        <div className="bg-white rounded-2xl border border-ink-200/90 p-6 shadow-subtle">
          <h4 className="text-sm font-bold text-ink-900 mb-4 flex items-center space-x-2">
            <ShieldCheck className="w-4 h-4 text-emerald-600" />
            <span>Your Distinctive Brand Strengths</span>
          </h4>
          <div className="space-y-2.5">
            {data.your_brand_strengths.map((str, idx) => (
              <div
                key={idx}
                className="p-3 bg-emerald-50/50 rounded-xl border border-emerald-100 text-xs font-medium text-emerald-900 flex items-start space-x-2"
              >
                <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 mt-1.5 flex-shrink-0" />
                <span>{str}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Opportunities */}
        <div className="bg-white rounded-2xl border border-ink-200/90 p-6 shadow-subtle">
          <h4 className="text-sm font-bold text-ink-900 mb-4 flex items-center space-x-2">
            <Sparkles className="w-4 h-4 text-orange-500" />
            <span>High-Impact Market Opportunities</span>
          </h4>
          <div className="space-y-2.5">
            {data.opportunities.map((opp, idx) => (
              <div
                key={idx}
                className="p-3 bg-orange-50/40 rounded-xl border border-orange-100 text-xs font-medium text-orange-950 flex items-start space-x-2"
              >
                <div className="w-1.5 h-1.5 rounded-full bg-orange-500 mt-1.5 flex-shrink-0" />
                <span>{opp}</span>
              </div>
            ))}
          </div>
        </div>

      </div>

    </div>
  );
};
