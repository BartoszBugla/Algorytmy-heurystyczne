import { Link, List, ListItemText, Stack } from '@mui/material';

import { useAlgorithmsApi } from '@/core/api';
import { routes } from '@/core/router';

const AlgorithmsList = () => {
  const { allAlgoritmsQuery } = useAlgorithmsApi();

  return (
    <Stack>
      <List>
        {allAlgoritmsQuery.data?.map(algorithm => (
          <ListItemText>
            <Link href={routes.algorithmView(algorithm)}>{algorithm}</Link>
          </ListItemText>
        ))}
      </List>
    </Stack>
  );
};

export { AlgorithmsList };
