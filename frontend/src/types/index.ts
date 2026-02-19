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

export interface CreateSessionRequest {
  initial_problem: string;
  custom_context?: string;
  logo_dir?: string;
}

export interface SendMessageRequest {
  message: string;
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
}

export interface GeneratePreviewResponse {
  success: boolean;
  image_url?: string;
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
