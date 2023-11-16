import { ChangeEvent, useState } from 'react';

import { Autocomplete, Button, Paper, Stack, TextField, Typography } from '@mui/material';

import { UploadInput } from '@/common/components/UploadInput';
import { useFunctionsApi } from '@/core/api';

const ManageFunctions = () => {
  const [selectedFunction, setSelectedFunction] = useState<string>('');

  const { functions, triggerFunctionMutation, uploadFunctionMutation, deleteFunctionMutation } =
    useFunctionsApi();

  const onUploadFunction = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target?.files?.[0];

    if (!file) return;

    uploadFunctionMutation.mutateAsync({ name: file.name, file });
  };

  const onFunctionTrigger = async () => {
    const { data } = await triggerFunctionMutation.mutateAsync({
      name: selectedFunction,
      args: [1, 2],
    });

    console.log(data);
  };

  return (
    <Stack direction='row' gap={2} justifyContent='center' alignItems='center' height='100vh'>
      <Paper>
        <Stack gap={2} padding={5}>
          <Typography variant='h4'>Function manager</Typography>
          <Autocomplete
            disablePortal
            onChange={(e, value) => value && setSelectedFunction(value)}
            value={selectedFunction}
            options={functions}
            sx={{ width: 300 }}
            renderInput={params => <TextField {...params} label='Function' size='small' />}
          />
          <UploadInput label='Upload Function' onChange={onUploadFunction} />

          <Button disabled={!selectedFunction} variant='contained' onClick={onFunctionTrigger}>
            Run function
          </Button>
          <Typography>{triggerFunctionMutation.data?.data}</Typography>
          <Button
            color='error'
            disabled={!selectedFunction}
            variant='outlined'
            onClick={() => deleteFunctionMutation.mutateAsync(selectedFunction)}
          >
            Delete function
          </Button>
        </Stack>
      </Paper>
    </Stack>
  );
};

export default ManageFunctions;
