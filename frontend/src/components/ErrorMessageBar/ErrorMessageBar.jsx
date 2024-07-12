// ErrorMessageBar.jsx
import React from 'react';
import {Card, CardBody} from '@nextui-org/react';

export const ErrorMessageBar = ({ message, visible }) => {
    if (!visible) return null;

    return (
        <div style={{display: "flex", justifyContent: "center", padding: "4px"}}>
        <Card
            style={{
                animation: 'grow 0.5s ease-out',
                zIndex: 1000,
                width: '100%',
                backgroundColor: '#f8d7da',
                color: '#721c24',
                alignItems: 'center',
            }}
        >
            <CardBody>
                <div>
                    <p>{message}</p>
                </div>
            </CardBody>
        </Card>
        <style>{`
            @keyframes grow {
              0% {
                transform: scale(0);
              }
              100% {
                transform: scale(1);
              }
            }
        `}</style>
        </div>
    );
};
