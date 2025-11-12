import React, { useState, useRef, useEffect } from "react";
import Webcam from "react-webcam";
import axios from "axios";
import { motion } from "framer-motion";

function App() {
  const [currentPage, setCurrentPage] = useState("home");
  const webcamRef = useRef(null);
  const [prediction, setPrediction] = useState("Show a sign to start!");
  const [confidence, setConfidence] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (currentPage !== "interpreter") return;

    const capture = async () => {
      if (!webcamRef.current) return;
      
      const imageSrc = webcamRef.current.getScreenshot();
      if (!imageSrc) return;

      try {
        const res = await axios.post("http://127.0.0.1:5000/predict", { 
          image: imageSrc 
        });
        setPrediction(res.data.prediction);
        setConfidence((res.data.confidence * 100).toFixed(2));
        setError(null);
      } catch (err) {
        console.error(err);
        setError("Connection failed. Is the server running?");
        setPrediction("Error");
        setConfidence(null);
      }
    };

    const interval = setInterval(capture, 1000);
    return () => clearInterval(interval);
  }, [currentPage]);

  if (currentPage === "home") {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900 text-white px-4">
        <motion.div
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center max-w-3xl"
        >
          <h1 className="text-6xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            ASL Interpreter
          </h1>
          <p className="text-xl text-gray-300 mb-12">
            Real-time American Sign Language Detection
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="bg-gray-800 rounded-2xl shadow-2xl p-8 max-w-2xl w-full mb-8"
        >
          <h2 className="text-2xl font-semibold mb-6 text-blue-400">How It Works</h2>
          <div className="space-y-4 text-gray-300">
            <div className="flex items-start">
              <span className="text-blue-400 font-bold text-xl mr-3">1.</span>
              <p>Click "Start Interpreter" to access your webcam</p>
            </div>
            <div className="flex items-start">
              <span className="text-blue-400 font-bold text-xl mr-3">2.</span>
              <p>Position yourself in front of the camera</p>
            </div>
            <div className="flex items-start">
              <span className="text-blue-400 font-bold text-xl mr-3">3.</span>
              <p>Perform one of the supported ASL signs</p>
            </div>
            <div className="flex items-start">
              <span className="text-blue-400 font-bold text-xl mr-3">4.</span>
              <p>The system will detect and display the sign in real-time</p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="bg-gray-800 rounded-2xl shadow-2xl p-8 max-w-2xl w-full mb-8"
        >
          <h2 className="text-2xl font-semibold mb-6 text-purple-400">Supported Signs</h2>
          <div className="grid grid-cols-2 gap-4">
            {[
              { sign: "Hello", emoji: "👋", color: "blue" },
              { sign: "Thanks", emoji: "🙏", color: "green" },
              { sign: "Yes", emoji: "✅", color: "purple" },
              { sign: "No", emoji: "❌", color: "red" }
            ].map((item, idx) => (
              <motion.div
                key={idx}
                whileHover={{ scale: 1.05 }}
                className={`bg-gray-700 rounded-xl p-4 text-center border-2 border-${item.color}-500`}
              >
                <div className="text-4xl mb-2">{item.emoji}</div>
                <div className="text-lg font-semibold">{item.sign}</div>
              </motion.div>
            ))}
          </div>
        </motion.div>

        <motion.button
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6 }}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setCurrentPage("interpreter")}
          className="bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 text-white font-bold text-xl px-12 py-4 rounded-full shadow-lg transition-all duration-300"
        >
          Start Interpreter
        </motion.button>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white p-4">
      <button
        onClick={() => setCurrentPage("home")}
        className="absolute top-6 left-6 bg-gray-800 hover:bg-gray-700 text-white px-6 py-2 rounded-lg transition-colors duration-300"
      >
        ← Back to Home
      </button>

      <h1 className="text-4xl font-bold mb-8">Sign Language Interpreter</h1>
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        className="rounded-lg shadow-lg border-4 border-blue-500 w-full max-w-[640px] h-auto"
      />
      <motion.div
        className="mt-6 p-4 bg-gray-800 rounded-xl shadow-xl text-center w-full max-w-[640px]"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h2 className="text-3xl font-semibold">{prediction}</h2>
        {confidence && <p className="text-gray-400 mt-2">Confidence: {confidence}%</p>}
        {error && <p className="text-red-400 mt-2 text-sm">{error}</p>}
      </motion.div>
    </div>
  );
}

export default App;