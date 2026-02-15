import { type FC, useEffect } from 'react';
import {
  Stack,
  Typography,
  CircularProgress,
  Alert,
  Box,
} from '@mui/material';
import { useAppSelector, useAppDispatch } from '../store/hooks';
import {
  selectNotes,
  selectNotesLoading,
  selectNotesError,
  selectNotesQuery,
  fetchNotes,
  clearError,
} from '../store/notesSlice';
import { NoteCard } from './NoteCard';

export const NoteList: FC = () => {
  const dispatch = useAppDispatch();
  const notes = useAppSelector(selectNotes);
  const loading = useAppSelector(selectNotesLoading);
  const error = useAppSelector(selectNotesError);
  const query = useAppSelector(selectNotesQuery);

  useEffect(() => {
    dispatch(fetchNotes());
  }, [dispatch]);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Stack spacing={2}>
      {error && (
        <Alert severity="error" onClose={() => dispatch(clearError())}>
          {error}
        </Alert>
      )}

      {!loading && notes.length === 0 && (
        <Typography variant="body1" color="text.secondary" align="center" sx={{ py: 4 }}>
          {query ? 'No notes match your search.' : 'No notes yet. Create one above!'}
        </Typography>
      )}

      {notes.map((note) => (
        <NoteCard key={note.id} note={note} />
      ))}
    </Stack>
  );
};
