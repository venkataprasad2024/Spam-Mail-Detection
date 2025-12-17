import { useState } from "react";
import axios from "axios";

/**
 * IMPORTANT:
 * Backend deployed on Render
 * https://spam-mail-detection-7w08.onrender.com
 */
const API_URL = "https://spam-mail-detection-7w08.onrender.com";

export default function SpamChecker() {
  const [email, setEmail] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isDark, setIsDark] = useState(true);

  const toggleDarkMode = () => {
    setIsDark(!isDark);
    document.documentElement.classList.toggle("dark", !isDark);
  };

  const checkSpam = async () => {
    if (!email.trim()) {
      alert("Paste an email first");
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const res = await axios.post(`${API_URL}/predict`, {
        email,
      });
      setResult(res.data);
    } catch (err) {
      console.error(err);
      alert("Backend connection error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className={`min-h-screen transition-colors duration-500 ${
        isDark
          ? "bg-gradient-to-br from-[#0f0f1a] via-[#111827] to-[#020617] text-white"
          : "bg-gradient-to-br from-[#f8fafc] via-[#eef2ff] to-[#fdf4ff] text-gray-900"
      }`}
    >
      {/* ===== Header ===== */}
      <header className="flex justify-between items-center px-8 py-6 max-w-6xl mx-auto">
        <h1 className="text-2xl font-bold tracking-tight">
          🛡️ SpamGuard AI
        </h1>

        <button
          onClick={toggleDarkMode}
          className={`px-5 py-2 rounded-full font-medium transition ${
            isDark
              ? "bg-white/10 hover:bg-white/20"
              : "bg-black/10 hover:bg-black/20"
          }`}
        >
          {isDark ? "☀ Light" : "🌙 Dark"}
        </button>
      </header>

      {/* ===== Main ===== */}
      <main className="flex items-center justify-center px-6 py-10">
        <div
          className={`w-full max-w-5xl rounded-3xl p-10 grid md:grid-cols-2 gap-10 shadow-2xl backdrop-blur-xl ${
            isDark
              ? "bg-white/5 border border-white/10"
              : "bg-white/70 border border-gray-200"
          }`}
        >
          {/* ===== Input ===== */}
          <div>
            <h2 className="text-3xl font-extrabold mb-2">
              Check your email
            </h2>
            <p className="text-gray-400 mb-6">
              Paste an email and our AI will instantly detect spam.
            </p>

            <textarea
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              rows={10}
              placeholder="Paste email content here..."
              className={`w-full p-5 rounded-2xl text-lg outline-none resize-none transition ${
                isDark
                  ? "bg-black/40 border border-white/20 text-white placeholder-gray-400 focus:ring-2 focus:ring-indigo-500"
                  : "bg-white border border-gray-300 text-gray-900 placeholder-gray-500 focus:ring-2 focus:ring-indigo-500"
              }`}
            />

            <button
              onClick={checkSpam}
              disabled={loading}
              className="mt-6 w-full py-4 rounded-2xl text-lg font-bold bg-gradient-to-r from-indigo-500 to-purple-500 text-white hover:scale-[1.02] transition disabled:opacity-60 shadow-lg"
            >
              {loading ? "Analyzing..." : "Detect Spam"}
            </button>
          </div>

          {/* ===== Result ===== */}
          <div className="flex items-center justify-center">
            {result ? (
              <div
                className={`w-full max-w-sm rounded-3xl p-8 text-center shadow-xl ${
                  result.is_spam
                    ? "bg-gradient-to-br from-red-500/80 to-pink-600/80"
                    : "bg-gradient-to-br from-emerald-500/80 to-teal-600/80"
                } text-white`}
              >
                <div className="text-7xl mb-4">
                  {result.is_spam ? "🚨" : "✅"}
                </div>
                <h3 className="text-3xl font-bold mb-2">
                  {result.is_spam ? "Spam Detected" : "Safe Email"}
                </h3>
                <p className="text-xl opacity-90">Confidence</p>
                <p className="text-4xl font-extrabold mt-1">
                  {result.confidence}
                </p>
              </div>
            ) : (
              <div
                className={`w-full max-w-sm rounded-3xl p-8 text-center ${
                  isDark
                    ? "bg-white/5 border border-white/10 text-gray-400"
                    : "bg-white border border-gray-300 text-gray-500"
                }`}
              >
                <p className="text-xl">Result will appear here</p>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* ===== Footer ===== */}
      <footer className="text-center text-sm text-gray-400 py-6">
        Built with React • Flask • Machine Learning
      </footer>
    </div>
  );
}
