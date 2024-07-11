import {useOpenApi} from "@/context/OpenApiContext";
import AgentLogItem from "@/components/tab-bar/AgentLogItem";


export default function TabAgent() {
    const { agentLogs} = useOpenApi();

    return (
        <div className='p-2'>
            <div className='mb-2'>
                {agentLogs.map((log, index) => (
                    <AgentLogItem key={index} type={log.type} message={log.message} metadata={log.metadata} terminal={log.terminal}/>
                ))}
            </div>
        </div>
    );
}