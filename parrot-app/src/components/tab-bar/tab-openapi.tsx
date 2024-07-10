import {Input} from "@/components/ui/input"
import {useContext, useState} from "react";
import {Editor} from "@monaco-editor/react";
import {Button} from "@/components/ui/button";
import {useOpenApi} from "@/context/OpenApiContext";

export default function TabOpenapi() {
    const [openapiValue, setOpenapiValue] = useState('');
    const { apiContent, setApiContent } = useOpenApi();

    const [isLoading, setIsLoading] = useState(false);

    const fetchOpenApiJson = async () => {
        if (openapiValue) {
            setIsLoading(true);
            try {
                const response = await fetch(openapiValue);
                const json = await response.json();
                setApiContent(json);
            } catch (error) {
                console.error('Failed to fetch OpenAPI JSON:', error);
                setApiContent('{ "error": "Failed to load API content." }');
            }
            setIsLoading(false);
        }
    };

    return (
        <div className={'h-full flex flex-col'}>
            <div className="flex items-center border-b-2">
                <Input
                    className='rounded-none focus-visible:ring-transparent mt-1 mb-1 border-0 pb-2'
                    placeholder="api.company.com/openapi.json"
                    value={openapiValue}
                    onChange={(e) => setOpenapiValue(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === 'Enter') {
                            fetchOpenApiJson();
                        }
                    }}
                />
                <Button
                    onClick={fetchOpenApiJson}
                    variant='secondary'
                    className="mr-2"
                    size='sm'
                >
                    {isLoading ? 'Fetching...' : 'Fetch API'}
                </Button>
            </div>
            <div className={'flex-grow h-full w-full overflow-none'}>
                <Editor
                    // height="100%"
                    defaultLanguage="json"
                    defaultValue="// Enter OpenAPI JSON"
                    value={JSON.stringify(apiContent, null, 2)}
                    options={{
                        minimap: {enabled: false}
                    }}
                />
            </div>
        </div>
    );
}