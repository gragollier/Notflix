import React from 'react';
import { Form } from 'react-bootstrap';

function SearchBar(props) {
    const handleInput = (event) => {
        props.onInput(event.target.value);
    }

    // Prevent enter key from submitting the "form"
    const handleKeyDown = (event) => {
        if (event.keyCode === 13) {
            event.preventDefault();
        }
    }
    
    return (
        <Form>
            <Form.Control placeholder="Search" onChange={handleInput} onKeyDown={handleKeyDown}></Form.Control>
        </Form>
    );
}

export default SearchBar;