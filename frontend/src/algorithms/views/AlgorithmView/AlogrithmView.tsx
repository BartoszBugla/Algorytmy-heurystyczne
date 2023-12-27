import { Fragment, useEffect } from 'react';
import { SubmitHandler, useFieldArray, useForm } from 'react-hook-form';
import { useSearchParams } from 'react-router-dom';

import { AddCircleOutlineRounded, RemoveCircleOutlineRounded } from '@mui/icons-material';
import {
  Autocomplete,
  Box,
  Button,
  Divider,
  FormControl,
  FormLabel,
  IconButton,
  Link,
  List,
  ListItem,
  Paper,
  Stack,
  TextField,
  Typography,
} from '@mui/material';
import { enqueueSnackbar } from 'notistack';

import { useAlgorithmsApi, useFunctionsApi } from '@/core/api';
import { routes } from '@/core/router';

const initialValues = {
  params: [] as number[],
  domain: [[0, 0]] as number[][],
  fun: '',
};

const CONTAINER_MAX_WIDTH = 800;

const AlogrithmView = () => {
  const formProps = useForm({
    defaultValues: initialValues,
  });

  const [searchParams] = useSearchParams();
  const id = searchParams.get('id') || '';
  const { functions } = useFunctionsApi();
  const { metadataQuery, triggerAlgorithmMutation } = useAlgorithmsApi({ metadataId: id });
  const { data: metadata } = metadataQuery;

  const handleSubmit: SubmitHandler<typeof initialValues> = values => {
    if (id) triggerAlgorithmMutation.mutate({ name: id, ...values });
  };

  const { fields, append, remove } = useFieldArray({ name: 'domain', control: formProps.control });

  const { register } = formProps;

  useEffect(() => {
    if (triggerAlgorithmMutation.isSuccess) {
      enqueueSnackbar(`Result is ${triggerAlgorithmMutation.data.data}`, { variant: 'success' });
    }
  }, [triggerAlgorithmMutation.data, triggerAlgorithmMutation.isSuccess]);
  if (metadataQuery.isLoading) return <Box>loading...</Box>;

  if (!metadataQuery.data)
    return (
      <Box>
        <Typography color='error'>Ouups it seems like this algorithm doesn't exist</Typography>
        <Link href={routes.main()}>Go back</Link>
      </Box>
    );

  console.log(formProps.formState.errors);
  return (
    <Paper sx={{ maxWidth: CONTAINER_MAX_WIDTH, width: '100%', margin: 'auto', padding: '16px' }}>
      <form onSubmit={formProps.handleSubmit(handleSubmit)}>
        <Stack gap={3}>
          <Link href={routes.main()}>Go back</Link>
          <Typography variant='h2'>{metadata?.name}</Typography>
          <FormControl>
            <FormLabel>Function name</FormLabel>
            <Autocomplete
              disablePortal
              fullWidth
              options={functions}
              renderInput={params => (
                <TextField {...params} {...register('fun', { required: true })} size='small' />
              )}
            />
          </FormControl>

          <Typography variant='h6'>Domain</Typography>

          <Stack gap={2}>
            {fields.map((field, index) => (
              <Stack direction='row' alignItems='center' gap={2} key={field.id}>
                <Typography color='text.secondary'>Lower Bound</Typography>
                <TextField
                  type='number'
                  {...register(`domain.${index}.0`, { valueAsNumber: true })}
                />
                <Typography color='text.secondary'>Upper Bound</Typography>
                <TextField
                  type='number'
                  {...register(`domain.${index}.1`, { valueAsNumber: true })}
                />
                {index > 0 && <RemoveCircleOutlineRounded onClick={() => remove(index)} />}
              </Stack>
            ))}
          </Stack>
          <Box>
            <IconButton onClick={() => append([[0, 0]])}>
              <AddCircleOutlineRounded />
            </IconButton>
          </Box>

          <Typography variant='h6'>Params</Typography>
          <List>
            {(metadata?.params_info || []).map((argument, i) => (
              <Fragment key={i}>
                <Divider />
                <ListItem>
                  <Stack gap={3}>
                    <Typography>Name: {argument.name}</Typography>
                    <Typography>Description: {argument.description}</Typography>
                    <Typography>{`Range (${argument.lower_bound}:${argument.upper_bound})`}</Typography>
                    <FormControl>
                      <FormLabel>Value</FormLabel>
                      <TextField
                        inputProps={{
                          type: 'number',
                        }}
                        {...register(`params.${i}`, {
                          valueAsNumber: true,
                          required: true,
                        })}
                        sx={{ width: 200 }}
                      />
                    </FormControl>
                  </Stack>
                </ListItem>
                <Divider />
              </Fragment>
            ))}
          </List>
          <Button disabled={!formProps.formState.isValid} type='submit'>
            Trigger
          </Button>
        </Stack>
      </form>
    </Paper>
  );
};

export default AlogrithmView;
