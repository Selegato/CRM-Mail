import { Alert } from "@mui/material";

const ErrorAlert = () => {
  return (
    <Alert severity="error">
      An error occurred while fetching data. Please try again later.
    </Alert>
  );
};

export default ErrorAlert;
