import React from "react";
import {
  FormControl,
  FormHelperText,
  InputLabel,
  OutlinedInput,
} from "@mui/material";
import { Controller } from "react-hook-form";

const NomeInput = ({ control, errors, name }) => {
  return (
    <FormControl fullWidth>
      <Controller
        control={control}
        name="name"
        render={({ field: { value, onChange } }) => (
          <>
            <InputLabel htmlFor="name">Name *</InputLabel>
            <OutlinedInput
              disabled={name !== "" && name !== undefined}
              label="Name *"
              onChange={onChange}
              value={value}
            />
          </>
        )}
      />
      {errors.name ? (
        <FormHelperText id="validation-async-side" sx={{ color: "error.main" }}>
          {errors.name.message}
        </FormHelperText>
      ) : null}
    </FormControl>
  );
};

export default NomeInput;
