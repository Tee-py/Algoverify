import React, { FC } from "react";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";

const Header: FC = () => {
  return (
    <Navbar bg="dark" variant="dark">
      <Container fluid>
        <Navbar.Brand href="/">AlgoVerify</Navbar.Brand>
        <Nav className="justify-content-center">
          <Nav.Link href="/verify">Verify</Nav.Link>
          <Nav.Link href="/">Apps</Nav.Link>
        </Nav>
      </Container>
    </Navbar>
  );
};

export default Header;
