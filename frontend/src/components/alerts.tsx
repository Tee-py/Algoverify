import React, { FC } from "react";
import { Alert } from "react-bootstrap";

type AlertProp = {
  variant: string;
  message: string;
  handleClose: () => void;
};

const AppAlert: FC<AlertProp> = (props) => {
  return (
    <Alert variant={props.variant} onClose={props.handleClose} dismissible style={{ marginTop: "2rem" }}>
      {props.message}
    </Alert>
  );
};

export default AppAlert;
