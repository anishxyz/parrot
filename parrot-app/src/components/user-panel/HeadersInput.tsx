/**
 * v0 by Vercel.
 * @see https://v0.dev/t/CnuJ0YAv0Bi
 * Documentation: https://v0.dev/docs#integrating-generated-code-into-your-nextjs-app
 */
"use client"

import React, { useState } from "react"
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card"
import { Table, TableHeader, TableRow, TableHead, TableBody, TableCell } from "@/components/ui/table"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export interface Header {
    name: string;
    value: string;
}

interface HeadersInputProps {
    headers: Header[];
    setHeaders: React.Dispatch<React.SetStateAction<Header[]>>;
}

export default function HeadersInput({ headers, setHeaders }: HeadersInputProps) {

    const addHeader = () => {
        setHeaders([...headers, { name: "", value: "" }])
    }

    const updateHeader = (index: number, field: keyof Header, value: string) => {
        const updatedHeaders = [...headers];
        updatedHeaders[index][field] = value;
        setHeaders(updatedHeaders);
    };

    const removeHeader = (index: number) => {
        const updatedHeaders = [...headers]
        updatedHeaders.splice(index, 1)
        setHeaders(updatedHeaders)
    }
    return (
        <Card className="w-full">
            <CardHeader>
                <CardTitle>API Headers</CardTitle>
                <CardDescription>Manage the headers that will be sent with your API requests.</CardDescription>
            </CardHeader>
            <CardContent>
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>Header Name</TableHead>
                            <TableHead>Header Value</TableHead>
                            <TableHead>
                                <Button size="sm" variant="outline" onClick={addHeader} className="ml-auto">
                                    Add
                                </Button>
                            </TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {headers.map((header, index) => (
                            <TableRow key={index}>
                                <TableCell>
                                    <Input value={header.name} className="font-mono" onChange={(e) => updateHeader(index, "name", e.target.value)} />
                                </TableCell>
                                <TableCell>
                                    <Input value={header.value} className="font-mono" onChange={(e) => updateHeader(index, "value", e.target.value)} />
                                </TableCell>
                                <TableCell>
                                    <Button size="sm" variant="ghost" onClick={() => removeHeader(index)}>
                                        <TrashIcon className="h-4 w-4" />
                                    </Button>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </CardContent>
        </Card>
    )
}

interface TrashIconProps {
    className?: string;
}


function TrashIcon(props: TrashIconProps) {
    return (
        <svg
            {...props}
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
        >
            <path d="M3 6h18" />
            <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" />
            <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" />
        </svg>
    )
}