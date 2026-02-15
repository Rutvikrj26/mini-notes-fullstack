import { type FC, useState, useCallback } from 'react';
import { TextField, Button, Stack } from '@mui/material';
import { Search as SearchIcon, Clear as ClearIcon } from '@mui/icons-material';

interface SearchBarProps {
  onSearch: (query: string) => void;
  loading: boolean;
}

export const SearchBar: FC<SearchBarProps> = ({ onSearch, loading }) => {
  const [input, setInput] = useState('');

  const handleSearch = useCallback(() => {
    onSearch(input.trim());
  }, [input, onSearch]);

  const handleClear = useCallback(() => {
    setInput('');
    onSearch('');
  }, [onSearch]);

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      if (e.key === 'Enter') {
        handleSearch();
      }
    },
    [handleSearch],
  );

  return (
    <Stack direction="row" spacing={1} sx={{ mb: 3 }}>
      <TextField
        fullWidth
        size="small"
        placeholder="Search notes..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={loading}
        slotProps={{
          input: {
            startAdornment: <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />,
          },
        }}
      />
      <Button variant="contained" onClick={handleSearch} disabled={loading}>
        Search
      </Button>
      {input && (
        <Button variant="outlined" onClick={handleClear} startIcon={<ClearIcon />}>
          Clear
        </Button>
      )}
    </Stack>
  );
};
