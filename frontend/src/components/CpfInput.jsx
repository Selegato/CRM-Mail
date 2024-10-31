import { Controller } from 'react-hook-form';
import { FormControl, InputLabel, OutlinedInput, FormHelperText } from '@mui/material';
import InputMask from 'react-input-mask';

const CpfInput = ({control, errors, documentNumber}) => {
  return (
    <FormControl fullWidth>
      <Controller
        control={control}
        name="documentNumber"
        render={({ field: { value, onChange } }) => (
          <>
            <InputLabel htmlFor="documentNumber">CPF *</InputLabel>
            <InputMask
              disabled={
                documentNumber !== "" &&
                documentNumber !== undefined
              }
              label="CPF *"
              mask="999.999.999-99"
              maskChar={null}
              onChange={onChange}
              value={value}
            >
              {(inputProps) => (
                <OutlinedInput
                  {...inputProps}
                  disabled={
                    documentNumber !== "" &&
                    documentNumber !== undefined
                  }
                  type="tel"
                />
              )}
            </InputMask>
          </>
        )}
      />
      {errors.documentNumber ? (
        <FormHelperText id="validation-async-side" sx={{ color: "error.main" }}>
          {errors.documentNumber.message}
        </FormHelperText>
      ) : null}
    </FormControl>
  );
};

export default CpfInput;
