import React, { useRef, useEffect, useState } from 'react';
import Draggable from 'react-draggable';
import styled from 'styled-components';

const CircularCamera = styled.div`
  width: 200px;
  height: 200px;
  border-radius: 50%;
  overflow: hidden;
  position: relative;
  background: black;
  cursor: move;
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
`;

const Video = styled.video`
  width: 100%;
  height: 100%;
  object-fit: cover;
  transform: scaleX(-1);
`;

const Controls = styled.div`
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 10px;
  opacity: 0;
  transition: opacity 0.3s;
  ${CircularCamera}:hover & {
    opacity: 1;
  }
`;

const Button = styled.button`
  background: rgba(0,0,0,0.5);
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  &:hover {
    background: rgba(0,0,0,0.7);
  }
`;

function App() {
  const videoRef = useRef(null);
  const [stream, setStream] = useState(null);
  const [isActive, setIsActive] = useState(true);

  useEffect(() => {
    startCamera();
    return () => {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  const startCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({ 
        video: { width: 400, height: 400 } 
      });
      setStream(mediaStream);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
      setIsActive(true);
    } catch (err) {
      console.error("Error accessing camera:", err);
    }
  };

  const toggleCamera = () => {
    if (isActive && stream) {
      stream.getTracks().forEach(track => track.stop());
      setIsActive(false);
    } else {
      startCamera();
    }
  };

  return (
    <Draggable>
      <CircularCamera>
        <Video
          ref={videoRef}
          autoPlay
          playsInline
          muted
        />
        <Controls>
          <Button onClick={toggleCamera}>
            {isActive ? 'Stop' : 'Start'}
          </Button>
        </Controls>
      </CircularCamera>
    </Draggable>
  );
}

export default App;