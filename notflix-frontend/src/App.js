import React, { useState } from 'react';
import { ToastContainer } from 'react-toastify';
import VideoContainer from './VideoContainer/VideoContainer';
import ContentBrowser from './ContentBrowser/ContentBrowser';
import './App.css';
import 'react-toastify/dist/ReactToastify.css';

function App() {

  const [isWatchingVideo, setIsWatchingVideo] = useState(false);
  const [videoId, setVideoId] = useState("");

  const playVideo = (id) => {
    setVideoId(id);
    setIsWatchingVideo(true);
  }

  if (isWatchingVideo) {
    return (
      <>
        <VideoContainer id={videoId} handleClose={() => setIsWatchingVideo(false)} />
        <ToastContainer position="bottom-right" />
      </>
    );
  } else {
    return (
      <>
        <ContentBrowser playVideo={playVideo} />
        <ToastContainer position="bottom-right" />
      </>
    );
  }
}

export default App;
