import React, { useState } from 'react';
import { Col, Container, Row } from 'react-bootstrap';
import SearchBar from './SearchBar';
import VideoList from './VideoList';
import './ContentBrowser.css';

function ContentBrowser(props) {
    const [searchTerm, setSearchTerm] = useState("");

    return(
        <>
        <Container className="brand-header">
            <Row>
                <Col md={2}></Col>
                <Col md={8}>
                    <h1 className="text-center">Notfilx</h1>
                    <h3 className="text-center">Start searching to find something you'll love</h3>
                    <br />
                    <SearchBar onInput={setSearchTerm}/>
                </Col>
                <Col md={2}></Col>
            </Row>
            <hr />
        </Container>
        <VideoList searchTerm={searchTerm} playVideo={props.playVideo} />
        </>
    );
}

export default ContentBrowser;
