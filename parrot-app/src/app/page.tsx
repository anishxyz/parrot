'use client'

import {
    ResizableHandle,
    ResizablePanel,
    ResizablePanelGroup,
} from "@/components/ui/resizable"
import TabSidebar from "@/components/tab-bar/TabSidebar";
import {OpenApiProvider} from "@/context/OpenApiContext";
import UserPanel from "@/components/user-panel/UserPanel";



export default function Home() {

    return (
        <OpenApiProvider>
            <div className="w-screen h-screen">
                <ResizablePanelGroup
                    direction="horizontal"
                    className="rounded-lg border"
                >
                    <ResizablePanel defaultSize={50}>
                        <UserPanel/>
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
