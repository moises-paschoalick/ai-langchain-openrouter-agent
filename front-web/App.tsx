
import React, { useState, useEffect, useCallback, useRef } from 'react';
import Sidebar from './components/Sidebar';
import ChatContainer from './components/ChatContainer';
import Toast from './components/Toast';
import HistoryView from './components/HistoryView';
import { AssistantConfig, Message, MessageRole, Thread, ToolDefinition } from './types';
import { apiService } from './services/api';

const App: React.FC = () => {
  // Assistant Settings
  const [config, setConfig] = useState<AssistantConfig>(() => {
    const saved = localStorage.getItem('assistant_config');
    return saved ? JSON.parse(saved) : {
      name: 'Default Assistant',
      systemInstructions: 'You are a helpful assistant.',
      model: 'gpt-4o',
      tools: []
    };
  });

  // Application State
  const [threads, setThreads] = useState<Thread[]>(() => {
    const saved = localStorage.getItem('assistant_threads');
    return saved ? JSON.parse(saved) : [];
  });
  const [currentThreadId, setCurrentThreadId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isDebugMode, setIsDebugMode] = useState(false);

  // History View State
  const [showHistory, setShowHistory] = useState(false);
  const [historyThreadId, setHistoryThreadId] = useState<string | null>(null);
  const [historyMessages, setHistoryMessages] = useState<any[]>([]);

  // Sync config and threads to local storage
  useEffect(() => {
    localStorage.setItem('assistant_config', JSON.stringify(config));
  }, [config]);

  useEffect(() => {
    localStorage.setItem('assistant_threads', JSON.stringify(threads));
  }, [threads]);

  // Handle creating a new thread
  const handleNewThread = async () => {
    try {
      setIsLoading(true);
      const { conversation_id } = await apiService.createThread();
      const newThread: Thread = {
        conversation_id,
        name: `Conversation ${threads.length + 1}`,
        createdAt: Date.now()
      };
      setThreads(prev => [newThread, ...prev]);
      setCurrentThreadId(conversation_id);
      setMessages([]);
    } catch (err) {
      setError('Erro interno ao processar a requisição. Verifique o backend.');
    } finally {
      setIsLoading(false);
    }
  };

  // Handle switching threads and loading history
  const handleSelectThread = async (threadId: string) => {
    try {
      setIsLoading(true);
      setCurrentThreadId(threadId);
      const history = await apiService.getThreadHistory(threadId);
      // Map API history to internal Message interface
      const mappedHistory = history.map((h: any, idx: number) => ({
        id: `hist-${idx}`,
        role: h.role as MessageRole,
        content: h.content || h.prompt || '',
        timestamp: Date.now(), // Real backend should provide timestamp
        toolDetails: h.tool ? {
          toolName: h.tool,
          toolCallId: h.tool_call_id,
          toolInput: h.tool_input,
          toolOutput: h.tool_output
        } : undefined
      }));
      setMessages(mappedHistory);
    } catch (err) {
      setError('Erro ao carregar histórico da thread.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteThread = (threadId: string) => {
    setThreads(prev => prev.filter(t => t.conversation_id !== threadId));
    if (currentThreadId === threadId) {
      setCurrentThreadId(null);
      setMessages([]);
    }
    // Note: Backend deletion is not implemented yet.
  };

  const handleViewHistory = async (threadId: string) => {
    try {
      setHistoryThreadId(threadId);
      setShowHistory(true);
      const history = await apiService.getThreadHistory(threadId);
      setHistoryMessages(history);
    } catch (err) {
      setError('Erro ao carregar histórico completo.');
    }
  };

  const handleRegisterTool = async (tool: ToolDefinition) => {
    try {
      const toolDef = {
        name: tool.name,
        description: tool.description,
        parameters: JSON.parse(tool.inputStructure),
        strict: false // Default to false or add to UI
      };
      await apiService.registerTool(toolDef);
      alert(`Tool ${tool.name} registered successfully!`);
    } catch (err) {
      setError('Erro ao registrar tool. Verifique o JSON.');
    }
  };

  // Handle sending user message
  const handleSendMessage = async (prompt: string) => {
    if (!currentThreadId) {
      // Auto-create thread if none selected
      await handleNewThread();
      return;
    }

    const userMessage: Message = {
      id: Date.now().toString(),
      role: MessageRole.USER,
      content: prompt,
      timestamp: Date.now()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await apiService.sendMessage(currentThreadId, prompt);
      handleApiResponse(response);
    } catch (err) {
      setError('Erro interno ao processar a requisição. Verifique o backend.');
    } finally {
      setIsLoading(false);
    }
  };

  // Process response from backend (could be text or tool call)
  const handleApiResponse = (response: any) => {
    if (response.type === 'tool_call') {
      const toolCallMessage: Message = {
        id: `tool-${Date.now()}`,
        role: MessageRole.TOOL_CALL,
        content: `Calling tool: ${response.tool}`,
        timestamp: Date.now(),
        toolDetails: {
          toolName: response.tool,
          toolCallId: response.tool_call_id,
          toolInput: response.tool_input
        }
      };
      setMessages(prev => [...prev, toolCallMessage]);
    } else {
      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        role: MessageRole.ASSISTANT,
        content: response.content || response.text || "Sem resposta do servidor.",
        timestamp: Date.now()
      };
      setMessages(prev => [...prev, assistantMessage]);
    }
  };

  // Handle tool result submission
  const handleToolSubmit = async (toolName: string, output: string) => {
    if (!currentThreadId) return;

    const resultMessage: Message = {
      id: `res-${Date.now()}`,
      role: MessageRole.TOOL_RESULT,
      content: `Result: ${output}`,
      timestamp: Date.now(),
      toolDetails: {
        toolName,
        toolOutput: output
      }
    };

    setMessages(prev => [...prev, resultMessage]);
    setIsLoading(true);

    try {
      const response = await apiService.sendToolResult(currentThreadId, toolName, output);
      handleApiResponse(response);
    } catch (err) {
      setError('Erro ao enviar resultado da tool.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen overflow-hidden bg-[#0b0b0b] relative">
      {/* Sidebar - Config */}
      <Sidebar
        config={config}
        setConfig={setConfig}
        threads={threads}
        currentThreadId={currentThreadId}
        onNewThread={handleNewThread}
        onSelectThread={handleSelectThread}
        onDeleteThread={handleDeleteThread}
        onViewHistory={handleViewHistory}
        onRegisterTool={handleRegisterTool}
        isDebugMode={isDebugMode}
        setIsDebugMode={setIsDebugMode}
      />

      {/* Main Content - Chat */}
      <div className="flex-1 flex flex-col relative">
        <ChatContainer
          messages={messages}
          onSendMessage={handleSendMessage}
          onToolSubmit={handleToolSubmit}
          isLoading={isLoading}
          currentThreadId={currentThreadId}
          isDebugMode={isDebugMode}
        />
      </div>

      {/* History View Sidebar */}
      {showHistory && historyThreadId && (
        <HistoryView
          threadId={historyThreadId}
          history={historyMessages}
          onClose={() => setShowHistory(false)}
        />
      )}

      {/* Error Toasts */}
      {error && <Toast message={error} onClose={() => setError(null)} />}
    </div>
  );
};

export default App;
