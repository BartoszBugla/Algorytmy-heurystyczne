export const BASE = '/Algorytmy-heurystyczne';

export const routes = {
  main: () => `${BASE}/`,
  algorithmView: (name: string) => `${BASE}/algorithms/${name}`,
  functions: () => `${BASE}/functions`,
  algorithms: () => `${BASE}/algorithms`,
};
