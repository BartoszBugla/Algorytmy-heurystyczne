import { Fragment } from 'react';
import { SubmitHandler, useFieldArray, useForm } from 'react-hook-form';
import { useParams } from 'react-router-dom';

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
  params: [] as number[][],
  domain: [[0, 0]] as number[][],
  fun: '',
};

const CONTAINER_MAX_WIDTH = 800;

const AlogrithmView = () => {
  const formProps = useForm({
    defaultValues: initialValues,
  });

  const { id } = useParams<{ id: string }>();

  const { functions } = useFunctionsApi();
  const { metadataQuery, triggerAlgorithmMutation, triggerAlgorithmOptunaMutation } =
    useAlgorithmsApi({ metadataId: id });
  const { data: metadata } = metadataQuery;

  const handleOptunaSubmit: SubmitHandler<typeof initialValues> = values => {
    if (id) triggerAlgorithmOptunaMutation.mutate({ name: id, ...values });

    enqueueSnackbar(`Algorithm with Optuna is running`, { variant: 'success' });
  };

  const handleSubmit: SubmitHandler<typeof initialValues> = values => {
    if (id) triggerAlgorithmMutation.mutate({ name: id, ...values });

    enqueueSnackbar(`Algorithm is running`, { variant: 'success' });
  };

  const { fields, append, remove } = useFieldArray({ name: 'domain', control: formProps.control });

  const { register } = formProps;

  if (metadataQuery.isLoading) return <Box>loading...</Box>;

  if (!metadataQuery.data)
    return (
      <Box>
        <Typography color='error'>Ouups it seems like this algorithm doesn't exist</Typography>
        <Link href={routes.main()}>Go back</Link>
      </Box>
    );

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
                <TextField {...register(`domain.${index}.0`, { valueAsNumber: true })} />
                <Typography color='text.secondary'>Upper Bound</Typography>
                <TextField {...register(`domain.${index}.1`, { valueAsNumber: true })} />
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
            {(metadata?.params_info || []).map((argument, i) => {
              const iterations =
                (formProps.watch(`params.${i}.1`) - formProps.watch(`params.${i}.0`)) /
                formProps.watch(`params.${i}.2`);

              return (
                <Fragment key={i}>
                  <Divider />
                  <ListItem>
                    <Stack gap={3}>
                      <Typography>Name: {argument.name}</Typography>
                      <Typography>Description: {argument.description}</Typography>
                      <Typography>{`Range (${argument.lower_bound}:${argument.upper_bound})`}</Typography>
                      <Typography color='error'>
                        {!!formProps.formState.errors?.params?.[i]?.length &&
                          `Invalid values in this section all fields are required, has to be in range  from ${argument.lower_bound} to ${argument.upper_bound}, step has to be positive and lower bound has to be lower than upper bound`}
                      </Typography>
                      <Stack gap={2} direction='row'>
                        <TextField
                          label='Lower bound'
                          {...register(`params.${i}.0`, {
                            valueAsNumber: true,
                            required: true,
                            validate: value =>
                              value <= argument.upper_bound &&
                              value >= argument.lower_bound &&
                              value < formProps.watch(`params.${i}.1`),
                          })}
                        />
                        <TextField
                          label='Upper bound'
                          {...register(`params.${i}.1`, {
                            valueAsNumber: true,
                            required: true,
                            validate: value =>
                              value <= argument.upper_bound &&
                              value >= argument.lower_bound &&
                              value > formProps.watch(`params.${i}.0`),
                          })}
                          sx={{ width: 200 }}
                        />
                        <TextField
                          label='Step'
                          min={0}
                          {...register(`params.${i}.2`, {
                            valueAsNumber: true,
                            required: true,
                            validate: value => value > 0,
                          })}
                          sx={{ width: 200 }}
                        />
                      </Stack>

                      {!formProps.formState.errors.params?.[i] &&
                        `Iterations: ${Math.floor(iterations)} `}
                    </Stack>
                  </ListItem>
                  <Divider />
                </Fragment>
              );
            })}
          </List>
          <Typography>
            The Algorithm will be run for all possible combinations of parameters: &nbsp;
            {formProps
              .watch()
              .params.reduce((acc, curr) => (acc * (curr[1] - curr[0])) / curr[2], 1)}{' '}
            times
          </Typography>

          <Button onClick={formProps.handleSubmit(handleOptunaSubmit)} variant='outlined'>
            Trigger Optuna
          </Button>
          <Button variant='contained' type='submit'>
            Trigger
          </Button>
        </Stack>
      </form>
    </Paper>
  );
};

export default AlogrithmView;
