import { RouterProvider } from 'react-router-dom';

import { CssBaseline, ThemeProvider } from '@mui/material';
import { QueryClientProvider } from '@tanstack/react-query';
import { QueryClient } from '@tanstack/react-query';
import { SnackbarProvider } from 'notistack';

import { router } from './router/router';
import { mainTheme } from './theme/main';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
    },
  },
});

export const App = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={mainTheme}>
        <CssBaseline />
        <SnackbarProvider>
          <RouterProvider router={router} />
        </SnackbarProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
};
