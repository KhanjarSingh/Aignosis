import { useState } from 'react';
export default function VideoPlayer() {
    const [uid, setUid] = useState<string>('');
    const [tid, setTid] = useState<string>('');
    const [videoUrl, setVideoUrl] = useState('');
    const handlePlay = ():void => {
        const url = `https://aignosis-layc.onrender.com/video/stream?uid=${uid}&tid=${tid}`;
        setVideoUrl(url);
    };

    const handleExample = ():void =>{
        setTid("456")
        setUid("123")
    }
    return (
        <>
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
        <div>
            <button onClick={handleExample}>Try Example!!!</button>
        </div>
    </>
    );
}