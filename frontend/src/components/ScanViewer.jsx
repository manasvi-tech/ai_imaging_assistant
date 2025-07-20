import { useApi } from '../../api';

export default function SegmentationViewer({ scanId }) {
  const [mask, setMask] = useState(null);
  const api = useApi();
  
  const runSegmentation = async () => {
    const result = await api.post(`/scans/${scanId}/segment`);
    setMask(result.mask);
  };

  return (
    <div className="relative">
      <button onClick={runSegmentation} className="bg-blue-500 text-white p-2">
        Run AI Segmentation
      </button>
      
      {mask && (
        <canvas 
          id="mask-canvas" 
          className="absolute top-0 left-0 pointer-events-none"
          width={mask.shape[1]}
          height={mask.shape[0]}
        />
      )}
    </div>
  );
}