import { Link as RouterLink } from 'react-router-dom';

import { Link, List, ListItemText, Paper, Stack } from '@mui/material';

import { useAlgorithmsApi } from '@/core/api';
import { routes } from '@/core/router';

const AlgorithmsList = () => {
  const { allAlgoritmsQuery } = useAlgorithmsApi();

  return (
    <Paper sx={{ width: '100%', height: '100%' }}>
      <Stack padding={2}>
        <List>
          {allAlgoritmsQuery.data?.map(algorithm => (
            <ListItemText>
              <Link component='a' href={`${routes.algorithmView()}?id=${algorithm}`}>
                {algorithm}
              </Link>
            </ListItemText>
          ))}

          {allAlgoritmsQuery.isLoading && <ListItemText>Loading...</ListItemText>}
          {allAlgoritmsQuery.isError && (
            <ListItemText>
              No algorithms found, please open server on http://localhost:8000, then refresh this
              page
            </ListItemText>
          )}
        </List>
      </Stack>
    </Paper>
  );
};

export { AlgorithmsList };
