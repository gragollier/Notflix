import React, { useState, useEffect } from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import axios from 'axios';
import { toast } from 'react-toastify';
import routes from '../../data/routes';
import './VideoInfo.css';

function VideoInfo(props) {
    const [videoInfo, setVideoInfo] = useState({});

    useEffect(() => {
        const getData = async () => {
            try {
                const res = await axios.get(routes.getVideoInfo + `${props.videoId}`);
                setVideoInfo(res.data);
            } catch (error) {
                console.error(error);
                toast.error("Error loading video info");
            }
        }
        getData();
    }, [props.videoId]);

    return (
        <Container style={{marginTop: "20px"}}>
            <Row>
                <Col md={2}></Col>
                <Col md={8}>
                    <h2 className="text-center">{videoInfo.title}</h2>
                    <h4 className="text-center">{videoInfo.subtitle}</h4>
                    <hr />
                    <p>{videoInfo.synopsis}</p>
                </Col>
                <Col md={2}></Col>
            </Row>
        </Container>
    );
}

export default VideoInfo;
