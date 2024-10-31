import { Typography } from "@mui/material";

const Title = ({ title, tenantName }) => {
  return (
    <Typography align="center" gutterBottom variant="h4">
      {`${title} - ${tenantName}`}
    </Typography>
  );
};
export default Title;
