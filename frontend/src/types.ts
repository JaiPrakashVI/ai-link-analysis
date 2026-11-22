export interface AnalysisMetadata {
  model_used: string;
  cached: boolean;
  processing_time_ms: number;
  input_tokens: number;
  output_tokens: number;
  estimated_cost_usd: number;
}

export interface BrandInfo {
  name: string;
  category: string;
  summary: string;
}

export interface TechnicalSeoAudit {
  title: string | null;
  title_char_count: number;
  meta_description: string | null;
  meta_description_char_count: number;
  h1_count: number;
  h1_tags: string[];
  h2_count: number;
  h3_count: number;
  total_images: number;
  images_missing_alt: number;
  images_with_alt: number;
  internal_nav_links: string[];
  canonical_url: string | null;
  has_og_tags: boolean;
  og_tags: Record<string, string>;
  has_schema_markup: boolean;
  schema_types_detected: string[];
  content_char_count: number;
  status_code: number;
}

export interface CompetitorItem {
  name: string;
  main_service: string;
  target_market: string;
  strengths: string[];
  weaknesses_or_gaps: string[];
  source_note: string;
}

export interface CompetitorAnalysis {
  brand_overview: string;
  main_products_and_services: string[];
  competitors: CompetitorItem[];
  your_brand_strengths: string[];
  opportunities: string[];
}

export interface TargetSearchQuery {
  query: string;
  platforms: string[];
  intent: string;
  business_relevance: string;
  target_audience: string;
}

export interface SupportingContentItem {
  type: 'Service Landing Page' | 'Industry Page' | 'FAQ' | 'Blog Topic' | 'Location Page';
  title: string;
  description: string;
}

export interface SeoImprovements {
  primary_keyword: string;
  secondary_keywords: string[];
  long_tail_keywords: string[];
  business_keywords: string[];
  recommended_title: string;
  title_rationale: string;
  meta_description: string;
  supporting_content: SupportingContentItem[];
}

export interface TopServiceItem {
  service_name: string;
  description: string;
  target_industry: string;
  target_customer: string;
  main_benefit: string;
  extraction_source: 'Explicitly stated on website' | 'Inferred from website context';
}

export interface MarketingSegmentItem {
  segment_name: string;
  business_type: string;
  requirement: string;
}

export interface TargetAudience {
  primary_audience: string;
  secondary_audience: string;
  industries: string[];
  business_types: string[];
  customer_profiles: string[];
  geographical_focus: string;
  customer_needs: string[];
  customer_interests: string[];
  recommended_marketing_segments: MarketingSegmentItem[];
}

export interface AnalysisSections {
  competitor_analysis: CompetitorAnalysis;
  target_search_queries: TargetSearchQuery[];
  seo_improvements: SeoImprovements;
  top_services: TopServiceItem[];
  target_audience: TargetAudience;
}

export interface LinkAnalysisResponse {
  success: boolean;
  website: string;
  metadata: AnalysisMetadata;
  brand: BrandInfo;
  technical_seo_audit: TechnicalSeoAudit;
  analysis: AnalysisSections;
}

export interface ApiError {
  detail: string;
  error_code: string;
}
