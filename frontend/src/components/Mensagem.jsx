import React from "react";
import { Controller } from "react-hook-form";
import { FormControl, TextField, FormHelperText } from "@mui/material";

const Mensagem = ({ control, errors }) => {
  return (
    <FormControl fullWidth>
      <Controller
        control={control}
        name="description"
        render={({ field: { value, onChange } }) => (
          <TextField
            id="outlined-textarea"
            label="Message *"
            multiline
            onChange={onChange}
            placeholder="Message *"
            rows={4}
            value={value}
          />
        )}
      />
      {errors.description ? (
        <FormHelperText id="validation-async-side" sx={{ color: "error.main" }}>
          {errors.description.message}
        </FormHelperText>
      ) : null}
    </FormControl>
  );
};

export default Mensagem;
