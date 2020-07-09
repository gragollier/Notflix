import React, { useState, useEffect } from 'react';
import ReactPlayer from 'react-player';
import VideoNavigation from './VideoNavigation/VideoNavigation';
import VideoInfo from './VideoInfo/VideoInfo';
import axios from 'axios';
import routes from '../data/routes';
import { toast } from 'react-toastify';
import "./VideoContainer.css";

function VideoContainer(props) {
    const [isHovering, setIsHovering] = useState(true);
    const [timeoutId, setTimeoutId] = useState(null);
    const [videoUrl, setVideoUrl] = useState("");

    useEffect(() => {
        const getData = async () => {
            try {
                const res = await axios.get(routes.findEdgeNode + props.id);
                setVideoUrl(res.data.mpd);
            } catch (error) {
                console.error(error);
                toast.error("Error loading video");
            }
        }
        getData();
    }, [props.id])
    
    const handleMouseMove = () => {
        setIsHovering(true);
        clearTimeout(timeoutId);
        setTimeoutId(setTimeout(() => {
            setIsHovering(false);
        }, 650));
    }

    return (
        <>
        <div onMouseMove={handleMouseMove}>
            {isHovering && <VideoNavigation handleClose={props.handleClose} />}
            <div className='video-container' >
                <ReactPlayer className='react-player' width='100%' height='100%' url={videoUrl} controls={true} playing={true} />
            </div>
        </div>
        <VideoInfo videoId={props.id} />
        </>
    );
}

export default VideoContainer;
