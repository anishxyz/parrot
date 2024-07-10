import React from "react";
import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "@/components/ui/card";
import {Input} from "@/components/ui/input";

interface BaseURLInputProps {
    baseURL: string;
    setBaseURL: React.Dispatch<React.SetStateAction<string>>;
}

export default function BaseURLInput({ baseURL, setBaseURL }: BaseURLInputProps) {

    return (
        <Card className="w-full">
            <CardHeader>
                <CardTitle>API Base URL</CardTitle>
                <CardDescription>Enter the base URL for the API you want to use.</CardDescription>
            </CardHeader>
            <CardContent className="grid gap-4">
                <Input placeholder="https://api.example.com" className="font-mono" value={baseURL} onChange={(e) => setBaseURL(e.target.value)} />
            </CardContent>
        </Card>
    );

}