import {
    ResizableHandle,
    ResizablePanel,
    ResizablePanelGroup,
} from "@/components/ui/resizable"
import TabSidebar from "@/components/tab-sidebar/tab-sidebar";

export default function Home() {
    return (
        <div className="w-screen h-screen">
            <ResizablePanelGroup
                direction="horizontal"
                className="rounded-lg border"
            >
                <ResizablePanel defaultSize={25}>
                    <div className="flex p-6">
                        <span className="font-semibold">Sidebar</span>
                    </div>
                </ResizablePanel>
                <ResizableHandle withHandle/>
                <ResizablePanel defaultSize={75}>
                    <TabSidebar/>
                </ResizablePanel>
            </ResizablePanelGroup>
        </div>
    );
}
