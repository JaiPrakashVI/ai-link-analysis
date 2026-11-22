import React from 'react';
import type { TargetSearchQuery } from '../types';
import { Compass, UserCheck } from 'lucide-react';

interface QueriesTabProps {
  queries: TargetSearchQuery[];
}

const getPlatformBadgeColor = (platform: string) => {
  switch (platform.toLowerCase()) {
    case 'google search':
      return 'bg-blue-50 text-blue-700 border-blue-200';
    case 'linkedin':
      return 'bg-sky-50 text-sky-700 border-sky-200';
    case 'x (twitter)':
    case 'x':
    case 'twitter':
      return 'bg-ink-100 text-ink-800 border-ink-300';
    case 'instagram':
      return 'bg-fuchsia-50 text-fuchsia-700 border-fuchsia-200';
    case 'facebook':
      return 'bg-indigo-50 text-indigo-700 border-indigo-200';
    default:
      return 'bg-orange-50 text-orange-700 border-orange-200';
  }
};

export const QueriesTab: React.FC<QueriesTabProps> = ({ queries }) => {
  return (
    <div className="space-y-6">
      
      {/* Notice on Real Intent */}
      <div className="bg-white rounded-2xl border border-ink-200/90 p-4 shadow-subtle flex items-start space-x-3 text-xs text-ink-600">
        <Compass className="w-4 h-4 text-orange-500 flex-shrink-0 mt-0.5" />
        <div>
          <span className="font-semibold text-ink-900">Truth-in-Intent Search Architecture: </span>
          These high-intent discovery phrases map buyer motivation across search engines and social channels. We strictly never invent synthetic search volume numbers or artificial CPC estimations.
        </div>
      </div>

      {/* Query Cards */}
      <div className="grid grid-cols-1 gap-4">
        {queries.map((q, idx) => (
          <div
            key={idx}
            className="bg-white rounded-2xl border border-ink-200/90 p-5 shadow-subtle hover:border-orange-200 hover:shadow-ios transition-all"
          >
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3">
              <div className="flex items-center space-x-2">
                <div className="w-6 h-6 rounded-lg bg-orange-500/10 text-orange-600 font-mono font-bold text-xs flex items-center justify-center">
                  #{idx + 1}
                </div>
                <h4 className="text-base font-bold text-ink-900 tracking-tight">
                  &ldquo;{q.query}&rdquo;
                </h4>
              </div>

              {/* Platforms */}
              <div className="flex flex-wrap gap-1.5">
                {q.platforms.map((p, pIdx) => (
                  <span
                    key={pIdx}
                    className={`text-[11px] font-semibold px-2.5 py-0.5 rounded-full border ${getPlatformBadgeColor(
                      p
                    )}`}
                  >
                    {p}
                  </span>
                ))}
                <span className="text-[11px] font-mono px-2 py-0.5 rounded-full bg-ink-50 text-ink-600 border border-ink-200 font-medium">
                  {q.intent}
                </span>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-3 border-t border-ink-100 text-xs">
              <div>
                <span className="font-semibold text-ink-500 uppercase tracking-wider text-[10px] block mb-1">
                  Strategic Relevance
                </span>
                <p className="text-ink-700 leading-relaxed font-normal">
                  {q.business_relevance}
                </p>
              </div>

              <div>
                <span className="font-semibold text-ink-500 uppercase tracking-wider text-[10px] block mb-1 flex items-center space-x-1">
                  <UserCheck className="w-3 h-3 text-orange-500" />
                  <span>Target Persona</span>
                </span>
                <p className="text-ink-800 font-medium leading-relaxed">
                  {q.target_audience}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>

    </div>
  );
};
