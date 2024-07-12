/**
 * v0 by Vercel.
 * @see https://v0.dev/t/FbX9OdSbdxy
 * Documentation: https://v0.dev/docs#integrating-generated-code-into-your-nextjs-app
 */
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import {AgentLog, AgentLogType} from "@/context/OpenApiContext";

export default function AgentLogItem({ type, message, metadata, terminal }: AgentLog) {
    return (
        <Card className={'w-full p-2'}>
            <CardContent className="grid gap-4">
                <div className="flex items-center gap-2">
                    <Badge variant="outline" className="text-s font-medium mt-2">
                        {type}
                    </Badge>
                </div>
                <div className="flex items-center gap-2">
                    <p>{message}</p>
                </div>
                {metadata && Object.keys(metadata).length > 0 && (
                    <div className="bg-muted rounded-md p-2 text-xs text-muted-foreground overflow-x-auto">
                        <pre>{JSON.stringify(metadata, null, 2)}</pre>
                    </div>
                )}
            </CardContent>
        </Card>
    );
}