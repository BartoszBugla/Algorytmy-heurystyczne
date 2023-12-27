import { Grid, Link, List, ListItemText, Paper, Stack } from '@mui/material';

import { useAlgorithmsApi } from '@/core/api';
import { routes } from '@/core/router';

import ManageAlgorithms from '../views/ManageAlgorithms/ManageAlgorithms';
import ManageFunctions from '../views/ManageFunctions/ManageFunctions';

const AlgorithmsList = () => {
  const { allAlgoritmsQuery } = useAlgorithmsApi();

  return (
    <Grid container spacing={2}>
      <Grid item sm={6} width={'100%'}>
        <ManageAlgorithms />
      </Grid>

      <Grid item sm={6} width={'100%'}>
        <ManageFunctions />
      </Grid>

      <Grid item sm={12} width={'100%'}>
        <Paper sx={{ width: '100%', height: '100%' }}>
          <Stack padding={2}>
            <List>
              {allAlgoritmsQuery.data?.map(algorithm => (
                <ListItemText>
                  <Link component='a' href={routes.algorithmView(algorithm)}>
                    {algorithm}
                  </Link>
                </ListItemText>
              ))}

              {allAlgoritmsQuery.isLoading && <ListItemText>Loading...</ListItemText>}
              {allAlgoritmsQuery.isError && (
                <ListItemText>
                  No algorithms found, please open server on http://localhost:8000, then refresh
                  this page
                </ListItemText>
              )}
            </List>
          </Stack>
        </Paper>
      </Grid>
    </Grid>
  );
};

export { AlgorithmsList };
