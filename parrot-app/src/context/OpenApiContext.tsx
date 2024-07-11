import React, { createContext, useState, useContext, ReactNode } from 'react';

export enum AgentLogType {
    TOOL_IN = 'tool_in',
    TOOL_OUT = 'tool_out',
    INFO = 'info',
    ERROR = 'error'
}

export interface AgentLog {
    type: AgentLogType;
    message: string;
    metadata?: Record<string, any>;
    terminal?: boolean;
}

interface OpenApiContextType {
    apiContent: any;
    setApiContent: React.Dispatch<React.SetStateAction<any>>;
    activeTab: string;
    setActiveTab: React.Dispatch<React.SetStateAction<string>>;
    activeAgent: boolean;
    setActiveAgent: React.Dispatch<React.SetStateAction<boolean>>;
    agentLogs: AgentLog[];
    setAgentLogs: React.Dispatch<React.SetStateAction<AgentLog[]>>;
}

const OpenApiContext = createContext<OpenApiContextType | null>(null);

interface OpenApiProviderProps {
    children: ReactNode;
}

export const OpenApiProvider: React.FC<OpenApiProviderProps> = ({ children }) => {
    const [apiContent, setApiContent] = useState<any>(null);
    const [activeTab, setActiveTab] = useState<string>('agent');
    const [activeAgent, setActiveAgent] = useState<boolean>(false);
    const [agentLogs, setAgentLogs] = useState<AgentLog[]>([]);

    return (
        <OpenApiContext.Provider value={{ apiContent, setApiContent, activeTab, setActiveTab, activeAgent, setActiveAgent, agentLogs, setAgentLogs }}>
            {children}
        </OpenApiContext.Provider>
    );
};

export const useOpenApi = () => {
    const context = useContext(OpenApiContext);
    if (!context) {
        throw new Error('useOpenApi must be used within a OpenApiProvider');
    }
    return context;
};

export function parseAgentLog(message: string): AgentLog | null {
    try {
        const parsed = JSON.parse(message) as AgentLog;
        if (Object.values(AgentLogType).includes(parsed.type) && typeof parsed.message === 'string') {
            // Optional: Add further validation if necessary
            return parsed;
        }
        console.error('Invalid agent log format:', message);
    } catch (error) {
        console.error('Error parsing agent log:', error);
    }
    return null;
}