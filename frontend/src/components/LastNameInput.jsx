import React from "react";
import { Controller } from "react-hook-form";
import {
  FormControl,
  InputLabel,
  OutlinedInput,
  FormHelperText,
} from "@mui/material";

function LastNameInput({ control, errors, lastName }) {
  return (
    <FormControl fullWidth>
      <Controller
        control={control}
        name="lastName"
        render={({ field: { value, onChange } }) => (
          <>
            <InputLabel htmlFor="lastName">Last Name *</InputLabel>
            <OutlinedInput
              disabled={lastName !== "" && lastName !== undefined}
              label="Last Name *"
              onChange={onChange}
              value={value}
            />
          </>
        )}
      />
      {errors.lastName ? (
        <FormHelperText
          id="validation-async-side"
          sx={{
            color: "error.main",
          }}
        >
          {errors.lastName.message}
        </FormHelperText>
      ) : null}
    </FormControl>
  );
}
export default LastNameInput;
