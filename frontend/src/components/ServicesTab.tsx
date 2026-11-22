import React from 'react';
import type { TopServiceItem } from '../types';
import { CheckCircle2, HelpCircle, Building, User } from 'lucide-react';

interface ServicesTabProps {
  services: TopServiceItem[];
}

export const ServicesTab: React.FC<ServicesTabProps> = ({ services }) => {
  return (
    <div className="space-y-6">
      
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-base font-bold text-ink-900 tracking-tight">
            Extracted Service Catalog ({services.length})
          </h3>
          <p className="text-xs text-ink-500 font-normal">
            Distinguished by explicit ground-truth copy versus AI contextual inferences
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {services.map((svc, idx) => {
          const isExplicit = svc.extraction_source === 'Explicitly stated on website';

          return (
            <div
              key={idx}
              className="bg-white rounded-2xl border border-ink-200/90 p-5 shadow-subtle hover:shadow-ios transition-all flex flex-col justify-between"
            >
              <div>
                {/* Header & Source pill */}
                <div className="flex items-start justify-between gap-2 mb-3">
                  <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full border inline-flex items-center space-x-1 ${
                    isExplicit
                      ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                      : 'bg-indigo-50 text-indigo-700 border-indigo-200'
                  }`}>
                    {isExplicit ? (
                      <CheckCircle2 className="w-2.5 h-2.5" />
                    ) : (
                      <HelpCircle className="w-2.5 h-2.5" />
                    )}
                    <span>{svc.extraction_source}</span>
                  </span>

                  <span className="text-[11px] font-mono text-ink-400 font-bold">
                    0{idx + 1}
                  </span>
                </div>

                <h4 className="text-base font-bold text-ink-900 tracking-tight mb-2">
                  {svc.service_name}
                </h4>

                <p className="text-xs text-ink-600 leading-relaxed mb-4 font-normal">
                  {svc.description}
                </p>

                {/* Vertical & Customer Metadata */}
                <div className="space-y-2 pt-3 border-t border-ink-100 text-xs mb-4">
                  <div className="flex items-center space-x-2 text-ink-700">
                    <Building className="w-3.5 h-3.5 text-orange-500 flex-shrink-0" />
                    <span className="truncate">
                      <span className="font-semibold text-ink-500">Vertical: </span>
                      {svc.target_industry}
                    </span>
                  </div>

                  <div className="flex items-center space-x-2 text-ink-700">
                    <User className="w-3.5 h-3.5 text-orange-500 flex-shrink-0" />
                    <span className="truncate">
                      <span className="font-semibold text-ink-500">Buyer: </span>
                      {svc.target_customer}
                    </span>
                  </div>
                </div>
              </div>

              {/* Main Benefit Box */}
              <div className="p-3 bg-orange-50/50 rounded-xl border border-orange-200/60 text-xs">
                <span className="text-[10px] font-bold text-orange-800 uppercase tracking-wider block mb-0.5">
                  Core Business Benefit
                </span>
                <span className="text-ink-900 font-medium">
                  {svc.main_benefit}
                </span>
              </div>
            </div>
          );
        })}
      </div>

    </div>
  );
};
