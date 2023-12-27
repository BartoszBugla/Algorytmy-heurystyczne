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

import { AlgorithmsList } from '@/algorithms/components/AlgorithmsList';
import { UploadInput } from '@/common/components/UploadInput';
import { useFunctionsApi } from '@/core/api';

const ManageFunctions = () => {
  const [selectedFunction, setSelectedFunction] = useState<string>('');
  const [functionArguments, setFunctionArguemnts] = useState<string>('');
  const { functions, triggerFunctionMutation, uploadFunctionMutation, deleteFunctionMutation } =
    useFunctionsApi();

  const onUploadFunction = async (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target?.files?.[0];

    if (!file) return;

    const { ok } = await uploadFunctionMutation.mutateAsync({ name: file.name, file });
    if (ok) setSelectedFunction(file.name.split('.')[0]);
  };

  const onFunctionTrigger = async () => {
    const parsedArgs = functionArguments.split(',').map(arg => Number(arg.trim()));

    triggerFunctionMutation.mutateAsync({
      name: selectedFunction,
      args: parsedArgs,
    });
  };

  const onFunctionDelete = async () => {
    const { ok } = await deleteFunctionMutation.mutateAsync(selectedFunction);
    if (ok) setSelectedFunction('');
  };

  return (
    <Stack direction='row' gap={2} justifyContent='center' alignItems='center' height='100vh'>
      <Paper>
        <AlgorithmsList />
      </Paper>
      <Paper>
        <Stack gap={2} padding={5}>
          <Typography variant='h4'>Function manager</Typography>
          <FormControl>
            <FormLabel>Function</FormLabel>

            <Stack direction='row' width='100%' gap={1} alignItems='center'>
              <Autocomplete
                disablePortal
                fullWidth
                onChange={(_, value) => value && setSelectedFunction(value)}
                value={selectedFunction}
                options={functions}
                renderInput={params => <TextField {...params} size='small' />}
              />
              <UploadInput onChange={onUploadFunction} />
            </Stack>
          </FormControl>

          <FormControl>
            <FormLabel>Function arguments</FormLabel>
            <TextField
              onChange={e => setFunctionArguemnts(e.target.value)}
              value={functionArguments}
              size='small'
            />
          </FormControl>

          <Button disabled={!selectedFunction} variant='contained' onClick={onFunctionTrigger}>
            Run function
          </Button>
          <Typography color='secondary'>
            Function Solution: {triggerFunctionMutation.data?.data}
          </Typography>
          <Button
            color='error'
            disabled={!selectedFunction}
            variant='outlined'
            onClick={onFunctionDelete}
          >
            Delete function
          </Button>
        </Stack>
      </Paper>
    </Stack>
  );
};

export default ManageFunctions;
