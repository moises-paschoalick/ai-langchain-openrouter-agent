
import React from 'react';
import { AssistantConfig, Thread, ToolDefinition } from '../types';
import { Plus, MessageSquare, Tool, Settings, Trash2, Code } from 'lucide-react';

interface SidebarProps {
  config: AssistantConfig;
  setConfig: React.Dispatch<React.SetStateAction<AssistantConfig>>;
  threads: Thread[];
  currentThreadId: string | null;
  onNewThread: () => void;
  onSelectThread: (id: string) => void;
  isDebugMode: boolean;
  setIsDebugMode: (val: boolean) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ 
  config, 
  setConfig, 
  threads, 
  currentThreadId, 
  onNewThread, 
  onSelectThread,
  isDebugMode,
  setIsDebugMode
}) => {

  const addTool = () => {
    const newTool: ToolDefinition = {
      id: Date.now().toString(),
      name: 'new_tool',
      description: 'Describe what the tool does',
      inputStructure: '{}'
    };
    setConfig(prev => ({ ...prev, tools: [...prev.tools, newTool] }));
  };

  const updateTool = (id: string, updates: Partial<ToolDefinition>) => {
    setConfig(prev => ({
      ...prev,
      tools: prev.tools.map(t => t.id === id ? { ...t, ...updates } : t)
    }));
  };

  const removeTool = (id: string) => {
    setConfig(prev => ({
      ...prev,
      tools: prev.tools.filter(t => t.id !== id)
    }));
  };

  return (
    <div className="w-80 bg-[#171717] border-r border-[#2d2d2d] flex flex-col overflow-hidden">
      <div className="p-4 border-b border-[#2d2d2d] flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Settings className="w-5 h-5 text-emerald-500" />
          <h2 className="text-lg font-bold">Configuração</h2>
        </div>
        <button 
          onClick={() => setIsDebugMode(!isDebugMode)}
          title="Toggle Debug Mode"
          className={`p-1.5 rounded transition ${isDebugMode ? 'bg-emerald-500/20 text-emerald-400' : 'text-gray-400 hover:bg-[#2d2d2d]'}`}
        >
          <Code className="w-4 h-4" />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {/* Basic Config */}
        <section className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Assistant Name</label>
            <input 
              type="text" 
              value={config.name}
              onChange={(e) => setConfig({ ...config, name: e.target.value })}
              className="w-full bg-[#212121] border border-[#2d2d2d] rounded-md px-3 py-2 focus:ring-1 focus:ring-emerald-500 outline-none text-sm"
              placeholder="Ex: Customer Support"
            />
          </div>
          <div>
            <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Model</label>
            <input 
              type="text" 
              value={config.model}
              onChange={(e) => setConfig({ ...config, model: e.target.value })}
              className="w-full bg-[#212121] border border-[#2d2d2d] rounded-md px-3 py-2 focus:ring-1 focus:ring-emerald-500 outline-none text-sm font-mono"
              placeholder="gpt-4o"
            />
          </div>
          <div>
            <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">System Instructions</label>
            <textarea 
              rows={4}
              value={config.systemInstructions}
              onChange={(e) => setConfig({ ...config, systemInstructions: e.target.value })}
              className="w-full bg-[#212121] border border-[#2d2d2d] rounded-md px-3 py-2 focus:ring-1 focus:ring-emerald-500 outline-none text-sm resize-none"
              placeholder="Define rules for the assistant..."
            />
          </div>
        </section>

        {/* Tools Section */}
        <section className="space-y-4">
          <div className="flex items-center justify-between">
            <label className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Tools</label>
            <button onClick={addTool} className="p-1 hover:bg-[#2d2d2d] rounded text-emerald-500">
              <Plus className="w-4 h-4" />
            </button>
          </div>
          <div className="space-y-4">
            {config.tools.map((tool) => (
              <div key={tool.id} className="p-3 bg-[#212121] border border-[#2d2d2d] rounded-md relative group">
                <button 
                  onClick={() => removeTool(tool.id)}
                  className="absolute top-2 right-2 p-1 text-gray-500 hover:text-red-400 opacity-0 group-hover:opacity-100 transition"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
                <input 
                  type="text" 
                  value={tool.name}
                  onChange={(e) => updateTool(tool.id, { name: e.target.value })}
                  className="bg-transparent border-b border-[#2d2d2d] w-full text-sm font-bold mb-2 focus:border-emerald-500 outline-none"
                />
                <textarea 
                  value={tool.description}
                  onChange={(e) => updateTool(tool.id, { description: e.target.value })}
                  className="bg-transparent text-xs text-gray-400 w-full resize-none h-10 outline-none"
                  placeholder="Tool description..."
                />
                <div className="mt-2">
                  <span className="text-[10px] text-gray-500 uppercase font-bold">Input Structure (JSON)</span>
                  <textarea 
                    value={tool.inputStructure}
                    onChange={(e) => updateTool(tool.id, { inputStructure: e.target.value })}
                    className="w-full bg-black/30 text-[11px] font-mono p-2 mt-1 rounded border border-[#2d2d2d] outline-none"
                    rows={3}
                  />
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Threads History */}
        <section className="space-y-4 pt-4 border-t border-[#2d2d2d]">
          <div className="flex items-center justify-between">
            <label className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Threads</label>
            <button 
              onClick={onNewThread}
              className="flex items-center space-x-1 text-xs text-emerald-500 hover:text-emerald-400 transition"
            >
              <Plus className="w-3.5 h-3.5" />
              <span>New Thread</span>
            </button>
          </div>
          <div className="space-y-1">
            {threads.length === 0 && (
              <p className="text-xs text-gray-500 italic px-2">No conversations yet.</p>
            )}
            {threads.map(thread => (
              <button
                key={thread.conversation_id}
                onClick={() => onSelectThread(thread.conversation_id)}
                className={`w-full text-left px-3 py-2 rounded-md transition text-sm flex items-center space-x-2 ${
                  currentThreadId === thread.conversation_id 
                    ? 'bg-[#2d2d2d] text-white' 
                    : 'text-gray-400 hover:bg-[#212121] hover:text-gray-200'
                }`}
              >
                <MessageSquare className="w-4 h-4 flex-shrink-0" />
                <span className="truncate">{thread.name}</span>
              </button>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
};

export default Sidebar;
