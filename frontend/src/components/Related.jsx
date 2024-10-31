import React from "react";
import { Controller } from "react-hook-form";
import {
  FormControl,
  InputLabel,
  OutlinedInput,
  FormHelperText,
  Select,
  MenuItem,
} from "@mui/material";

const Related = ({ control, errors, related }) => {
  return (
    <FormControl fullWidth>
      <Controller
        control={control}
        name="contactRelatedTo"
        render={({ field: { value, onChange } }) => (
          <>
            <InputLabel id="relatedToFieldLabel">Related *</InputLabel>
            <Select
              id="relatedToField"
              input={<OutlinedInput label="Related a *" />}
              labelId="reasonToFieldLabel"
              onChange={onChange}
              value={value}
            >
              {related.map((related, index) => (
                <MenuItem key={index} value={related}>
                  {related}
                </MenuItem>
              ))}
            </Select>
          </>
        )}
      />
      {errors.contactRelatedTo ? (
        <FormHelperText id="validation-async-side" sx={{ color: "error.main" }}>
          {errors.contactRelatedTo.message}
        </FormHelperText>
      ) : null}
    </FormControl>
  );
};

export default Related;
