import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { api } from '.';

export const useAlgorithmsApi = () => {
  const queryClient = useQueryClient();

  const allAlgoritmsQuery = useQuery({
    queryKey: ['algorithms'],
    queryFn: () =>
      api()
        .functions.readAllFunctionsGet()
        .then(({ data }) => data),
  });

  const uploadAlgoritmMutation = useMutation({
    mutationFn: (payload: { name: string; file: File }) =>
      api().functions.createFunctionsNamePost(payload.name, { file: payload.file }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['algorithms'] });
    },
  });

  const deleteAlgoritmMutation = useMutation({
    mutationFn: (payload: { name: string }) =>
      api().algorithms.deleteByNameAlgorithmsNameDelete(payload.name),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['algorithms'] });
    },
  });

  return {
    algoritms: allAlgoritmsQuery.data || [],
    allAlgoritmsQuery,
    uploadAlgoritmMutation,
    deleteAlgoritmMutation,
  };
};
