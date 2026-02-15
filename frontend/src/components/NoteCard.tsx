import { memo, type FC } from 'react';
import { Card, CardContent, Typography } from '@mui/material';
import type { Note } from '../types/note';

interface NoteCardProps {
  note: Note;
}

const NoteCardInner: FC<NoteCardProps> = ({ note }) => {
  const preview =
    note.content.length > 150 ? `${note.content.slice(0, 150)}...` : note.content;

  const formattedDate = new Date(note.created_at).toLocaleString();

  return (
    <Card variant="outlined">
      <CardContent>
        <Typography variant="h6" component="h3" gutterBottom>
          {note.title}
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
          {preview}
        </Typography>
        <Typography variant="caption" color="text.disabled">
          {formattedDate}
        </Typography>
      </CardContent>
    </Card>
  );
};

export const NoteCard = memo(NoteCardInner);
NoteCard.displayName = 'NoteCard';
