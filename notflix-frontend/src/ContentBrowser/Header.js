import React from 'react';
import {Navbar, NavbarBrand} from 'react-bootstrap';

function Header() {
    return (
        <Navbar style={{backgroundColor: "var(--gray-dark)"}} variant="dark">
            <NavbarBrand>Hello, world</NavbarBrand>
        </Navbar>
    );
}

export default Header;
