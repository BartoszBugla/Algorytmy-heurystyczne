import { AppBar, Button, IconButton, Link, Stack, Toolbar, Typography } from '@mui/material';

import { routes } from '@/core/router';

const Header = () => {
  return (
    <AppBar position='static'>
      <Toolbar>
        <IconButton
          size='large'
          edge='start'
          color='inherit'
          aria-label='menu'
          sx={{ mr: 2 }}
        ></IconButton>
        <Typography variant='h6' component='div' sx={{ flexGrow: 1 }}>
          Algorytmy metaheurystyczne
        </Typography>
        <Stack direction='row' spacing={2}>
          <Link component='a' href={routes.main()} color='inherit'>
            Algorithms list
          </Link>
          <Link component='a' href={routes.functions()} color='inherit'>
            Manage functions
          </Link>
        </Stack>
      </Toolbar>
    </AppBar>
  );
};

export { Header };
