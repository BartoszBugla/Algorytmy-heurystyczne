import { AppBar, Link, Stack, Toolbar } from '@mui/material';

import { routes } from '@/core/router';

const Header = () => {
  return (
    <AppBar position='static'>
      <Toolbar>
        <Stack direction='row' spacing={2}>
          <Link component='a' href={routes.main()} color='inherit'>
            Dashboard
          </Link>
        </Stack>
      </Toolbar>
    </AppBar>
  );
};

export { Header };
