/**
 * TypeScript types for the Bricksmith Architect frontend.
 * These mirror the Pydantic schemas from the backend API.
 */

export interface Component {
  id: string;
  label: string;
  type: string;
  logo_name?: string;
}

export interface Connection {
  from_id: string;
  to_id: string;
  label?: string;
  style: 'solid' | 'dashed' | 'dotted';
}

export interface ArchitectureState {
  components: Component[];
  connections: Connection[];
  title?: string;
  subtitle?: string;
}

export interface Session {
  session_id: string;
  initial_problem: string;
  status: 'active' | 'completed';
  created_at: string;
  turn_count: number;
  current_architecture?: ArchitectureState;
}

export interface SessionListResponse {
  sessions: Session[];
  total: number;
}

export interface MCPEnrichmentOptions {
  enabled: boolean;
  sources: string[];
}

export interface CreateSessionRequest {
  initial_problem: string;
  custom_context?: string;
  logo_dir?: string;
  image_provider?: 'gemini' | 'openai' | 'databricks';
  openai_api_key?: string;
  vertex_api_key?: string;
  reference_prompt?: string;
  reference_prompt_path?: string;
  reference_image_base64?: string;
  reference_image_filename?: string;
  reference_images_base64?: string[];
  reference_images_filenames?: string[];
  mcp_enrichment?: MCPEnrichmentOptions;
}

export interface SendMessageRequest {
  message: string;
  image_base64?: string;
  image_filename?: string;
}

export interface MessageResponse {
  response: string;
  ready_for_output: boolean;
  architecture: ArchitectureState;
  turn_number: number;
}

export interface StatusResponse {
  session_id: string;
  status: string;
  turn_count: number;
  ready_for_output: boolean;
  architecture: ArchitectureState;
  available_logos: string[];
  image_provider: 'gemini' | 'openai' | 'databricks';
  credential_mode: 'environment' | 'custom_key';
}

export interface GenerateOutputResponse {
  success: boolean;
  output_dir?: string;
  prompt_file?: string;
  architecture_file?: string;
  error?: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  architecture?: ArchitectureState;
  imageUrl?: string;
  attachedImageBase64?: string;
}

export interface TurnSchema {
  turn_number: number;
  user_input: string;
  architect_response: string;
  architecture_snapshot?: Record<string, unknown> | null;
  created_at?: string;
}

export interface TurnsResponse {
  turns: TurnSchema[];
}

export interface GeneratePreviewResponse {
  success: boolean;
  image_url?: string;
  image_urls?: string[];
  run_id?: string;
  error?: string;
}

export interface CLICommandSpec {
  name: string;
  description: string;
  examples: string[];
  supports_stdin: boolean;
}

export interface CLICommandsResponse {
  commands: CLICommandSpec[];
}

export type CliJobStatus =
  | 'queued'
  | 'running'
  | 'succeeded'
  | 'failed'
  | 'cancelled'
  | 'timeout';

export interface CliJob {
  job_id: string;
  status: CliJobStatus;
  command: string;
  args: string[];
  started_at: string;
  ended_at?: string;
  exit_code?: number;
  stdout: string;
  stderr: string;
  timeout_seconds: number;
}

export interface StartCliJobRequest {
  command: string;
  args: string[];
  stdin_text?: string;
  timeout_seconds?: number;
}

export interface StartCliJobResponse {
  job: CliJob;
}

export interface BestResultItem {
  result_id: string;
  source: 'chat' | 'generate_raw' | 'refine' | 'unknown';
  title: string;
  image_path?: string;
  image_url?: string;
  prompt_path?: string;
  prompt_preview: string;
  full_prompt?: string;
  run_id?: string;
  run_group?: string;
  score?: number;
  score_source?: string;
  created_at?: string;
  relative_output_dir: string;
  notes?: string;
}

export interface BestResultsResponse {
  results: BestResultItem[];
  total: number;
}

export interface PromptFileItem {
  path: string;
  relative_path: string;
  preview: string;
  size: number;
  modified_at?: string;
}

export interface PromptFilesResponse {
  files: PromptFileItem[];
  total: number;
}

export interface GenerateFromDocRequest {
  document_text: string;
  filename?: string;
}

export interface GenerateFromDocResponse {
  prompt: string;
}

// Refinement loop types

export interface EvaluationScores {
  information_hierarchy: number;
  technical_accuracy: number;
  logo_fidelity: number;
  visual_clarity: number;
  data_flow_legibility: number;
  text_readability: number;
}

export interface RefinementIteration {
  iteration: number;
  prompt_used: string;
  image_url: string;
  image_urls: string[];
  overall_score?: number;
  scores?: EvaluationScores;
  strengths: string[];
  issues: string[];
  improvements: string[];
  feedback_for_refinement: string;
  user_feedback?: string;
  refinement_reasoning?: string;
  settings_used?: GenerationSettingsRequest;
  created_at: string;
}

export interface RefinementState {
  session_id: string;
  status: 'idle' | 'generating' | 'evaluating' | 'refining';
  original_prompt: string;
  current_prompt: string;
  current_image_url?: string;
  iterations: RefinementIteration[];
  iteration_count: number;
}

export interface RefinementIterationResponse {
  success: boolean;
  iteration?: RefinementIteration;
  error?: string;
}

export interface RefineRequest {
  user_feedback: string;
  user_score?: number;
}

export interface RefineResponse {
  success: boolean;
  refined_prompt?: string;
  reasoning?: string;
  expected_improvement?: string;
  error?: string;
}

// Standalone refinement types

export interface StartStandaloneRefinementRequest {
  prompt?: string;
  prompt_file?: string;
  image_provider?: 'gemini' | 'openai' | 'databricks';
  gemini_model?: string;
  openai_api_key?: string;
  vertex_api_key?: string;
  persona?: 'architect' | 'executive' | 'developer' | 'auto';
  aspect_ratio?: string;
  image_size?: string;
  folder?: string;
  num_variants?: number;
}

export const GEMINI_MODELS = [
  {
    value: 'gemini-3-pro-image-preview',
    label: 'Nano Banana Pro',
    desc: 'Best quality, reasoning-driven (default)',
  },
  {
    value: 'gemini-2.5-flash-image',
    label: 'Nano Banana',
    desc: 'Faster, cheaper, good for iteration',
  },
] as const;

// Generation settings types

export interface GenerationSettingsRequest {
  preset?: string;
  image_size?: string;
  aspect_ratio?: string;
  num_variants?: number;
}

export const TEMPERATURE_PRESETS = [
  { value: 'deterministic', label: 'Deterministic', temp: '0.0' },
  { value: 'conservative', label: 'Conservative', temp: '0.4' },
  { value: 'balanced', label: 'Balanced', temp: '0.8' },
  { value: 'creative', label: 'Creative', temp: '1.2' },
  { value: 'wild', label: 'Wild', temp: '1.8' },
] as const;

export const IMAGE_SIZES = ['1K', '2K', '4K'] as const;

export const ASPECT_RATIOS = ['16:9', '1:1', '4:3', '9:16', '3:4', '21:9'] as const;
