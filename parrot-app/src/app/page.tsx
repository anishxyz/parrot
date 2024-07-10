'use client'

import {
    ResizableHandle,
    ResizablePanel,
    ResizablePanelGroup,
} from "@/components/ui/resizable"
import TabSidebar from "@/components/tab-bar/tab-sidebar";
import {OpenApiProvider} from "@/context/OpenApiContext";



export default function Home() {

    return (
        <OpenApiProvider>
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
        </OpenApiProvider>

    );
}
