import React, { useState } from 'react';
import type { AnalysisMetadata, BrandInfo } from '../types';
import { Cpu, Zap, Clock, Coins, Layers, Check, Copy, ExternalLink, RefreshCw } from 'lucide-react';

interface TelemetryBarProps {
  metadata: AnalysisMetadata;
  brand: BrandInfo;
  website: string;
  onRefresh: () => void;
  fullData: any;
}

export const TelemetryBar: React.FC<TelemetryBarProps> = ({
  metadata,
  brand,
  website,
  onRefresh,
  fullData,
}) => {
  const [copied, setCopied] = useState(false);

  const handleCopyJson = () => {
    navigator.clipboard.writeText(JSON.stringify(fullData, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-white rounded-3xl border border-ink-200/90 shadow-ios p-5 sm:p-6 mb-8 transition-all">
      
      {/* Brand title & actions */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-5 border-b border-ink-100">
        <div>
          <div className="flex items-center space-x-2.5 mb-1.5 flex-wrap">
            <h2 className="text-xl sm:text-2xl font-extrabold text-ink-900 tracking-tight">
              {brand.name}
            </h2>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-orange-50 text-orange-600 border border-orange-200/80">
              {brand.category}
            </span>
          </div>

          <a
            href={website}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center space-x-1.5 text-xs font-mono text-ink-500 hover:text-orange-600 transition-colors"
          >
            <span>{website}</span>
            <ExternalLink className="w-3 h-3" />
          </a>
        </div>

        {/* Action buttons */}
        <div className="flex items-center space-x-2 flex-shrink-0">
          <button
            onClick={onRefresh}
            className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-xl border border-ink-200 text-xs font-medium text-ink-700 bg-white hover:bg-ink-50 transition-colors shadow-2xs"
            title="Re-run analysis to test cache hit"
          >
            <RefreshCw className="w-3.5 h-3.5 text-ink-500" />
            <span>Re-Audit</span>
          </button>

          <button
            onClick={handleCopyJson}
            className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-xl border border-ink-200 text-xs font-medium text-ink-700 bg-white hover:bg-ink-50 transition-colors shadow-2xs"
          >
            {copied ? (
              <>
                <Check className="w-3.5 h-3.5 text-emerald-600" />
                <span className="text-emerald-600">Copied</span>
              </>
            ) : (
              <>
                <Copy className="w-3.5 h-3.5 text-ink-500" />
                <span>Copy JSON</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Executive Summary */}
      <p className="text-sm text-ink-600 py-4 leading-relaxed font-normal">
        {brand.summary}
      </p>

      {/* Telemetry Metrics Row */}
      <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 pt-4 border-t border-ink-100">
        
        {/* Metric 1: Model */}
        <div className="p-3 rounded-2xl bg-ink-50/70 border border-ink-100">
          <div className="flex items-center space-x-1.5 text-[11px] font-semibold text-ink-500 mb-1">
            <Cpu className="w-3.5 h-3.5 text-orange-500" />
            <span>MODEL</span>
          </div>
          <div className="text-xs font-bold font-mono text-ink-900 truncate">
            {metadata.model_used}
          </div>
        </div>

        {/* Metric 2: Cache status */}
        <div className="p-3 rounded-2xl bg-ink-50/70 border border-ink-100">
          <div className="flex items-center space-x-1.5 text-[11px] font-semibold text-ink-500 mb-1">
            <Zap className="w-3.5 h-3.5 text-orange-500" />
            <span>CACHE TIER</span>
          </div>
          <div className="flex items-center space-x-1">
            <span
              className={`inline-block w-2 h-2 rounded-full ${
                metadata.cached ? 'bg-emerald-500' : 'bg-blue-500'
              }`}
            />
            <span className="text-xs font-bold font-mono text-ink-900">
              {metadata.cached ? 'TTL Hit (<5ms)' : 'Live Synthesis'}
            </span>
          </div>
        </div>

        {/* Metric 3: Latency */}
        <div className="p-3 rounded-2xl bg-ink-50/70 border border-ink-100">
          <div className="flex items-center space-x-1.5 text-[11px] font-semibold text-ink-500 mb-1">
            <Clock className="w-3.5 h-3.5 text-orange-500" />
            <span>LATENCY</span>
          </div>
          <div className="text-xs font-bold font-mono text-ink-900">
            {metadata.processing_time_ms.toLocaleString()} ms
          </div>
        </div>

        {/* Metric 4: Tokens */}
        <div className="p-3 rounded-2xl bg-ink-50/70 border border-ink-100">
          <div className="flex items-center space-x-1.5 text-[11px] font-semibold text-ink-500 mb-1">
            <Layers className="w-3.5 h-3.5 text-orange-500" />
            <span>TOKENS</span>
          </div>
          <div className="text-xs font-bold font-mono text-ink-900">
            {metadata.input_tokens.toLocaleString()} / {metadata.output_tokens.toLocaleString()}
          </div>
        </div>

        {/* Metric 5: Cost */}
        <div className="p-3 rounded-2xl bg-ink-50/70 border border-ink-100 col-span-2 sm:col-span-1">
          <div className="flex items-center space-x-1.5 text-[11px] font-semibold text-ink-500 mb-1">
            <Coins className="w-3.5 h-3.5 text-orange-500" />
            <span>EST. COST</span>
          </div>
          <div className="text-xs font-bold font-mono text-emerald-600">
            ${metadata.estimated_cost_usd.toFixed(6)}
          </div>
        </div>

      </div>
    </div>
  );
};
