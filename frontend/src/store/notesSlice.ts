import { createSlice, createAsyncThunk, type PayloadAction } from '@reduxjs/toolkit';
import { apiClient } from '../api/client';
import type { Note, NoteCreate } from '../types/note';
import type { RootState } from './store';

interface NotesState {
  items: Note[];
  loading: boolean;
  creating: boolean;
  error: string | null;
  query: string;
}

const initialState: NotesState = {
  items: [],
  loading: false,
  creating: false,
  error: null,
  query: '',
};

// Fetch notes (with optional search query)
export const fetchNotes = createAsyncThunk<Note[], { q?: string } | void>(
  'notes/fetchNotes',
  async (args, { rejectWithValue }) => {
    try {
      const params = args && 'q' in args && args.q ? { q: args.q } : undefined;
      const response = await apiClient.get<Note[]>('/notes', { params });
      return response.data;
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to fetch notes';
      return rejectWithValue(message);
    }
  },
);

// Create a new note
export const createNote = createAsyncThunk<Note, NoteCreate>(
  'notes/createNote',
  async (data, { rejectWithValue }) => {
    try {
      const response = await apiClient.post<Note>('/notes', data);
      return response.data;
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to create note';
      return rejectWithValue(message);
    }
  },
);

const notesSlice = createSlice({
  name: 'notes',
  initialState,
  reducers: {
    setQuery(state, action: PayloadAction<string>) {
      state.query = action.payload;
    },
    clearError(state) {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    // fetchNotes
    builder
      .addCase(fetchNotes.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchNotes.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload;
      })
      .addCase(fetchNotes.rejected, (state, action) => {
        state.loading = false;
        state.error = (action.payload as string) ?? 'Failed to fetch notes';
      });

    // createNote
    builder
      .addCase(createNote.pending, (state) => {
        state.creating = true;
        state.error = null;
      })
      .addCase(createNote.fulfilled, (state, action) => {
        state.creating = false;
        state.items.push(action.payload);
      })
      .addCase(createNote.rejected, (state, action) => {
        state.creating = false;
        state.error = (action.payload as string) ?? 'Failed to create note';
      });
  },
});

export const { setQuery, clearError } = notesSlice.actions;
export const notesReducer = notesSlice.reducer;

// Selectors
export const selectNotes = (state: RootState) => state.notes.items;
export const selectNotesLoading = (state: RootState) => state.notes.loading;
export const selectNotesError = (state: RootState) => state.notes.error;
export const selectNotesQuery = (state: RootState) => state.notes.query;
export const selectIsCreating = (state: RootState) => state.notes.creating;
