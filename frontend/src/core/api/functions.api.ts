import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { api } from '.';

export const useFunctionsApi = () => {
  const queryClient = useQueryClient();

  const allFunctionsQuery = useQuery({
    queryKey: ['functions'],
    queryFn: () =>
      api()
        .functions.readAllFunctionsGet()
        .then(({ data }) => data),
  });

  const triggerFunctionMutation = useMutation({
    mutationFn: (payload: { name: string; args: number[] }) =>
      api().functions.triggerByNameFunctionsNameTriggerPost(payload.name, payload.args),

    onSuccess: () => {},
  });

  const uploadFunctionMutation = useMutation({
    mutationFn: (payload: { name: string; file: File }) =>
      api().functions.createFunctionsNamePost(payload.name, { file: payload.file }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['functions'] });
    },
  });

  const deleteFunctionMutation = useMutation({
    mutationFn: (payload: string) => api().functions.deleteByNameFunctionsNameDelete(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['functions'] });
    },
  });

  return {
    functions: allFunctionsQuery.data || [],
    allFunctionsQuery,
    triggerFunctionMutation,
    uploadFunctionMutation,
    deleteFunctionMutation,
  };
};
