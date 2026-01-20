export type MessageType = 'sensor_update' | 'task_update' | 'note_update';

export interface SensorPayload {
    id: string;
    sensor_id: string;
    value: number;
    timestamp: string;
    metadata?: Record<string, any> | undefined;
}

export interface TaskPayload {
    id: string;                // Matches serializer 'id'
    name: string;              // Matches serializer 'name'
    status: string;            // Matches serializer 'status'
    group: string;             // Usually an ID if not nested
    description?: string;
    location: string;
    sensor?: number;           // Related sensor ID
    limit_value?: number;
    created_at: string;        // ISO Date string
    updated_at: string;        // ISO Date string
}


// The Discriminated Union
export type WSMessage = 
    | { type: 'sensor_update'; payload: SensorPayload }
    | { type: 'task_update'; payload: TaskPayload }
    | { type: 'note_update'; payload: any };