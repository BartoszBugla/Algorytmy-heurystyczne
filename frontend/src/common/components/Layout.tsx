import { PropsWithChildren } from 'react';
import { Outlet } from 'react-router-dom';

import { Box, Divider, Stack, Typography } from '@mui/material';

import { Header } from './Header';

interface LayoutProps {
  flexElement?: JSX.Element;
}

const Layout = ({ flexElement }: PropsWithChildren<LayoutProps>) => {
  return (
    <Stack minHeight='100vh'>
      <Header />
      {flexElement && (
        <Stack minHeight='100vh'>
          <Box
            sx={{
              flexGrow: 1,
              display: 'flex',
            }}
          >
            {flexElement}
          </Box>
        </Stack>
      )}

      <Box
        sx={{
          flex: 1,
          display: 'flex',
          alignItems: 'stretch',
          justifyContent: 'center',
          padding: 2,
        }}
      >
        <Outlet />
      </Box>

      <footer>
        <Divider />
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            gap: 1,
            padding: 2,
          }}
        >
          <Typography>© Cycly 2024</Typography>
          <Typography>Michał Bober</Typography>
          <Typography>Bartosz Bugla</Typography>
          <Typography>Patryk Buchtyar</Typography>
          <Typography>Bartosz Bieńkowski</Typography>
        </Box>
      </footer>
    </Stack>
  );
};

export { Layout };
