import { HTMLAttributes } from 'react';

import { Upload } from '@mui/icons-material';
import { Button } from '@mui/material';

interface UploadInputProps extends HTMLAttributes<HTMLInputElement> {
  label: string;
}

const UploadInput = ({ label, ...props }: UploadInputProps) => {
  return (
    <Button variant='contained' component='label'>
      {label} <Upload />
      <input type='file' hidden {...props} />
    </Button>
  );
};

export { UploadInput };
