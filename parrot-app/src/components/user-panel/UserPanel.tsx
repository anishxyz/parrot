'use client'

import React, {useState} from 'react';
import {useOpenApi} from "@/context/OpenApiContext";
import HeadersInput, {Header} from "@/components/user-panel/HeadersInput";
import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "@/components/ui/card";
import {Button} from "@/components/ui/button";
import {Textarea} from "@/components/ui/textarea";
import BaseURLInput from "@/components/user-panel/BaseURLInput";

export default function UserPanel() {
    const { apiContent } = useOpenApi();
    const [headers, setHeaders] = useState<Header[]>([
        { name: "Authorization", value: "Bearer <token>" },
        { name: "Content-Type", value: "application/json" },
    ]);
    const [baseURL, setBaseURL] = useState<string>('');

    const handleAutoLoad = () => {
        // Set baseURL from servers if available
        if (apiContent && apiContent.servers && apiContent.servers.length > 0) {
            setBaseURL(apiContent.servers[0].url);
        }

        // Update headers based on security schemes
        if (apiContent && apiContent.components && apiContent.components.securitySchemes) {
            const schemes = apiContent.components.securitySchemes;
            const newHeaders = Object.keys(schemes).map(key => {
                const scheme = schemes[key];
                if (scheme.type === 'apiKey' && scheme.in === 'header') {
                    return { name: scheme.name, value: "<apiKey>" }; // Placeholder value
                }
                return null;
            }).filter(header => header !== null);

            setHeaders([...newHeaders]);
        }
    };


    return (
        <div className='p-8'>
            <Card className="w-full mb-8">
                <CardHeader>
                    <div className='flex items-start justify-between'>
                        <div>
                            <CardTitle className='mb-2'>OpenAPI Agent</CardTitle>
                            <CardDescription>Enter a prompt for the AI agent to respond to.</CardDescription>
                        </div>
                        <Button
                            variant="ghost"
                            className="mr-2"
                            onClick={handleAutoLoad}
                        >
                            Auto Load
                        </Button>
                    </div>
                </CardHeader>
                <CardContent className="grid gap-4">
                    <Textarea placeholder="Enter your prompt here..." className="resize-none font-mono" rows={6} />
                    <Button
                        variant="default"
                        className="bg-orange-500 text-white font-mono text-md hover:bg-orange-600 focus:ring-orange-500"
                    >
                        Run Agent
                    </Button>
                </CardContent>
            </Card>
            <div className="mb-8">
                <BaseURLInput baseURL={baseURL} setBaseURL={setBaseURL}/>
            </div>
            <HeadersInput headers={headers} setHeaders={setHeaders}/>
        </div>
    );
};
