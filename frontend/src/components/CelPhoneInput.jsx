import React from 'react'
import { FormControl, InputLabel, OutlinedInput, FormHelperText } from '@mui/material'
import { Controller } from 'react-hook-form'
import InputMask from 'react-input-mask'

const CelPhoneInput = ({control, errors, celPhone}) => {
  return <FormControl fullWidth>
  <Controller
    control={control}
    name="celPhone"
    render={({ field: { value, onChange } }) => (
      <>
        <InputLabel htmlFor="celPhone">Mobile Phone *</InputLabel>
        <InputMask
          disabled={
            celPhone !== "" && celPhone !== undefined
          }
          label="Mobile Phone *"
          mask="(99) 99999-9999"
          maskChar={null}
          onChange={onChange}
          value={value}
        >
          {(inputProps) => (
            <OutlinedInput
              {...inputProps}
              disabled={
                celPhone !== "" &&
                celPhone !== undefined
              }
              type="tel"
            />
          )}
        </InputMask>
      </>
    )}
  />
  {errors.celPhone ? (
    <FormHelperText
      id="validation-async-side"
      sx={{ color: "error.main" }}
    >
      {errors.celPhone.message}
    </FormHelperText>
  ) : null}
</FormControl>
}

export default CelPhoneInput
