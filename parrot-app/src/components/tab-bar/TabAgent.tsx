import {useOpenApi} from "@/context/OpenApiContext";
import AgentLogItem from "@/components/tab-bar/AgentLogItem";


export default function TabAgent() {
    const { agentLogs} = useOpenApi();

    return (
        <div className='p-8'>
            {agentLogs.map((log, index) => (
                <div key={index} className='mb-4'>
                    <AgentLogItem type={log.type} message={log.message} metadata={log.metadata} terminal={log.terminal}/>
                </div>
            ))}
        </div>
    );
}