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
  const { id } = useParams<{ id: string }>();
  const { functions } = useFunctionsApi();
  const { metadataQuery, triggerAlgorithmMutation } = useAlgorithmsApi({ metadataId: id });
  const { data: metadata } = metadataQuery;

  const handleSubmit: SubmitHandler<typeof initialValues> = values => {
    if (id) triggerAlgorithmMutation.mutate({ name: id, ...values });
  };

  const { fields, append, remove } = useFieldArray({ name: 'domain', control: formProps.control });

  const { register } = formProps;

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
              renderInput={params => <TextField {...params} {...register('fun')} size='small' />}
            />
          </FormControl>

          <Typography variant='h6'>Domain</Typography>

          <Stack gap={2}>
            {fields.map((field, index) => (
              <Stack direction='row' alignItems='center' gap={2} key={field.id}>
                <Typography>Lower Bound</Typography>
                <TextField {...register(`domain.${index}.0`)} sx={{ width: 200 }} />
                <Typography>Upper Bound</Typography>
                <TextField {...register(`domain.${index}.1`)} sx={{ width: 200 }} />
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
              <>
                <Divider />
                <ListItem>
                  <Stack gap={3}>
                    <Typography>Name: {argument.name}</Typography>
                    <Typography>Description: {argument.description}</Typography>
                    <Typography>{`Range (${argument.lower_bound}:${argument.upper_bound})`}</Typography>
                    <FormControl>
                      <FormLabel>Value</FormLabel>
                      <TextField {...register(`params.${i}`)} sx={{ width: 200 }} />
                    </FormControl>
                  </Stack>
                </ListItem>
                <Divider />
              </>
            ))}
          </List>
          <Button type='submit'>Trigger</Button>
        </Stack>
      </form>
    </Paper>
  );
};

export default AlogrithmView;
