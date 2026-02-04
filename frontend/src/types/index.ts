/**
 * TypeScript types for the Nano Banana Architect frontend.
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
