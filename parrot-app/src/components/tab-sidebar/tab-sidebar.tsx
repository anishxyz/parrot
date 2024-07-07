'use client'

import { useState } from 'react';
import { Button } from "@/components/ui/button";

export default function TabSidebar() {
    const [activeTab, setActiveTab] = useState('agent');

    return (
        <div className="flex flex-row bg-secondary border-b-2 border-gray-200">
            <Button
                variant="secondary"
                size='sm'
                className={`rounded-none min-w-[150px] ${activeTab === 'agent' ? 'bg-white text-black shadow-none hover:bg-white' : 'text-gray-500 bg-transparent'}`}
                onClick={() => setActiveTab('agent')}
                style={{ borderRight: '1px solid #e0e0e0' }}
            >
                Agent Actions
            </Button>
            <Button
                variant="secondary"
                size='sm'
                className={`rounded-none min-w-[150px] hover ${activeTab === 'openapi' ? 'bg-white text-gray-700 shadow-none hover:bg-white' : 'text-gray-500 bg-transparent'}`}
                onClick={() => setActiveTab('openapi')}
            >
                OpenAPI Spec
            </Button>
        </div>
    );
}
