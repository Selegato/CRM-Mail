import React from "react";
import { Controller } from "react-hook-form";
import {
  FormControl,
  FormHelperText,
  InputLabel,
  OutlinedInput,
} from "@mui/material";
import InputMask from "react-input-mask";

const PhoneInput = ({ control, errors, phone }) => {
  return (
    <FormControl fullWidth>
      <Controller
        control={control}
        name="phone"
        render={({ field: { value, onChange } }) => (
          <>
            <InputLabel htmlFor="phone">Phone</InputLabel>
            <InputMask
              disabled={phone !== "" && phone !== undefined}
              label="Phone"
              mask="(99) 9999-9999"
              maskChar={null}
              onChange={onChange}
              value={value}
            >
              {(inputProps) => (
                <OutlinedInput
                  {...inputProps}
                  disabled={phone !== "" && phone !== undefined}
                  type="tel"
                />
              )}
            </InputMask>
          </>
        )}
      />
      {errors.phone ? (
        <FormHelperText id="validation-async-side" sx={{ color: "error.main" }}>
          {errors.phone.message}
        </FormHelperText>
      ) : null}
    </FormControl>
  );
};

export default PhoneInput;
