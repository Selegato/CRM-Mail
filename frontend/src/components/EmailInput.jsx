import React from "react";
import { Controller } from "react-hook-form";
import {
  FormControl,
  FormHelperText,
  InputLabel,
  OutlinedInput,
} from "@mui/material";

const EmailInput = ({ control, errors, email }) => {
  return (
    <FormControl fullWidth>
      <Controller
        control={control}
        name="email"
        render={({ field: { value, onChange } }) => (
          <>
            <InputLabel htmlFor="email">E-mail *</InputLabel>
            <OutlinedInput
              disabled={email !== "" && email !== undefined}
              label="e-mail *"
              onChange={onChange}
              value={value}
            />
          </>
        )}
      />
      {errors.email ? (
        <FormHelperText id="validation-async-side" sx={{ color: "error.main" }}>
          {errors.email.message}
        </FormHelperText>
      ) : null}
    </FormControl>
  );
};

export default EmailInput;
