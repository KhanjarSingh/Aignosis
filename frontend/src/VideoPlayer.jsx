import { useState } from 'react';
export default function VideoPlayer() {
    const [uid, setUid] = useState('');
    const [tid, setTid] = useState('');
    const [videoUrl, setVideoUrl] = useState('');
    const handlePlay = () => {
        const url = `https://aignosis-layc.onrender.com/video/stream?uid=${uid}&tid=${tid}`;
        setVideoUrl(url);
    };
    return (
        <div>
            <h1>Admin Video Player</h1>
            <input
                placeholder="UID"
                value={uid}
                onChange={(e) => setUid(e.target.value)}
            />
            <input
                placeholder="Transaction ID"
                value={tid}
                onChange={(e) => setTid(e.target.value)}
            />
            <button onClick={handlePlay}>Play Video</button>
            {videoUrl && (
                <video controls width="800" src={videoUrl} />
            )}
        </div>
    );
}