import { lazy } from 'react';
import { createBrowserRouter } from 'react-router-dom';

import { Layout } from '@/common/components/Layout';

import { routes } from '.';

export const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      {
        path: '/',
        Component: lazy(() => import('@/algorithms/views/ManageFunctions/ManageFunctions')),
      },
      {
        path: routes.algorithmView(':id'),
        Component: lazy(() => import('@/algorithms/views/AlgorithmView/AlogrithmView')),
      },
    ],
  },
]);
