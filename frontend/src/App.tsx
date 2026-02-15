import { useCallback, type FC } from 'react';
import { useAppDispatch, useAppSelector } from './store/hooks';
import {
  fetchNotes,
  createNote,
  setQuery,
  selectNotesLoading,
  selectIsCreating,
} from './store/notesSlice';
import type { NoteCreate } from './types/note';
import { Layout } from './components/Layout';
import { SearchBar } from './components/SearchBar';
import { NoteForm } from './components/NoteForm';
import { NoteList } from './components/NoteList';

export const App: FC = () => {
  const dispatch = useAppDispatch();
  const loading = useAppSelector(selectNotesLoading);
  const creating = useAppSelector(selectIsCreating);

  const handleSearch = useCallback(
    (query: string) => {
      dispatch(setQuery(query));
      dispatch(fetchNotes(query ? { q: query } : undefined));
    },
    [dispatch],
  );

  const handleCreate = useCallback(
    async (data: NoteCreate) => {
      const result = await dispatch(createNote(data));
      if (createNote.fulfilled.match(result)) {
        // Re-fetch to ensure consistency with server
        dispatch(fetchNotes());
      }
    },
    [dispatch],
  );

  return (
    <Layout>
      <SearchBar onSearch={handleSearch} loading={loading} />
      <NoteForm onSubmit={handleCreate} creating={creating} />
      <NoteList />
    </Layout>
  );
};
