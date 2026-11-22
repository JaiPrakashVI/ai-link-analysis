import React from 'react';
import type { TargetAudience } from '../types';
import { Users, Globe, Briefcase, Heart, CheckCircle2, Layers } from 'lucide-react';

interface AudienceTabProps {
  audience: TargetAudience;
}

export const AudienceTab: React.FC<AudienceTabProps> = ({ audience }) => {
  return (
    <div className="space-y-8">
      
      {/* Primary vs Secondary Hero Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* Primary ICP */}
        <div className="bg-white rounded-2xl border border-ink-200/90 p-6 shadow-subtle">
          <div className="flex items-center space-x-2 text-xs font-bold text-orange-600 uppercase tracking-wider mb-2">
            <Users className="w-4 h-4" />
            <span>Primary Buyer Profile (ICP)</span>
          </div>
          <p className="text-base font-bold text-ink-900 tracking-tight leading-snug mb-3">
            {audience.primary_audience}
          </p>
          <div className="text-xs text-ink-500 font-medium">
            Core economic decision maker driving buying authorization
          </div>
        </div>

        {/* Secondary Influencers */}
        <div className="bg-white rounded-2xl border border-ink-200/90 p-6 shadow-subtle">
          <div className="flex items-center space-x-2 text-xs font-bold text-ink-500 uppercase tracking-wider mb-2">
            <Users className="w-4 h-4" />
            <span>Secondary / User Demographics</span>
          </div>
          <p className="text-base font-bold text-ink-900 tracking-tight leading-snug mb-3">
            {audience.secondary_audience}
          </p>
          <div className="text-xs text-ink-500 font-medium">
            Key operational users, practitioners, and internal champions
          </div>
        </div>

      </div>

      {/* Target Industries & Firmographics */}
      <div className="bg-white rounded-2xl border border-ink-200/90 p-6 shadow-subtle space-y-6">
        <h3 className="text-base font-bold text-ink-900 flex items-center space-x-2">
          <Briefcase className="w-4 h-4 text-orange-500" />
          <span>Firmographic Demographics &amp; Geographic Footprint</span>
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 text-xs">
          
          <div>
            <span className="font-bold text-ink-400 uppercase tracking-wider block mb-2 text-[10px]">
              Target Verticals
            </span>
            <div className="flex flex-wrap gap-1.5">
              {audience.industries.map((ind, idx) => (
                <span
                  key={idx}
                  className="px-2.5 py-1 rounded-lg bg-ink-50 text-ink-800 border border-ink-200 font-medium"
                >
                  {ind}
                </span>
              ))}
            </div>
          </div>

          <div>
            <span className="font-bold text-ink-400 uppercase tracking-wider block mb-2 text-[10px]">
              Business Scale Categories
            </span>
            <div className="flex flex-wrap gap-1.5">
              {audience.business_types.map((bt, idx) => (
                <span
                  key={idx}
                  className="px-2.5 py-1 rounded-lg bg-ink-50 text-ink-800 border border-ink-200 font-medium"
                >
                  {bt}
                </span>
              ))}
            </div>
          </div>

          <div>
            <span className="font-bold text-ink-400 uppercase tracking-wider block mb-2 text-[10px]">
              Key Stakeholder Roles
            </span>
            <div className="flex flex-wrap gap-1.5">
              {audience.customer_profiles.map((cp, idx) => (
                <span
                  key={idx}
                  className="px-2.5 py-1 rounded-lg bg-orange-50 text-orange-800 border border-orange-200 font-medium"
                >
                  {cp}
                </span>
              ))}
            </div>
          </div>

        </div>

        {/* Geographic Focus */}
        <div className="pt-4 border-t border-ink-100 flex items-center space-x-2 text-xs">
          <Globe className="w-4 h-4 text-orange-500 flex-shrink-0" />
          <span className="font-semibold text-ink-900">Geographic Focus: </span>
          <span className="text-ink-600">{audience.geographical_focus}</span>
        </div>
      </div>

      {/* Needs vs Interests */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* Customer Needs */}
        <div className="bg-white rounded-2xl border border-ink-200/90 p-6 shadow-subtle">
          <h4 className="text-sm font-bold text-ink-900 mb-4 flex items-center space-x-2">
            <CheckCircle2 className="w-4 h-4 text-orange-500" />
            <span>Functional Buyer Needs &amp; Pain Points</span>
          </h4>
          <ul className="space-y-2">
            {audience.customer_needs.map((need, idx) => (
              <li
                key={idx}
                className="p-3 bg-ink-50 rounded-xl border border-ink-200 text-xs font-medium text-ink-800 flex items-start space-x-2"
              >
                <div className="w-1.5 h-1.5 rounded-full bg-orange-500 mt-1.5 flex-shrink-0" />
                <span>{need}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Customer Interests */}
        <div className="bg-white rounded-2xl border border-ink-200/90 p-6 shadow-subtle">
          <h4 className="text-sm font-bold text-ink-900 mb-4 flex items-center space-x-2">
            <Heart className="w-4 h-4 text-orange-500" />
            <span>Strategic Priorities &amp; Category Interests</span>
          </h4>
          <ul className="space-y-2">
            {audience.customer_interests.map((interest, idx) => (
              <li
                key={idx}
                className="p-3 bg-ink-50 rounded-xl border border-ink-200 text-xs font-medium text-ink-800 flex items-start space-x-2"
              >
                <div className="w-1.5 h-1.5 rounded-full bg-orange-500 mt-1.5 flex-shrink-0" />
                <span>{interest}</span>
              </li>
            ))}
          </ul>
        </div>

      </div>

      {/* Recommended Marketing Segments Table */}
      <div className="bg-white rounded-2xl border border-ink-200/90 overflow-hidden shadow-subtle">
        <div className="p-5 border-b border-ink-100 bg-ink-50/50 flex items-center justify-between">
          <h4 className="text-sm font-bold text-ink-900 flex items-center space-x-2">
            <Layers className="w-4 h-4 text-orange-500" />
            <span>Actionable Customer Marketing Segments ({audience.recommended_marketing_segments.length})</span>
          </h4>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-ink-50/80 text-ink-500 font-semibold border-b border-ink-200">
              <tr>
                <th className="py-3 px-4 font-mono text-[10px] uppercase">Segment Name</th>
                <th className="py-3 px-4 font-mono text-[10px] uppercase">Business Scale</th>
                <th className="py-3 px-4 font-mono text-[10px] uppercase">Core Operational Requirement</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-ink-100 font-medium">
              {audience.recommended_marketing_segments.map((seg, idx) => (
                <tr key={idx} className="hover:bg-ink-50/50 transition-colors">
                  <td className="py-3 px-4 font-bold text-ink-900 whitespace-nowrap">
                    {seg.segment_name}
                  </td>
                  <td className="py-3 px-4 text-ink-600">
                    <span className="px-2 py-0.5 rounded-md bg-ink-100 text-ink-700 text-[11px] font-medium border border-ink-200">
                      {seg.business_type}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-ink-700 font-normal">
                    {seg.requirement}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
};
