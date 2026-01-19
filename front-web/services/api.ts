
const BASE_URL = 'http://localhost:5000';

export const apiService = {
  async createThread(): Promise<{ conversation_id: string }> {
    const response = await fetch(`${BASE_URL}/threads`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!response.ok) throw new Error('Failed to create thread');
    return response.json();
  },

  async registerTool(toolDef: any): Promise<any> {
    const response = await fetch(`${BASE_URL}/tools`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(toolDef),
    });
    if (!response.ok) throw new Error('Failed to register tool');
    return response.json();
  },

  async sendMessage(conversation_id: string, prompt: string): Promise<any> {
    const response = await fetch(`${BASE_URL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ conversation_id, prompt }),
    });
    if (!response.ok) throw new Error('Failed to send message');
    return response.json();
  },

  async sendToolResult(conversation_id: string, tool_name: string, tool_output: string): Promise<any> {
    const response = await fetch(`${BASE_URL}/tools/result`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ conversation_id, tool_name, tool_output }),
    });
    if (!response.ok) throw new Error('Failed to send tool result');
    return response.json();
  },

  async getThreadHistory(thread_id: string): Promise<any[]> {
    const response = await fetch(`${BASE_URL}/threads/${thread_id}/history`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!response.ok) throw new Error('Failed to fetch thread history');
    return response.json();
  }
};
