import { type FC, useState, useCallback } from 'react';
import {
  TextField,
  Button,
  Paper,
  Typography,
  Stack,
  CircularProgress,
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import type { NoteCreate } from '../types/note';

interface NoteFormProps {
  onSubmit: (data: NoteCreate) => Promise<void>;
  creating: boolean;
}

export const NoteForm: FC<NoteFormProps> = ({ onSubmit, creating }) => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');

  const isValid = title.trim().length > 0 && content.trim().length > 0;

  const handleSubmit = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault();
      if (!isValid || creating) return;
      await onSubmit({ title: title.trim(), content: content.trim() });
      setTitle('');
      setContent('');
    },
    [title, content, isValid, creating, onSubmit],
  );

  return (
    <Paper sx={{ p: 3, mb: 3 }}>
      <Typography variant="h6" sx={{ mb: 2 }}>
        Create Note
      </Typography>
      <form onSubmit={handleSubmit}>
        <Stack spacing={2}>
          <TextField
            label="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            disabled={creating}
            fullWidth
            required
            size="small"
          />
          <TextField
            label="Content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            disabled={creating}
            fullWidth
            required
            multiline
            rows={3}
            size="small"
          />
          <Button
            type="submit"
            variant="contained"
            disabled={!isValid || creating}
            startIcon={creating ? <CircularProgress size={18} /> : <AddIcon />}
          >
            {creating ? 'Creating...' : 'Create Note'}
          </Button>
        </Stack>
      </form>
    </Paper>
  );
};
