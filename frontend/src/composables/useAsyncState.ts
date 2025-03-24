import { ref, shallowRef } from "vue";

export interface AsyncStateOptions<T> {
  immediate?: boolean;
  initialState?: T;
  onError?: (error: Error) => void;
  onSuccess?: (data: T) => void;
}

export function useAsyncState<T>(
  asyncFn: () => Promise<T>,
  options: AsyncStateOptions<T> = {},
) {
  const {
    immediate = true,
    initialState = undefined,
    onError,
    onSuccess,
  } = options;

  const state = shallowRef<T | undefined>(initialState);
  const error = ref<Error | null>(null);
  const loading = ref(false);

  async function execute() {
    loading.value = true;
    error.value = null;

    try {
      const data = await asyncFn();
      state.value = data;
      onSuccess?.(data);
      return data;
    } catch (err) {
      error.value = err as Error;
      onError?.(error.value);
      return Promise.reject(error.value);
    } finally {
      loading.value = false;
    }
  }

  if (immediate) {
    execute();
  }

  return {
    state,
    error,
    loading,
    execute,
  };
}
