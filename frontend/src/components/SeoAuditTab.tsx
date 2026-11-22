import React from 'react';
import type { TechnicalSeoAudit } from '../types';
import { AlertCircle, CheckCircle2, Image, FileText, Share2, Code, Compass } from 'lucide-react';

interface SeoAuditTabProps {
  audit: TechnicalSeoAudit;
}

export const SeoAuditTab: React.FC<SeoAuditTabProps> = ({ audit }) => {
  const isTitleOptimal = audit.title_char_count >= 50 && audit.title_char_count <= 60;
  const isDescOptimal = audit.meta_description_char_count >= 140 && audit.meta_description_char_count <= 160;

  return (
    <div className="space-y-6">
      
      {/* Overview Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        {/* Card 1: Title length */}
        <div className="bg-white rounded-2xl border border-ink-200/90 p-5 shadow-subtle">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-ink-500 uppercase tracking-wider">Document Title</span>
            <span className={`text-[11px] font-semibold px-2 py-0.5 rounded-full ${
              isTitleOptimal ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-orange-50 text-orange-700 border border-orange-200'
            }`}>
              {audit.title_char_count} chars
            </span>
          </div>
          <p className="text-sm font-semibold text-ink-900 line-clamp-2 mb-2">
            {audit.title || 'No title tag found'}
          </p>
          <div className="w-full bg-ink-100 h-1.5 rounded-full overflow-hidden">
            <div
              className={`h-full rounded-full transition-all ${
                isTitleOptimal ? 'bg-emerald-500' : 'bg-orange-500'
              }`}
              style={{ width: `${Math.min(100, (audit.title_char_count / 60) * 100)}%` }}
            />
          </div>
          <span className="text-[10px] text-ink-400 mt-1 block">Optimal: 50–60 characters</span>
        </div>

        {/* Card 2: Meta description length */}
        <div className="bg-white rounded-2xl border border-ink-200/90 p-5 shadow-subtle">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-ink-500 uppercase tracking-wider">Meta Description</span>
            <span className={`text-[11px] font-semibold px-2 py-0.5 rounded-full ${
              isDescOptimal ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-orange-50 text-orange-700 border border-orange-200'
            }`}>
              {audit.meta_description_char_count} chars
            </span>
          </div>
          <p className="text-xs text-ink-700 line-clamp-2 mb-2">
            {audit.meta_description || 'No meta description found'}
          </p>
          <div className="w-full bg-ink-100 h-1.5 rounded-full overflow-hidden">
            <div
              className={`h-full rounded-full transition-all ${
                isDescOptimal ? 'bg-emerald-500' : 'bg-orange-500'
              }`}
              style={{ width: `${Math.min(100, (audit.meta_description_char_count / 160) * 100)}%` }}
            />
          </div>
          <span className="text-[10px] text-ink-400 mt-1 block">Optimal: 140–160 characters</span>
        </div>

        {/* Card 3: Images & Alt tags */}
        <div className="bg-white rounded-2xl border border-ink-200/90 p-5 shadow-subtle">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-ink-500 uppercase tracking-wider">Image Alt Attributes</span>
            <Image className="w-4 h-4 text-ink-400" />
          </div>
          <div className="flex items-baseline space-x-2 mb-1">
            <span className="text-2xl font-extrabold text-ink-900 font-mono">
              {audit.images_with_alt} / {audit.total_images}
            </span>
            <span className="text-xs text-ink-500 font-medium">with alt text</span>
          </div>
          {audit.images_missing_alt > 0 ? (
            <div className="flex items-center space-x-1 text-xs text-amber-700 font-medium mt-1">
              <AlertCircle className="w-3.5 h-3.5 flex-shrink-0" />
              <span>{audit.images_missing_alt} images missing descriptive alt tags</span>
            </div>
          ) : (
            <div className="flex items-center space-x-1 text-xs text-emerald-700 font-medium mt-1">
              <CheckCircle2 className="w-3.5 h-3.5" />
              <span>All images contain alt text</span>
            </div>
          )}
        </div>

        {/* Card 4: Headings distribution */}
        <div className="bg-white rounded-2xl border border-ink-200/90 p-5 shadow-subtle">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-ink-500 uppercase tracking-wider">Heading Architecture</span>
            <FileText className="w-4 h-4 text-ink-400" />
          </div>
          <div className="grid grid-cols-3 gap-2 text-center pt-1">
            <div className="bg-ink-50 py-1.5 rounded-lg border border-ink-100">
              <div className="text-lg font-bold font-mono text-ink-900">{audit.h1_count}</div>
              <div className="text-[10px] font-semibold text-ink-500 uppercase">H1 Tags</div>
            </div>
            <div className="bg-ink-50 py-1.5 rounded-lg border border-ink-100">
              <div className="text-lg font-bold font-mono text-ink-900">{audit.h2_count}</div>
              <div className="text-[10px] font-semibold text-ink-500 uppercase">H2 Tags</div>
            </div>
            <div className="bg-ink-50 py-1.5 rounded-lg border border-ink-100">
              <div className="text-lg font-bold font-mono text-ink-900">{audit.h3_count}</div>
              <div className="text-[10px] font-semibold text-ink-500 uppercase">H3 Tags</div>
            </div>
          </div>
        </div>

      </div>

      {/* Row 2: Deep Technical Details */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Left: H1 Tags & Canonical Info */}
        <div className="bg-white rounded-2xl border border-ink-200/90 p-6 shadow-subtle">
          <h3 className="text-sm font-bold text-ink-900 mb-4 flex items-center space-x-2">
            <FileText className="w-4 h-4 text-orange-500" />
            <span>Extracted H1 Headings ({audit.h1_count})</span>
          </h3>

          {audit.h1_tags.length > 0 ? (
            <div className="space-y-2 mb-6">
              {audit.h1_tags.map((tag, idx) => (
                <div
                  key={idx}
                  className="p-3 bg-ink-50 rounded-xl border border-ink-200 text-xs font-medium text-ink-900"
                >
                  <span className="text-orange-600 font-mono font-bold mr-2">H1 #{idx + 1}:</span>
                  {tag}
                </div>
              ))}
            </div>
          ) : (
            <p className="text-xs text-rose-500 mb-6 font-medium">No &lt;h1&gt; tags detected on the page.</p>
          )}

          <h3 className="text-sm font-bold text-ink-900 mb-3 flex items-center space-x-2">
            <Compass className="w-4 h-4 text-orange-500" />
            <span>Canonical &amp; Internal Navigation</span>
          </h3>
          <div className="text-xs font-mono text-ink-600 bg-ink-50 p-3 rounded-xl border border-ink-200 mb-4 truncate">
            <span className="font-semibold text-ink-900">Canonical: </span>
            {audit.canonical_url || 'None declared'}
          </div>

          <div className="text-xs text-ink-500 mb-2 font-medium">Detected Navigation Link Labels:</div>
          <div className="flex flex-wrap gap-1.5">
            {audit.internal_nav_links.length > 0 ? (
              audit.internal_nav_links.map((link, idx) => (
                <span
                  key={idx}
                  className="px-2.5 py-1 bg-ink-100/70 border border-ink-200 rounded-lg text-xs font-medium text-ink-700"
                >
                  {link}
                </span>
              ))
            ) : (
              <span className="text-xs text-ink-400">No navigation links detected</span>
            )}
          </div>
        </div>

        {/* Right: OpenGraph & Schema.org */}
        <div className="bg-white rounded-2xl border border-ink-200/90 p-6 shadow-subtle space-y-6">
          
          {/* Schema.org */}
          <div>
            <h3 className="text-sm font-bold text-ink-900 mb-3 flex items-center space-x-2">
              <Code className="w-4 h-4 text-orange-500" />
              <span>Structured Schema Markup ({audit.schema_types_detected.length})</span>
            </h3>
            {audit.has_schema_markup ? (
              <div className="flex flex-wrap gap-2">
                {audit.schema_types_detected.map((st, idx) => (
                  <span
                    key={idx}
                    className="px-3 py-1 rounded-full text-xs font-mono font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200"
                  >
                    @{st}
                  </span>
                ))}
              </div>
            ) : (
              <p className="text-xs text-ink-500 font-medium">No JSON-LD structured schema detected.</p>
            )}
          </div>

          {/* OpenGraph Preview */}
          <div>
            <h3 className="text-sm font-bold text-ink-900 mb-3 flex items-center space-x-2">
              <Share2 className="w-4 h-4 text-orange-500" />
              <span>OpenGraph Social Metadata</span>
            </h3>
            
            {audit.has_og_tags ? (
              <div className="border border-ink-200 rounded-2xl overflow-hidden bg-white shadow-2xs">
                {audit.og_tags['og:image'] && (
                  <img
                    src={audit.og_tags['og:image']}
                    alt="OG Social Card Preview"
                    className="w-full h-36 object-cover bg-ink-100"
                    onError={(e) => {
                      (e.target as HTMLElement).style.display = 'none';
                    }}
                  />
                )}
                <div className="p-4 space-y-1">
                  <div className="text-[11px] font-mono text-ink-400 uppercase tracking-wider">
                    {audit.og_tags['og:site_name'] || 'Social Preview'}
                  </div>
                  <div className="text-sm font-bold text-ink-900 line-clamp-1">
                    {audit.og_tags['og:title'] || audit.title}
                  </div>
                  <div className="text-xs text-ink-500 line-clamp-2">
                    {audit.og_tags['og:description'] || audit.meta_description}
                  </div>
                </div>
              </div>
            ) : (
              <p className="text-xs text-ink-500">No OpenGraph social tags detected on target page.</p>
            )}
          </div>

        </div>

      </div>

    </div>
  );
};
