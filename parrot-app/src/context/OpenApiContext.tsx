import React, { createContext, useState, useContext, ReactNode } from 'react';

interface OpenApiContextType {
    apiContent: any;
    setApiContent: React.Dispatch<React.SetStateAction<any>>;
    activeTab: string;
    setActiveTab: React.Dispatch<React.SetStateAction<string>>;
    activeAgent: boolean;
    setActiveAgent: React.Dispatch<React.SetStateAction<boolean>>;
}

const OpenApiContext = createContext<OpenApiContextType | null>(null);

interface OpenApiProviderProps {
    children: ReactNode;
}

export const OpenApiProvider: React.FC<OpenApiProviderProps> = ({ children }) => {
    const [apiContent, setApiContent] = useState<any>(null);
    const [activeTab, setActiveTab] = useState<string>('agent');
    const [activeAgent, setActiveAgent] = useState<boolean>(false);

    return (
        <OpenApiContext.Provider value={{ apiContent, setApiContent, activeTab, setActiveTab, activeAgent, setActiveAgent }}>
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
