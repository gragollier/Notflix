import React from 'react';
import './VideoNavigation.css';

function VideoNavigation(props) {
    return (
        <div className="video-navigation">
            <button className="close-video-nav-button" onClick={props.handleClose}>
            <svg width="3em" height="3em" viewBox="0 0 16 16" className="bi bi-x" fill="white" xmlns="http://www.w3.org/2000/svg">
                <path fillRule="evenodd" d="M11.854 4.146a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708-.708l7-7a.5.5 0 0 1 .708 0z"/>
                <path fillRule="evenodd" d="M4.146 4.146a.5.5 0 0 0 0 .708l7 7a.5.5 0 0 0 .708-.708l-7-7a.5.5 0 0 0-.708 0z"/>
            </svg>
            </button>
        </div>
    );
}

export default VideoNavigation;
