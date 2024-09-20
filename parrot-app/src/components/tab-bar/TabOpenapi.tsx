import {Input} from "@/components/ui/input"
import {useState} from "react";
import {Editor} from "@monaco-editor/react";
import {Button} from "@/components/ui/button";
import {useOpenApi} from "@/context/OpenApiContext";
import { dereference } from '@scalar/openapi-parser'

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

    const getCircularReplacer = () => {
        const seen = new WeakSet();
        return (key, value) => {
            if (typeof value === "object" && value !== null) {
                if (seen.has(value)) {
                    return "[Circular Reference]";
                }
                seen.add(value);
            }
            return value;
        };
    };

    const resolveOpenApiContent = async () => {
        const { schema, errors } = await dereference(apiContent);

        console.log("ERR", errors);
        console.log("SCH", schema);

        if (errors?.length === 0) {
            const safeJsonString = JSON.stringify(schema, getCircularReplacer(), 2);
            setApiContent(safeJsonString);

            // Create a Blob with the safe JSON content
            const blob = new Blob([safeJsonString], { type: 'application/json' });

            // Create a temporary URL for the Blob
            const url = URL.createObjectURL(blob);

            // Create a temporary anchor element
            const link = document.createElement('a');
            link.href = url;
            link.download = 'schema.json'; // Set the file name

            // Append the link to the body, click it, and remove it
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            // Clean up the temporary URL
            URL.revokeObjectURL(url);
        }
    }

    const handleEditorChange = (value: string) => {
        try {
            const jsonObject = JSON.parse(value);
            setApiContent(jsonObject);
        } catch (error) {
            // If parsing fails, don't update the state
            console.warn('Invalid JSON:', error);
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
                    onClick={resolveOpenApiContent}
                    variant='secondary'
                    className="mr-2"
                    size='sm'
                >
                    Resolve
                </Button>
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
                    onChange={handleEditorChange}
                    options={{
                        minimap: {enabled: false}
                    }}
                />
            </div>
        </div>
    );
}