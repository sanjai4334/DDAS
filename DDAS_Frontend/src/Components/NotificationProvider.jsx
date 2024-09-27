// NotificationProvider.jsx
import React from 'react';
import { SnackbarProvider } from 'notistack';

export default function NotificationProvider({ children }) {
    return (
        <SnackbarProvider maxSnack={3} anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}>
            {children}
        </SnackbarProvider>
    );
}
