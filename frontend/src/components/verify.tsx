import React, { FC, useState } from "react";
import Button from "react-bootstrap/Button";
import { Container } from "react-bootstrap";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Form from "react-bootstrap/Form";
import Spinner from "react-bootstrap/Spinner";
import AppAlert from "./alerts";
import { verifyTealApp } from "../network";
import { FormState } from "../types";

const VerifyAppPage: FC = () => {
  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const target = event.currentTarget;
    if (target.name === "app-id") {
      setFormState({ ...formState, appId: target.value });
    }
    if (target.name === "name") {
      setFormState({ ...formState, name: target.value });
    }
    if (target.name === "description") {
      setFormState({ ...formState, description: target.value });
    }
    if (target.name === "type") {
      setFormState({ ...formState, type: target.value });
    }
    if (target.name === "github-url") {
      setFormState({ ...formState, githubUrl: target.value });
    }
    if (target.name === "approval-github") {
      setFormState({ ...formState, approvalUrl: target.value });
    }
    if (target.name === "clear-state-github") {
      setFormState({ ...formState, clearStateUrl: target.value });
    }
  };
  const handleSelectChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const target = event.currentTarget;
    setFormState({ ...formState, type: target.value });
  };

  const handleFormSubmit: React.FormEventHandler<HTMLFormElement> = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (formState.type === "1" && !formState.approvalUrl && !formState.clearStateUrl) {
      setAlertState({
        variant: "danger",
        show: true,
        message: "Approval And Clear State github url is required for Teal verification.",
      });
      return;
    }
    if (formState.type === "2" && !formState.githubUrl) {
      setAlertState({ variant: "danger", show: true, message: "Github url required for reach contract verification." });
      return;
    }
    for (let [key, value] of Object.entries(formState)) {
      if (key !== "githubUrl" && key !== "approvalUrl" && key !== "clearStateUrl") {
        if (!value) {
          setAlertState({ variant: "danger", show: true, message: `${key} is required` });
          return;
        }
      }
    }
    setLoading(true);
    let response;
    if (formState.type === "1") {
      const payload = {
        app_id: formState.appId,
        name: formState.name,
        description: formState.description,
        approval_github_url: formState.approvalUrl,
        clear_state_github_url: formState.clearStateUrl,
      };
      try {
        response = await verifyTealApp(payload);
      } catch {
        setLoading(false);
        setAlertState({ variant: "danger", message: "An Error Occurred.", show: true });
      }
      setAlertState({ variant: "success", message: response.message, show: true });
      setLoading(false);
    }
  };

  const handleAlertClose = () => {
    setAlertState({ show: false, message: "", variant: "" });
  };

  const defaultFormState: FormState = {
    appId: "",
    name: "",
    description: "",
    githubUrl: "",
    approvalUrl: "",
    clearStateUrl: "",
    type: "1",
  };

  const [formState, setFormState] = useState(defaultFormState);
  const [alertState, setAlertState] = useState({ show: false, message: "", variant: "" });
  const [loading, setLoading] = useState(false);

  return (
    <Container>
      <Row>
        <Col></Col>
        <Col sm={12} md={6}>
          <h1 style={{ paddingTop: "2rem" }}>Verify Algorand App</h1>
          {alertState.show ? (
            <AppAlert
              variant={alertState.variant}
              message={alertState.message}
              handleClose={handleAlertClose}
            ></AppAlert>
          ) : (
            <></>
          )}
          <Form style={{ marginTop: "2rem" }} onSubmit={handleFormSubmit}>
            <Form.Group className="mb-3" controlId="contractName">
              <Form.Control type="text" name="app-id" placeholder="Enter app id" onChange={handleInputChange} />
            </Form.Group>
            <Form.Group className="mb-3" controlId="contractName">
              <Form.Control type="text" name="name" placeholder="Enter app name" onChange={handleInputChange} />
            </Form.Group>
            <Form.Group className="mb-3" controlId="descripion">
              <Form.Control
                type="text"
                name="description"
                placeholder="Enter app description"
                as="textarea"
                rows={3}
                onChange={handleInputChange}
              />
            </Form.Group>
            <Form.Select aria-label="Contract type" name="type" className="mb-3" onChange={handleSelectChange}>
              <option value="1">Teal</option>
              <option value="2">Reach</option>
            </Form.Select>
            {formState.type === "1" ? (
              <div>
                <Form.Group className="mb-3" controlId="approval-github">
                  <Form.Control
                    type="text"
                    name="approval-github"
                    placeholder="Enter approval github url"
                    onChange={handleInputChange}
                  />
                </Form.Group>
                <Form.Group className="mb-3" controlId="clear-state-github">
                  <Form.Control
                    type="text"
                    name="clear-state-github"
                    placeholder="Enter clear state github url"
                    onChange={handleInputChange}
                  />
                </Form.Group>
              </div>
            ) : (
              <Form.Group className="mb-3" controlId="github-url">
                <Form.Control
                  type="text"
                  name="github-url"
                  placeholder="Enter github url"
                  onChange={handleInputChange}
                />
              </Form.Group>
            )}
            <div className="d-grid gap-2">
              {!loading ? (
                <Button variant="primary" size="lg" type="submit">
                  Verify
                </Button>
              ) : (
                <Button variant="primary" disabled size="lg">
                  <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" />
                  <span className="visually-hidden">Loading...</span>
                </Button>
              )}
            </div>
          </Form>
        </Col>
        <Col></Col>
      </Row>
    </Container>
  );
};

export default VerifyAppPage;
