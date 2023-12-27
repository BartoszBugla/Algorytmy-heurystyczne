import { ChangeEvent, useState } from 'react';

import {
  Autocomplete,
  Button,
  FormControl,
  FormLabel,
  Paper,
  Stack,
  TextField,
  Typography,
} from '@mui/material';

import { UploadInput } from '@/common/components/UploadInput';
import { useAlgorithmsApi } from '@/core/api';

interface ManageAlgorithmsProps {}

const ManageAlgorithms = (props: ManageAlgorithmsProps) => {
  const [selectedAlgo, setSelectedAlgo] = useState<string>('');

  const { algoritms, uploadAlgoritmMutation, deleteAlgoritmMutation } = useAlgorithmsApi();

  const onUploadFunction = async (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target?.files?.[0];

    if (!file) return;

    const { ok } = await uploadAlgoritmMutation.mutateAsync({ name: file.name, file });
    if (ok) setSelectedAlgo(file.name.split('.')[0]);
  };

  const onFunctionDelete = async () => {
    const { ok } = await deleteAlgoritmMutation.mutateAsync({ name: selectedAlgo });
    if (ok) setSelectedAlgo('');
  };

  return (
    <Paper sx={{ width: '100%', height: '100%' }}>
      <Stack gap={2} padding={5}>
        <Typography variant='h4'>Algorithm manager</Typography>
        <FormControl>
          <FormLabel>Algorithm</FormLabel>

          <Stack direction='row' width='100%' gap={1} alignItems='center'>
            <Autocomplete
              disablePortal
              fullWidth
              onChange={(_, value) => value && setSelectedAlgo(value)}
              value={selectedAlgo}
              options={algoritms}
              renderInput={params => <TextField {...params} size='small' />}
            />
            <UploadInput onChange={onUploadFunction} />
          </Stack>
        </FormControl>

        <Button
          color='error'
          disabled={!selectedAlgo}
          variant='outlined'
          onClick={onFunctionDelete}
        >
          Delete Algorithm
        </Button>
      </Stack>
    </Paper>
  );
};

export default ManageAlgorithms;
