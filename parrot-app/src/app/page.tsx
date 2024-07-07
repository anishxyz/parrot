'use client'

import {
    ResizableHandle,
    ResizablePanel,
    ResizablePanelGroup,
} from "@/components/ui/resizable"
import TabSidebar from "@/components/tab-sidebar/tab-sidebar";
import {createContext, Dispatch, SetStateAction, useState} from "react";

interface ApiContextType {
    apiContent: string;
    setApiContent: Dispatch<SetStateAction<string>>;
}

const openApiContext = createContext<ApiContextType>({
    apiContent: '',
    setApiContent: () => {}, // Default no-op function
});

export { openApiContext };

export default function Home() {
    const [apiContent, setApiContent] = useState('');

    return (
        <openApiContext.Provider value={{apiContent, setApiContent}}>
            <div className="w-screen h-screen">
                <ResizablePanelGroup
                    direction="horizontal"
                    className="rounded-lg border"
                >
                    <ResizablePanel defaultSize={50}>
                        <div className="flex p-6">
                            <span className="font-semibold">Sidebar</span>
                        </div>
                    </ResizablePanel>
                    <ResizableHandle withHandle/>
                    <ResizablePanel defaultSize={50}>
                        <TabSidebar/>
                    </ResizablePanel>
                </ResizablePanelGroup>
            </div>
        </openApiContext.Provider>

    );
}
