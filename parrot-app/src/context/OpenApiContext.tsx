import React, { createContext, useState, useContext, ReactNode } from 'react';

interface OpenApiContextType {
    apiContent: any;
    setApiContent: React.Dispatch<React.SetStateAction<any>>;
    activeTab: string;
    setActiveTab: React.Dispatch<React.SetStateAction<string>>;
}

const OpenApiContext = createContext<OpenApiContextType | null>(null);

interface OpenApiProviderProps {
    children: ReactNode;
}

export const OpenApiProvider: React.FC<OpenApiProviderProps> = ({ children }) => {
    const [apiContent, setApiContent] = useState<any>(null);
    const [activeTab, setActiveTab] = useState<string>('agent');

    return (
        <OpenApiContext.Provider value={{ apiContent, setApiContent, activeTab, setActiveTab }}>
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
