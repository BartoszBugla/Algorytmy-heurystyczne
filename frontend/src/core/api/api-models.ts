/* eslint-disable */
/* tslint:disable */
/*
 * ---------------------------------------------------------------
 * ## THIS FILE WAS GENERATED VIA SWAGGER-TYPESCRIPT-API        ##
 * ##                                                           ##
 * ## AUTHOR: acacode                                           ##
 * ## SOURCE: https://github.com/acacode/swagger-typescript-api ##
 * ---------------------------------------------------------------
 */

/** AlgorithmMetadata */
export interface AlgorithmMetadata {
  /** Name */
  name: string;
  /** Params Info */
  params_info?: ParamInfo[] | null;
}

/** Body_create_algorithms__name__post */
export interface BodyCreateAlgorithmsNamePost {
  /**
   * File
   * @format binary
   */
  file: File;
}

/** Body_create_functions__name__post */
export interface BodyCreateFunctionsNamePost {
  /**
   * File
   * @format binary
   */
  file: File;
}

/** Body_trigger_algorithms__name__trigger_post */
export interface BodyTriggerAlgorithmsNameTriggerPost {
  /**
   * Domain
   * domain for all dimnensions example: [[-5.12, 5.12], [-5.12, 5.12]]]
   */
  domain: number[][];
  /**
   * Params
   * The parameters for the algorithm if you don't know them check the Parama Info of given algorithm
   */
  params: number[];
}

/** Body_trigger_multiple_tests_algorithms_trigger_multiple_tests_post */
export interface BodyTriggerMultipleTestsAlgorithmsTriggerMultipleTestsPost {
  /**
   * Names
   * The names of the algorithms to trigger
   */
  names: string[];
  /**
   * Domain
   * domain for all dimnensions example: [[-5.12, 5.12], [-5.12, 5.12]]]
   */
  domain: number[][];
  /**
   * Params
   * The parameters for the algorithm in format  List of of Lists of parameters datafor next algorithms in order[[range_start, range_end, 'int'/'float'], [], etc.,where next lists are the values for next parameters, example:[[[3,100,'int'],[20, 300,'int']],[[3,100,'int'],[20, 300,'int']]]
   */
  params: any[][][];
  /**
   * Trials Count
   * Number of trials for each algorithm
   */
  trials_count: number;
}

/** Body_trigger_optuna_test_algorithms__name__trigger_optuna_test_post */
export interface BodyTriggerOptunaTestAlgorithmsNameTriggerOptunaTestPost {
  /**
   * Domain
   * domain for all dimnensions example: [[-5.12, 5.12], [-5.12, 5.12]]
   */
  domain: number[][];
  /**
   * Params
   * The parameters for the algorithm in format [[range_start, range_end, int/float], [], etc.,where next lists are the values for next parameters, example: [[3,100,'int'],[20, 300,'int']]
   */
  params: any[][];
  /**
   * Trials Count
   * Number of trials for algorithm
   */
  trials_count: number;
}

/** Body_trigger_test_algorithms__name__trigger_test_post */
export interface BodyTriggerTestAlgorithmsNameTriggerTestPost {
  /**
   * Domain
   * domain for all dimnensions example: [[-5.12, 5.12], [-5.12, 5.12]]]
   */
  domain: number[][];
  /**
   * Params
   * The parameters for the algorithm in format [[range_start, range_end, step], [], etc.,where next lists are the values for next parameters if you don't know the order of paramscheck algorithm's metadata
   */
  params: number[][];
}

/** HTTPValidationError */
export interface HTTPValidationError {
  /** Detail */
  detail?: ValidationError[];
}

/** ParamInfo */
export interface ParamInfo {
  /** Name */
  name: string;
  /** Description */
  description: string;
  /** Upper Bound */
  upper_bound: number;
  /** Lower Bound */
  lower_bound: number;
}

/** ValidationError */
export interface ValidationError {
  /** Location */
  loc: (string | number)[];
  /** Message */
  msg: string;
  /** Error Type */
  type: string;
}

export type QueryParamsType = Record<string | number, any>;
export type ResponseFormat = keyof Omit<Body, 'body' | 'bodyUsed'>;

export interface FullRequestParams extends Omit<RequestInit, 'body'> {
  /** set parameter to `true` for call `securityWorker` for this request */
  secure?: boolean;
  /** request path */
  path: string;
  /** content type of request body */
  type?: ContentType;
  /** query params */
  query?: QueryParamsType;
  /** format of response (i.e. response.json() -> format: "json") */
  format?: ResponseFormat;
  /** request body */
  body?: unknown;
  /** base url */
  baseUrl?: string;
  /** request cancellation token */
  cancelToken?: CancelToken;
}

export type RequestParams = Omit<FullRequestParams, 'body' | 'method' | 'query' | 'path'>;

export interface ApiConfig<SecurityDataType = unknown> {
  baseUrl?: string;
  baseApiParams?: Omit<RequestParams, 'baseUrl' | 'cancelToken' | 'signal'>;
  securityWorker?: (
    securityData: SecurityDataType | null,
  ) => Promise<RequestParams | void> | RequestParams | void;
  customFetch?: typeof fetch;
}

export interface HttpResponse<D extends unknown, E extends unknown = unknown> extends Response {
  data: D;
  error: E;
}

type CancelToken = Symbol | string | number;

export enum ContentType {
  Json = 'application/json',
  FormData = 'multipart/form-data',
  UrlEncoded = 'application/x-www-form-urlencoded',
  Text = 'text/plain',
}

export class HttpClient<SecurityDataType = unknown> {
  public baseUrl: string = '';
  private securityData: SecurityDataType | null = null;
  private securityWorker?: ApiConfig<SecurityDataType>['securityWorker'];
  private abortControllers = new Map<CancelToken, AbortController>();
  private customFetch = (...fetchParams: Parameters<typeof fetch>) => fetch(...fetchParams);

  private baseApiParams: RequestParams = {
    credentials: 'same-origin',
    headers: {},
    redirect: 'follow',
    referrerPolicy: 'no-referrer',
  };

  constructor(apiConfig: ApiConfig<SecurityDataType> = {}) {
    Object.assign(this, apiConfig);
  }

  public setSecurityData = (data: SecurityDataType | null) => {
    this.securityData = data;
  };

  protected encodeQueryParam(key: string, value: any) {
    const encodedKey = encodeURIComponent(key);
    return `${encodedKey}=${encodeURIComponent(typeof value === 'number' ? value : `${value}`)}`;
  }

  protected addQueryParam(query: QueryParamsType, key: string) {
    return this.encodeQueryParam(key, query[key]);
  }

  protected addArrayQueryParam(query: QueryParamsType, key: string) {
    const value = query[key];
    return value.map((v: any) => this.encodeQueryParam(key, v)).join('&');
  }

  protected toQueryString(rawQuery?: QueryParamsType): string {
    const query = rawQuery || {};
    const keys = Object.keys(query).filter(key => 'undefined' !== typeof query[key]);
    return keys
      .map(key =>
        Array.isArray(query[key])
          ? this.addArrayQueryParam(query, key)
          : this.addQueryParam(query, key),
      )
      .join('&');
  }

  protected addQueryParams(rawQuery?: QueryParamsType): string {
    const queryString = this.toQueryString(rawQuery);
    return queryString ? `?${queryString}` : '';
  }

  private contentFormatters: Record<ContentType, (input: any) => any> = {
    [ContentType.Json]: (input: any) =>
      input !== null && (typeof input === 'object' || typeof input === 'string')
        ? JSON.stringify(input)
        : input,
    [ContentType.Text]: (input: any) =>
      input !== null && typeof input !== 'string' ? JSON.stringify(input) : input,
    [ContentType.FormData]: (input: any) =>
      Object.keys(input || {}).reduce((formData, key) => {
        const property = input[key];
        formData.append(
          key,
          property instanceof Blob
            ? property
            : typeof property === 'object' && property !== null
            ? JSON.stringify(property)
            : `${property}`,
        );
        return formData;
      }, new FormData()),
    [ContentType.UrlEncoded]: (input: any) => this.toQueryString(input),
  };

  protected mergeRequestParams(params1: RequestParams, params2?: RequestParams): RequestParams {
    return {
      ...this.baseApiParams,
      ...params1,
      ...(params2 || {}),
      headers: {
        ...(this.baseApiParams.headers || {}),
        ...(params1.headers || {}),
        ...((params2 && params2.headers) || {}),
      },
    };
  }

  protected createAbortSignal = (cancelToken: CancelToken): AbortSignal | undefined => {
    if (this.abortControllers.has(cancelToken)) {
      const abortController = this.abortControllers.get(cancelToken);
      if (abortController) {
        return abortController.signal;
      }
      return void 0;
    }

    const abortController = new AbortController();
    this.abortControllers.set(cancelToken, abortController);
    return abortController.signal;
  };

  public abortRequest = (cancelToken: CancelToken) => {
    const abortController = this.abortControllers.get(cancelToken);

    if (abortController) {
      abortController.abort();
      this.abortControllers.delete(cancelToken);
    }
  };

  public request = async <T = any, E = any>(
    { body, secure, path, type, query, format, baseUrl, cancelToken, ...params }: FullRequestParams,
  ): Promise<HttpResponse<T, E>> => {
    const secureParams =
      ((typeof secure === 'boolean' ? secure : this.baseApiParams.secure) &&
        this.securityWorker &&
        (await this.securityWorker(this.securityData))) ||
      {};
    const requestParams = this.mergeRequestParams(params, secureParams);
    const queryString = query && this.toQueryString(query);
    const payloadFormatter = this.contentFormatters[type || ContentType.Json];
    const responseFormat = format || requestParams.format;

    return this.customFetch(
      `${baseUrl || this.baseUrl || ''}${path}${queryString ? `?${queryString}` : ''}`,
      {
        ...requestParams,
        headers: {
          ...(requestParams.headers || {}),
          ...(type && type !== ContentType.FormData ? { 'Content-Type': type } : {}),
        },
        signal: (cancelToken ? this.createAbortSignal(cancelToken) : requestParams.signal) || null,
        body: typeof body === 'undefined' || body === null ? null : payloadFormatter(body),
      },
    ).then(async response => {
      const r = response as HttpResponse<T, E>;
      r.data = null as unknown as T;
      r.error = null as unknown as E;

      const data = !responseFormat
        ? r
        : await response[responseFormat]()
            .then(data => {
              if (r.ok) {
                r.data = data;
              } else {
                r.error = data;
              }
              return r;
            })
            .catch(e => {
              r.error = e;
              return r;
            });

      if (cancelToken) {
        this.abortControllers.delete(cancelToken);
      }

      if (!response.ok) throw data;
      return data;
    });
  };
}

/**
 * @title Algorytmy metaherustyczne API
 * @version 1.0.0
 *
 * Algorytmy metaherustyczne API
 */
export class Api<SecurityDataType extends unknown> extends HttpClient<SecurityDataType> {
  functions = {
    /**
     * @description Trigger function by name.
     *
     * @tags functions
     * @name TriggerByNameFunctionsNameTriggerPost
     * @summary Trigger By Name
     * @request POST:/functions/{name}/trigger
     */
    triggerByNameFunctionsNameTriggerPost: (
      name: string,
      data: number[],
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/functions/${name}/trigger`,
        method: 'POST',
        body: data,
        type: ContentType.Json,
        format: 'json',
        ...params,
      }),

    /**
     * @description Get all functions
     *
     * @tags functions
     * @name ReadAllFunctionsGet
     * @summary Read All
     * @request GET:/functions/
     */
    readAllFunctionsGet: (params: RequestParams = {}) =>
      this.request<string[], any>({
        path: `/functions/`,
        method: 'GET',
        format: 'json',
        ...params,
      }),

    /**
     * No description
     *
     * @tags functions
     * @name CreateFunctionsNamePost
     * @summary Create
     * @request POST:/functions/{name}
     */
    createFunctionsNamePost: (
      name: string,
      data: BodyCreateFunctionsNamePost,
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/functions/${name}`,
        method: 'POST',
        body: data,
        type: ContentType.FormData,
        format: 'json',
        ...params,
      }),

    /**
     * No description
     *
     * @tags functions
     * @name DeleteByNameFunctionsNameDelete
     * @summary Delete By Name
     * @request DELETE:/functions/{name}
     */
    deleteByNameFunctionsNameDelete: (name: string, params: RequestParams = {}) =>
      this.request<any, HTTPValidationError>({
        path: `/functions/${name}`,
        method: 'DELETE',
        format: 'json',
        ...params,
      }),
  };
  storage = {
    /**
     * No description
     *
     * @tags storage
     * @name GetAllFoldersStorageGet
     * @summary Get All Folders
     * @request GET:/storage/
     */
    getAllFoldersStorageGet: (params: RequestParams = {}) =>
      this.request<any, any>({
        path: `/storage/`,
        method: 'GET',
        format: 'json',
        ...params,
      }),
  };
  algorithms = {
    /**
     * No description
     *
     * @tags algorithms
     * @name TriggerAlgorithmsNameTriggerPost
     * @summary Trigger
     * @request POST:/algorithms/{name}/trigger
     */
    triggerAlgorithmsNameTriggerPost: (
      name: string,
      query: {
        /**
         * Fun
         * The name of the function to use
         */
        fun: string;
      },
      data: BodyTriggerAlgorithmsNameTriggerPost,
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/algorithms/${name}/trigger`,
        method: 'POST',
        query: query,
        body: data,
        type: ContentType.Json,
        format: 'json',
        ...params,
      }),

    /**
     * No description
     *
     * @tags algorithms
     * @name TriggerTestAlgorithmsNameTriggerTestPost
     * @summary Trigger Test
     * @request POST:/algorithms/{name}/trigger_test
     */
    triggerTestAlgorithmsNameTriggerTestPost: (
      name: string,
      query: {
        /**
         * Fun
         * The name of the function to use
         */
        fun: string;
      },
      data: BodyTriggerTestAlgorithmsNameTriggerTestPost,
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/algorithms/${name}/trigger_test`,
        method: 'POST',
        query: query,
        body: data,
        type: ContentType.Json,
        format: 'json',
        ...params,
      }),

    /**
     * No description
     *
     * @tags algorithms
     * @name TriggerOptunaTestAlgorithmsNameTriggerOptunaTestPost
     * @summary Trigger Optuna Test
     * @request POST:/algorithms/{name}/trigger_optuna_test
     */
    triggerOptunaTestAlgorithmsNameTriggerOptunaTestPost: (
      name: string,
      query: {
        /**
         * Fun
         * The name of the function to use
         */
        fun: string;
      },
      data: BodyTriggerOptunaTestAlgorithmsNameTriggerOptunaTestPost,
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/algorithms/${name}/trigger_optuna_test`,
        method: 'POST',
        query: query,
        body: data,
        type: ContentType.Json,
        format: 'json',
        ...params,
      }),

    /**
     * No description
     *
     * @tags algorithms
     * @name TriggerMultipleTestsAlgorithmsTriggerMultipleTestsPost
     * @summary Trigger Multiple Tests
     * @request POST:/algorithms/trigger_multiple_tests
     */
    triggerMultipleTestsAlgorithmsTriggerMultipleTestsPost: (
      query: {
        /**
         * Fun
         * The name of the function to use
         */
        fun: string;
      },
      data: BodyTriggerMultipleTestsAlgorithmsTriggerMultipleTestsPost,
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/algorithms/trigger_multiple_tests`,
        method: 'POST',
        query: query,
        body: data,
        type: ContentType.Json,
        format: 'json',
        ...params,
      }),

    /**
     * No description
     *
     * @tags algorithms
     * @name MetadataAlgorithmsNameGet
     * @summary Metadata
     * @request GET:/algorithms/{name}
     */
    metadataAlgorithmsNameGet: (name: string, params: RequestParams = {}) =>
      this.request<AlgorithmMetadata, HTTPValidationError>({
        path: `/algorithms/${name}`,
        method: 'GET',
        format: 'json',
        ...params,
      }),

    /**
     * No description
     *
     * @tags algorithms
     * @name CreateAlgorithmsNamePost
     * @summary Create
     * @request POST:/algorithms/{name}
     */
    createAlgorithmsNamePost: (
      name: string,
      data: BodyCreateAlgorithmsNamePost,
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/algorithms/${name}`,
        method: 'POST',
        body: data,
        type: ContentType.FormData,
        format: 'json',
        ...params,
      }),

    /**
     * No description
     *
     * @tags algorithms
     * @name DeleteByNameAlgorithmsNameDelete
     * @summary Delete By Name
     * @request DELETE:/algorithms/{name}
     */
    deleteByNameAlgorithmsNameDelete: (name: string, params: RequestParams = {}) =>
      this.request<any, HTTPValidationError>({
        path: `/algorithms/${name}`,
        method: 'DELETE',
        format: 'json',
        ...params,
      }),

    /**
     * No description
     *
     * @tags algorithms
     * @name ReadAllAlgorithmsGet
     * @summary Read All
     * @request GET:/algorithms/
     */
    readAllAlgorithmsGet: (params: RequestParams = {}) =>
      this.request<string[], any>({
        path: `/algorithms/`,
        method: 'GET',
        format: 'json',
        ...params,
      }),
  };
}
