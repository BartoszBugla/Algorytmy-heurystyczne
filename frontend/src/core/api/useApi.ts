import { Api } from '.';

export const api = () =>
  new Api({
    baseUrl: 'http://localhost:8000',
  });
