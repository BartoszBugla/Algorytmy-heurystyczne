import { lazy } from 'react';
import { createBrowserRouter } from 'react-router-dom';

import { Layout } from '@/common/components/Layout';

import { routes } from '.';

export const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      {
        path: routes.main(),
        Component: lazy(() => import('@/algorithms/views/MainPage')),
      },
      {
        path: routes.algorithmView(':id'),
        Component: lazy(() => import('@/algorithms/views/AlgorithmView/AlogrithmView')),
      },
      // {
      //   path: routes.functions(),
      //   Component: lazy(() => import('@/algorithms/views/ManageFunctions/ManageFunctions')),
      // },
      // {
      //   path: routes.algorithms(),
      //   Component: lazy(() => import('@/algorithms/views/ManageAlgorithms/ManageAlgorithms')),
      // },
    ],
  },
]);
