import { HTMLAttributes } from 'react';

import { PostAdd } from '@mui/icons-material';
import { IconButton } from '@mui/material';

interface UploadInputProps extends HTMLAttributes<HTMLInputElement> {}

const UploadInput = ({ ...props }: UploadInputProps) => {
  return (
    <IconButton component='label'>
      <PostAdd />
      <input type='file' hidden {...props} />
    </IconButton>
  );
};

export { UploadInput };
