import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Container } from 'react-bootstrap';
import { toast } from 'react-toastify';
import axios from 'axios';
import routes from '../data/routes';

function VideoList(props) {
    const [videos, setVideos] = useState([]);

    useEffect(() => {
        const getData = async () => {
            try {
                const res = await axios.post(routes.search, { query: props.searchTerm } );
                setVideos(res.data);
            } catch (error) {
                console.error(error);
                toast.error("Error loading search results");
            }
        }
        getData();
    }, [props.searchTerm]);


    return (
        <>
        <Container fluid={true}>
            <Row>
                {videos.map((video) => <Col s={12} lg={3} key={video.id}>
                    <Card style={{backgroundColor: "var(--gray-dark)", marginBottom: "10px", cursor: "pointer"}} onClick={() => props.playVideo(video.id)}>
                        <Card.Header>
                            <Card.Title >{video.title}</Card.Title>
                        </Card.Header>
                        <Card.Img src="temp.png"></Card.Img>
                        <Card.Body>
                            <Card.Text>{video.synopsis}</Card.Text>
                        </Card.Body>
                    </Card>
                    </Col>)}
            </Row>
        </Container>
        </>
    );

}

export default VideoList;
