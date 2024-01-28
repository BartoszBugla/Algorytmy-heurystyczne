import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { api } from '.';

interface UseAlgorithmsApiOptions {
  enableGetAll?: boolean;
  metadataId?: string;
}

export const useAlgorithmsApi = ({ enableGetAll, metadataId }: UseAlgorithmsApiOptions = {}) => {
  const queryClient = useQueryClient();

  const allAlgoritmsQuery = useQuery({
    queryKey: ['algorithms'],
    queryFn: () =>
      api()
        .algorithms.readAllAlgorithmsGet()
        .then(({ data }) => data),
    enabled: enableGetAll,
  });

  const metadataQuery = useQuery({
    queryKey: ['algorithms', metadataId],
    queryFn: () =>
      api()
        .algorithms.metadataAlgorithmsNameGet(metadataId || '')
        .then(({ data }) => data),
    enabled: !!metadataId,
  });

  const uploadAlgoritmMutation = useMutation({
    mutationFn: (payload: { name: string; file: File }) =>
      api().algorithms.createAlgorithmsNamePost(payload.name, { file: payload.file }),
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

  const triggerAlgorithmMutation = useMutation({
    mutationFn: ({
      name,
      fun,
      domain,
      params,
    }: {
      name: string;
      fun: string;
      domain: number[][];
      params: number[][];
    }) =>
      api().algorithms.triggerTestAlgorithmsNameTriggerTestPost(name, { fun }, { domain, params }),
    onSuccess: () => {},
  });

  const triggerAlgorithmOptunaMutation = useMutation({
    mutationFn: ({
      name,
      fun,
      domain,
      params,
    }: {
      name: string;
      fun: string;
      domain: number[][];
      params: number[][];
    }) =>
      api().algorithms.triggerOptunaTestAlgorithmsNameTriggerOptunaTestPost(
        name,
        { fun },
        { domain, params, trials_count: 30 },
      ),
    onSuccess: () => {},
  });

  const triggerMultiple = useMutation({
    mutationFn: ({
      names,
      fun,
      domain,
      params,
      trials_count,
    }: {
      names: string[];
      fun: string;
      domain: number[][];
      params: number[][][];
      trials_count: number;
    }) =>
      api().algorithms.triggerMultipleTestsAlgorithmsTriggerMultipleTestsPost(
        { fun },
        {
          names,
          domain,
          params: params.map(data => data.map(nextData => [...nextData, 'int'])),
          trials_count,
        },
      ),
    onSuccess: () => {},
  });

  return {
    algoritms: allAlgoritmsQuery.data || [],
    allAlgoritmsQuery,
    uploadAlgoritmMutation,
    metadataQuery,
    deleteAlgoritmMutation,
    triggerAlgorithmMutation,
    triggerAlgorithmOptunaMutation,
    triggerMultiple,
  };
};
