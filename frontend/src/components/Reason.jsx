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

const Reason = ({ control, errors, reason }) => {
  return (
    <FormControl fullWidth>
      <Controller
        control={control}
        name="contactReason"
        render={({ field: { value, onChange } }) => (
          <>
            <InputLabel id="reasonToFieldLabel">Reason *</InputLabel>
            <Select
              id="reasonToField"
              input={<OutlinedInput label="Reason *" />}
              labelId="reasonToFieldLabel"
              onChange={onChange}
              value={value}
            >
              {reason.map((reason, index) => (
                <MenuItem key={index} value={reason}>
                  {reason}
                </MenuItem>
              ))}
            </Select>
          </>
        )}
      />
      {errors.contactReason ? (
        <FormHelperText id="validation-async-side" sx={{ color: "error.main" }}>
          {errors.contactReason.message}
        </FormHelperText>
      ) : null}
    </FormControl>
  );
};

export default Reason;
