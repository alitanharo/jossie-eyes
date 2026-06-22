"use client";

import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";

const API_BASE_URL = "http://localhost:8000";

export default function Home() {
  const [isConnected, setIsConnected] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [currentMode, setCurrentMode] = useState("describe");
  const [analysisResult, setAnalysisResult] = useState("");
  const [neuralData, setNeuralData] = useState({
    alpha: [],
    beta: [],
    gamma: [],
    theta: []
  });
  const [azureResponse, setAzureResponse] = useState(null);
  const [lastUpdate, setLastUpdate] = useState(null);
  const canvasRef = useRef(null);

  const modes = [
    { id: "describe", name: "Describe Scene", icon: "👁️", color: "#3b82f6" },
    { id: "ocr", name: "Read Text", icon: "📝", color: "#8b5cf6" },
    { id: "neural_simulation", name: "Neural Simulation", icon: "🧠", color: "#ec4899" }
  ];

  // Simulate neural data updates
  useEffect(() => {
    const interval = setInterval(() => {
      setNeuralData(prev => ({
        alpha: [...prev.alpha.slice(-50), Math.random() * 100],
        beta: [...prev.beta.slice(-50), Math.random() * 100],
        gamma: [...prev.gamma.slice(-50), Math.random() * 100],
        theta: [...prev.theta.slice(-50), Math.random() * 100]
      }));
      setLastUpdate(new Date());
    }, 100);

    return () => clearInterval(interval);
  }, []);

  // Check API connection
  useEffect(() => {
    const checkConnection = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/health`);
        if (response.ok) {
          setIsConnected(true);
        }
      } catch (error) {
        setIsConnected(false);
      }
    };
    checkConnection();
    const interval = setInterval(checkConnection, 5000);
    return () => clearInterval(interval);
  }, []);

  const startAnalysis = async () => {
    setIsAnalyzing(true);
    setAnalysisResult("");
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mode: currentMode, source: "raspberry_pi_camera" })
      });

      if (response.ok) {
        const data = await response.json();
        setAnalysisResult(data.description);
        setAzureResponse(data);
      }
    } catch (error) {
      console.error("Analysis error:", error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const WaveformChart = ({ data, color, label }) => (
    <div className="relative">
      <div className="flex justify-between items-center mb-2">
        <span className="text-sm font-medium text-gray-300">{label}</span>
        <span className="text-xs text-gray-500">{data[data.length - 1]?.toFixed(1) || 0} μV</span>
      </div>
      <div className="h-28 bg-black/80 rounded-lg overflow-hidden border border-gray-900">
        <svg className="w-full h-full" viewBox={`0 0 ${data.length} 100`} preserveAspectRatio="none">
          <defs>
            <linearGradient id={`gradient-${label}`} x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor={color} stopOpacity="0.6" />
              <stop offset="100%" stopColor={color} stopOpacity="0" />
            </linearGradient>
          </defs>
          <path
            d={`M ${data.map((val, i) => `${i},${50 - (val - 50) * 0.8}`).join(" L ")}`}
            fill="none"
            stroke={color}
            strokeWidth="1"
            strokeLinecap="round"
            strokeLinejoin="round"
            style={{ filter: `drop-shadow(0 0 4px ${color})` }}
          />
          <path
            d={`M ${data.map((val, i) => `${i},${50 - (val - 50) * 0.8}`).join(" L ")} L ${data.length - 1},100 L 0,100 Z`}
            fill={`url(#gradient-${label})`}
            opacity="0.2"
          />
        </svg>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-black text-white overflow-hidden relative">
      {/* Animated Background - Dark with Neural Network */}
      <div className="fixed inset-0">
        <div className="absolute inset-0 bg-gradient-to-br from-black via-gray-900 to-black" />
        <div className="absolute inset-0 opacity-10 bg-[radial-gradient(ellipse at center, rgba(124,58,237,0.3) 0%, transparent 70%)]" />
        <div className="absolute inset-0" style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%237c3aed' fill-opacity='0.15'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
          opacity: 0.3
        }} />
      </div>

      {/* Header */}
      <header className="relative z-10 border-b border-white/10 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <motion.div 
              className="flex items-center space-x-4"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
            >
              <div className="relative">
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-2xl">
                  🧠
                </div>
                <div className="absolute -inset-1 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl blur opacity-30 animate-pulse" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                  Jossie Eyes
                </h1>
                <p className="text-xs text-gray-400">Neural Sensory Guide</p>
              </div>
            </motion.div>

            {/* Connection Status */}
            <motion.div 
              className="flex items-center space-x-3"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
            >
              <div className={`flex items-center space-x-2 px-4 py-2 rounded-full ${isConnected ? 'bg-green-500/20' : 'bg-red-500/20'} border ${isConnected ? 'border-green-500/50' : 'border-red-500/50'}`}>
                <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'} animate-pulse`} />
                <span className="text-sm">{isConnected ? 'Azure Connected' : 'Disconnected'}</span>
              </div>
              {lastUpdate && (
                <span className="text-xs text-gray-500">
                  Last update: {lastUpdate.toLocaleTimeString()}
                </span>
              )}
            </motion.div>
          </div>
        </div>
      </header>

      <main className="relative z-10 max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Panel - Controls */}
          <div className="lg:col-span-1 space-y-6">
            {/* Mode Selection */}
            <motion.div 
              className="bg-black/60 backdrop-blur-xl rounded-2xl p-6 border border-purple-500/30 shadow-lg shadow-purple-500/10"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
            >
              <h2 className="text-lg font-semibold mb-4 text-white flex items-center">
                <span className="w-1 h-6 bg-purple-500 rounded-full mr-3" />
                Analysis Mode
              </h2>
              <div className="space-y-3">
                {modes.map((mode) => (
                  <motion.button
                    key={mode.id}
                    onClick={() => setCurrentMode(mode.id)}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition-all ${
                      currentMode === mode.id
                        ? `bg-gradient-to-r from-${mode.color}/20 to-${mode.color}/10 border-2 border-${mode.color} shadow-lg shadow-${mode.color}/20`
                        : "bg-black/40 border border-white/10 hover:border-white/20 hover:bg-black/60"
                    }`}
                  >
                    <span className="text-2xl">{mode.icon}</span>
                    <span className="text-sm font-medium text-gray-200">{mode.name}</span>
                    {currentMode === mode.id && (
                      <motion.div
                        layoutId="activeMode"
                        className={`ml-auto w-2 h-2 rounded-full bg-${mode.color} shadow-lg shadow-${mode.color}/50`}
                      />
                    )}
                  </motion.button>
                ))}
              </div>
            </motion.div>

            {/* Camera Feed */}
            <motion.div 
              className="bg-black/60 backdrop-blur-xl rounded-2xl p-6 border border-cyan-500/30 shadow-lg shadow-cyan-500/10"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
            >
              <h2 className="text-lg font-semibold mb-4 text-white flex items-center">
                <span className="w-1 h-6 bg-cyan-500 rounded-full mr-3" />
                Camera Feed
              </h2>
              <div className="relative aspect-video bg-black rounded-xl overflow-hidden border border-cyan-500/30 shadow-lg shadow-cyan-500/10">
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="text-center">
                    <div className="text-4xl mb-2">📹</div>
                    <p className="text-sm text-gray-400">Raspberry Pi Camera</p>
                    <p className="text-xs text-gray-500 mt-1">Live feed active</p>
                  </div>
                </div>
                {/* Scanning line animation */}
                <motion.div
                  className="absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r from-transparent via-blue-500 to-transparent"
                  animate={{ top: ["0%", "100%", "0%"] }}
                  transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
                />
              </div>
            </motion.div>

            {/* Start Analysis Button */}
            <motion.div 
              className="bg-black/60 backdrop-blur-xl rounded-2xl p-6 border border-green-500/30 shadow-lg shadow-green-500/10"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
            >
              <h2 className="text-lg font-semibold mb-4 text-white flex items-center">
                <span className="w-1 h-6 bg-green-500 rounded-full mr-3" />
                Control
              </h2>
              <motion.button
                onClick={startAnalysis}
                disabled={isAnalyzing}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="w-full py-4 bg-gradient-to-r from-green-500 to-emerald-600 rounded-xl font-semibold text-white disabled:opacity-50 disabled:cursor-not-allowed relative overflow-hidden shadow-lg shadow-green-500/30 hover:shadow-green-500/50 transition-shadow"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-green-600 to-emerald-700 opacity-0 hover:opacity-100 transition-opacity" />
                <span className="relative flex items-center justify-center space-x-2">
                  {isAnalyzing ? (
                    <>
                      <motion.div
                        animate={{ rotate: 360 }}
                        transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                        className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full"
                      />
                      <span>Analyzing...</span>
                    </>
                  ) : (
                    <>
                      <span>🚀</span>
                      <span>Start Analysis</span>
                    </>
                  )}
                </span>
              </motion.button>
            </motion.div>
          </div>

          {/* Right Panel - Neural Visualization */}
          <div className="lg:col-span-2 space-y-6">
            {/* Analysis Result */}
            <motion.div 
              className="bg-black/60 backdrop-blur-xl rounded-2xl p-6 border border-blue-500/30 shadow-lg shadow-blue-500/10 min-h-[200px]"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
            >
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-semibold text-white">Analysis Result</h2>
                {azureResponse && (
                  <span className="text-xs text-green-400 flex items-center space-x-1">
                    <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                    <span>Processed by Azure</span>
                  </span>
                )}
              </div>
              
              {analysisResult ? (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="prose prose-invert max-w-none"
                >
                  <p className="text-gray-200 leading-relaxed">{analysisResult}</p>
                </motion.div>
              ) : (
                <div className="flex flex-col items-center justify-center h-32 text-gray-500">
                  <span className="text-4xl mb-2">🧠</span>
                  <p>Ready to analyze</p>
                </div>
              )}
            </motion.div>

            {/* Neural Signals Dashboard */}
            <motion.div 
              className="bg-black/60 backdrop-blur-xl rounded-2xl p-6 border border-pink-500/30 shadow-lg shadow-pink-500/10"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
            >
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-semibold text-white flex items-center">
                  <span className="w-1 h-6 bg-pink-500 rounded-full mr-3" />
                  Neural Signals
                </h2>
                <div className="flex space-x-2">
                  <div className="flex items-center space-x-1 text-xs text-gray-400">
                    <div className="w-2 h-2 bg-blue-500 rounded-full shadow-lg shadow-blue-500/50" />
                    <span>Alpha</span>
                  </div>
                  <div className="flex items-center space-x-1 text-xs text-gray-400">
                    <div className="w-2 h-2 bg-purple-500 rounded-full shadow-lg shadow-purple-500/50" />
                    <span>Beta</span>
                  </div>
                  <div className="flex items-center space-x-1 text-xs text-gray-400">
                    <div className="w-2 h-2 bg-pink-500 rounded-full shadow-lg shadow-pink-500/50" />
                    <span>Gamma</span>
                  </div>
                  <div className="flex items-center space-x-1 text-xs text-gray-400">
                    <div className="w-2 h-2 bg-yellow-500 rounded-full shadow-lg shadow-yellow-500/50" />
                    <span>Theta</span>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <WaveformChart data={neuralData.alpha} color="#3b82f6" label="Alpha Waves" />
                <WaveformChart data={neuralData.beta} color="#8b5cf6" label="Beta Waves" />
                <WaveformChart data={neuralData.gamma} color="#ec4899" label="Gamma Waves" />
                <WaveformChart data={neuralData.theta} color="#f59e0b" label="Theta Waves" />
              </div>

              {/* Brain Activation Visualization */}
              <div className="mt-6">
                <h3 className="text-sm font-medium text-gray-300 mb-3">Brain Activation Map</h3>
                <div className="relative h-48 bg-black/80 rounded-xl overflow-hidden border border-pink-500/30 shadow-lg shadow-pink-500/10">
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="relative w-32 h-32">
                      {/* Brain activation heatmap spots */}
                      <div className="absolute top-1/4 left-1/4 w-8 h-8 rounded-full bg-blue-500/40 blur-xl animate-pulse" />
                      <div className="absolute top-1/3 right-1/4 w-6 h-6 rounded-full bg-purple-500/50 blur-lg animate-pulse" style={{ animationDelay: '0.5s' }} />
                      <div className="absolute bottom-1/3 left-1/3 w-10 h-10 rounded-full bg-pink-500/30 blur-xl animate-pulse" style={{ animationDelay: '1s' }} />
                      <div className="absolute bottom-1/4 right-1/3 w-5 h-5 rounded-full bg-yellow-500/40 blur-lg animate-pulse" style={{ animationDelay: '1.5s' }} />
                      
                      {/* Animated brain activation circles */}
                      {[...Array(5)].map((_, i) => (
                        <motion.div
                          key={i}
                          className="absolute inset-0 rounded-full border-2 border-pink-500/30"
                          animate={{
                            scale: [1, 1.5, 1],
                            opacity: [0.5, 0, 0.5]
                          }}
                          transition={{
                            duration: 2,
                            delay: i * 0.3,
                            repeat: Infinity
                          }}
                        />
                      ))}
                      <div className="absolute inset-0 flex items-center justify-center">
                        <span className="text-5xl">🧠</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>

            {/* Azure Response Details */}
            {azureResponse && (
              <motion.div 
                className="bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/10"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6 }}
              >
                <h2 className="text-lg font-semibold mb-4 text-white">Azure Response Details</h2>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div className="bg-gray-900/50 rounded-lg p-3">
                    <span className="text-gray-400">Confidence Score</span>
                    <p className="text-lg font-semibold text-blue-400">
                      {(azureResponse.confidence * 100).toFixed(1)}%
                    </p>
                  </div>
                  <div className="bg-gray-900/50 rounded-lg p-3">
                    <span className="text-gray-400">Processing Time</span>
                    <p className="text-lg font-semibold text-purple-400">
                      {azureResponse.processing_time?.toFixed(2) || '0.00'}s
                    </p>
                  </div>
                  <div className="bg-gray-900/50 rounded-lg p-3">
                    <span className="text-gray-400">Detected Objects</span>
                    <p className="text-lg font-semibold text-green-400">
                      {azureResponse.objects?.length || 0}
                    </p>
                  </div>
                  <div className="bg-gray-900/50 rounded-lg p-3">
                    <span className="text-gray-400">Neural Intensity</span>
                    <p className="text-lg font-semibold text-pink-400">
                      {(azureResponse.intensity * 100).toFixed(1)}%
                    </p>
                  </div>
                </div>
              </motion.div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}