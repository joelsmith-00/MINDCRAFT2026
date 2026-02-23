import { useEffect, useRef } from "react";

// Palette: #1b120e #34251b #534030 #7b5f48 #a68569
// 4 layers back→front. Each layer uses two adjacent palette stops for its gradient.
const PALETTE = ["#1b120e", "#34251b", "#534030", "#7b5f48", "#a68569"];

const LAYERS = [
  { p0: 0, p1: 1, p2: 2, baseAmp: 0.10, voiceAmp: 0.68, speed: 0.00110, freq: 2.0, phaseOff: 0.0 },
  { p0: 1, p1: 2, p2: 3, baseAmp: 0.08, voiceAmp: 0.58, speed: 0.00140, freq: 2.5, phaseOff: 1.9 },
  { p0: 2, p1: 3, p2: 4, baseAmp: 0.06, voiceAmp: 0.46, speed: 0.00170, freq: 3.1, phaseOff: 3.7 },
  { p0: 1, p1: 3, p2: 4, baseAmp: 0.04, voiceAmp: 0.34, speed: 0.00210, freq: 3.8, phaseOff: 5.5 },
];

const NUM_PTS = 180;

export default function App() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx    = canvas.getContext("2d");

    function resize() {
      canvas.width  = window.innerWidth;
      canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener("resize", resize);

    let animId;
    let analyser  = null;
    let dataArray = null;
    let smoothEnergy = 0;
    const phase = new Float64Array(LAYERS.length);

    async function setupMic() {
      try {
        const stream       = await navigator.mediaDevices.getUserMedia({ audio: true });
        const audioContext = new AudioContext();
        const source       = audioContext.createMediaStreamSource(stream);
        analyser           = audioContext.createAnalyser();
        analyser.fftSize   = 1024;
        analyser.smoothingTimeConstant = 0.80;
        source.connect(analyser);
        dataArray = new Uint8Array(analyser.frequencyBinCount);
      } catch (e) {
        console.warn("Mic unavailable.", e);
      }
    }

    function getEnergy() {
      if (!analyser || !dataArray) return 0;
      analyser.getByteFrequencyData(dataArray);
      let sum = 0;
      const lim = Math.min(200, dataArray.length);
      for (let i = 0; i < lim; i++) sum += dataArray[i];
      return Math.pow(sum / (lim * 255), 0.55);
    }

    function buildPoints(layer, layerIdx, W, H, energy) {
      const amp = layer.baseAmp + energy * layer.voiceAmp;
      const ph  = phase[layerIdx];
      const pts = [];
      for (let i = 0; i <= NUM_PTS; i++) {
        const t = i / NUM_PTS;
        const x = t * W;
        const w1 =        Math.sin(2 * Math.PI * layer.freq        * t + ph);
        const w2 = 0.42 * Math.sin(2 * Math.PI * layer.freq * 1.73 * t + ph * 1.4 + 1.1);
        const w3 = 0.20 * Math.sin(2 * Math.PI * layer.freq * 0.47 * t + ph * 0.6 + 2.8);
        const wave = (w1 + w2 + w3) / (1 + 0.42 + 0.20);
        const y = H * 0.97 - (wave * 0.5 + 0.5) * amp * H;
        pts.push({ x, y });
      }
      return pts;
    }

    // Parse hex to [r,g,b]
    function hexRgb(hex) {
      return [
        parseInt(hex.slice(1,3),16),
        parseInt(hex.slice(3,5),16),
        parseInt(hex.slice(5,7),16),
      ];
    }
    // Lerp between two hex colours, return rgba string
    function lerpColor(hex1, hex2, t, a) {
      const [r1,g1,b1] = hexRgb(hex1);
      const [r2,g2,b2] = hexRgb(hex2);
      return `rgba(${Math.round(r1+(r2-r1)*t)},${Math.round(g1+(g2-g1)*t)},${Math.round(b1+(b2-b1)*t)},${a})`;
    }

    function drawWave(pts, W, H, layer, energy) {
      ctx.beginPath();
      ctx.moveTo(0, H);
      ctx.lineTo(pts[0].x, pts[0].y);
      for (let i = 1; i < pts.length - 1; i++) {
        const mx = (pts[i].x + pts[i + 1].x) / 2;
        const my = (pts[i].y + pts[i + 1].y) / 2;
        ctx.quadraticCurveTo(pts[i].x, pts[i].y, mx, my);
      }
      ctx.lineTo(pts[pts.length - 1].x, pts[pts.length - 1].y);
      ctx.lineTo(W, H);
      ctx.closePath();

      const edge  = lerpColor(PALETTE[layer.p0], PALETTE[layer.p1], 0.2,  0.96);
      const mid   = lerpColor(PALETTE[layer.p1], PALETTE[layer.p2], 0.3,  0.90);
      const crest = lerpColor(PALETTE[layer.p1], PALETTE[layer.p2], 0.4 + energy * 0.6, 0.85);

      const grad = ctx.createLinearGradient(0, 0, W, 0);
      grad.addColorStop(0.00, edge);
      grad.addColorStop(0.25, mid);
      grad.addColorStop(0.50, crest);
      grad.addColorStop(0.75, mid);
      grad.addColorStop(1.00, edge);
      ctx.fillStyle = grad;
      ctx.fill();
    }

    let lastTs = 0;

    function draw(ts) {
      animId = requestAnimationFrame(draw);
      const dt = Math.min(ts - lastTs, 50);
      lastTs = ts;
      const W = canvas.width;
      const H = canvas.height;

      const raw = getEnergy();
      smoothEnergy += (raw - smoothEnergy) * (raw > smoothEnergy ? 0.45 : 0.05);

      for (let i = 0; i < LAYERS.length; i++) {
        phase[i] += LAYERS[i].speed * (1 + smoothEnergy * 2.2) * dt;
      }

      ctx.clearRect(0, 0, W, H);

      for (let i = 0; i < LAYERS.length; i++) {
        const pts = buildPoints(LAYERS[i], i, W, H, smoothEnergy);
        drawWave(pts, W, H, LAYERS[i], smoothEnergy);
      }
    }

    setupMic();
    requestAnimationFrame(draw);

    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener("resize", resize);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      style={{ display: "block", background: "#1b120e" }}
    />
  );
}
