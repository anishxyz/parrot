'use client'

import React, {useState} from 'react';
import {useOpenApi} from "@/context/OpenApiContext";
import HeadersInput, {Header} from "@/components/user-panel/HeadersInput";
import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "@/components/ui/card";
import {Button} from "@/components/ui/button";
import {Textarea} from "@/components/ui/textarea";
import {Input} from "@/components/ui/input";
import BaseURLInput from "@/components/user-panel/BaseURLInput";

export default function UserPanel() {
    const { apiContent } = useOpenApi();
    const [headers, setHeaders] = useState<Header[]>([
        { name: "Authorization", value: "Bearer <token>" },
        { name: "Content-Type", value: "application/json" },
    ]);
    const [baseURL, setBaseURL] = useState<string>('');

    return (
        <div className='p-8'>
            <Card className="w-full mb-8">
                <CardHeader>
                    <CardTitle>OpenAPI Agent</CardTitle>
                    <CardDescription>Enter a prompt for the AI agent to respond to.</CardDescription>
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
            {/*{apiContent ? JSON.stringify(apiContent) : "Hello"}*/}
            <HeadersInput headers={headers} setHeaders={setHeaders}/>
        </div>
    );
};
