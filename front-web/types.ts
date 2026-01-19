
export enum MessageRole {
  USER = 'user',
  ASSISTANT = 'assistant',
  TOOL_CALL = 'tool_call',
  TOOL_RESULT = 'tool_result',
  SYSTEM = 'system'
}

export interface ToolDefinition {
  id: string;
  name: string;
  description: string;
  inputStructure: string; // JSON string representation
}

export interface Message {
  id: string;
  role: MessageRole;
  content: string;
  timestamp: number;
  toolDetails?: {
    toolName: string;
    toolCallId?: string;
    toolInput?: any;
    toolOutput?: string;
  };
}

export interface Thread {
  conversation_id: string;
  name: string;
  createdAt: number;
}

export interface AssistantConfig {
  name: string;
  systemInstructions: string;
  model: string;
  tools: ToolDefinition[];
}

export interface ChatResponse {
  type?: 'tool_call';
  tool?: string;
  tool_call_id?: string;
  tool_input?: any;
  content?: string; // Standard text response if not a tool call
}
