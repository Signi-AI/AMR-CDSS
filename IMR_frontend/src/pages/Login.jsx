import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../service/api";
import { Eye, EyeOff, LayoutGrid } from "lucide-react";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
      e.preventDefault();
      setLoading(true);
      setError("");

      try {
          await login(email, password);
          navigate("/");
      } catch (err) {
          // Auto-register fallback for presentation purposes
          // This allows the presenter to use any "doctor@" email seamlessly
          if (email.startsWith("doctor")) {
              try {
                  await fetch("http://localhost:8000/auth/register", {
                      method: "POST",
                      headers: { "Content-Type": "application/json" },
                      body: JSON.stringify({
                          full_name: "Dr. Smith",
                          email,
                          password,
                          role: "doctor"
                      })
                  });
                  
                  await login(email, password);
                  navigate("/");
              } catch (registerErr) {
                  setError("Failed to authenticate.");
              }
          } else {
              setError("Invalid credentials or server error");
          }
      } finally {
          setLoading(false);
      }
  };

  return (
    <div className="min-h-screen w-full flex items-center justify-center p-6 bg-gradient-to-br from-teal-100 via-teal-50/50 to-slate-50">
      <style>{`
        @keyframes gentle-float {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-10px); }
        }
        .float-anim { animation: gentle-float 4.5s ease-in-out infinite; }

        @keyframes orb-drift-1 {
          0%, 100% { transform: translate(0, 0); }
          50% { transform: translate(12px, -18px); }
        }
        @keyframes orb-drift-2 {
          0%, 100% { transform: translate(0, 0); }
          50% { transform: translate(-10px, 14px); }
        }
        @keyframes orb-drift-3 {
          0%, 100% { transform: translate(0, 0); }
          50% { transform: translate(8px, 10px); }
        }
        .orb-1 { animation: orb-drift-1 7s ease-in-out infinite; }
        .orb-2 { animation: orb-drift-2 9s ease-in-out infinite; }
        .orb-3 { animation: orb-drift-3 6s ease-in-out infinite; }

        .pulse-line {
          stroke-dasharray: 300;
          stroke-dashoffset: 300;
          animation: draw-pulse 2.5s ease-in-out infinite;
        }
        @keyframes draw-pulse {
          0% { stroke-dashoffset: 300; }
          50% { stroke-dashoffset: 0; }
          100% { stroke-dashoffset: -300; }
        }

        @media (prefers-reduced-motion: reduce) {
          .float-anim, .orb-1, .orb-2, .orb-3, .pulse-line { animation: none; }
        }
      `}</style>

      <div className="w-full max-w-4xl bg-white rounded-3xl shadow-2xl flex flex-col md:flex-row overflow-hidden">
        {/* Left: gradient panel with the 3D piece */}
        <div className="hidden md:flex md:w-5/12 md:flex-col justify-between p-10 bg-gradient-to-b from-teal-500 to-teal-700">
          <div>
            <div className="w-10 h-10 rounded-full bg-white/15 flex items-center justify-center mb-8">
              <LayoutGrid className="w-5 h-5 text-white" />
            </div>
            <h2 className="text-white text-xl font-semibold mb-2">Welcome back</h2>
            <p className="text-teal-100 text-sm leading-relaxed max-w-48">
              Sign in to pick up right where you left off in AMR-CDSS.
            </p>
          </div>

          <div className="flex-1 flex items-center justify-center mt-8 relative">
            {/* Floating orbs background */}
            <div className="absolute inset-0 overflow-hidden">
              <div className="absolute w-20 h-20 rounded-full bg-white/10 blur-xl top-4 left-4 orb-1" />
              <div className="absolute w-14 h-14 rounded-full bg-teal-300/15 blur-lg bottom-16 right-6 orb-2" />
              <div className="absolute w-10 h-10 rounded-full bg-white/10 blur-md top-1/2 right-2 orb-3" />
            </div>

            {/* Center piece — Medical AI Shield */}
            <div className="relative float-anim">
              <svg viewBox="0 0 200 220" className="w-48 h-52" style={{ filter: "drop-shadow(0 12px 32px rgba(0,0,0,0.3))" }}>
                <defs>
                  <linearGradient id="shieldFill" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="rgba(255,255,255,0.2)" />
                    <stop offset="100%" stopColor="rgba(255,255,255,0.05)" />
                  </linearGradient>
                  <linearGradient id="shieldStroke" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="rgba(255,255,255,0.6)" />
                    <stop offset="100%" stopColor="rgba(255,255,255,0.1)" />
                  </linearGradient>
                  <radialGradient id="coreGlow" cx="50%" cy="45%" r="35%">
                    <stop offset="0%" stopColor="#5eead4" />
                    <stop offset="60%" stopColor="#14b8a6" />
                    <stop offset="100%" stopColor="transparent" />
                  </radialGradient>
                </defs>

                {/* Shield shape */}
                <path
                  d="M100 16 L170 50 L170 120 Q170 175 100 204 Q30 175 30 120 L30 50 Z"
                  fill="url(#shieldFill)"
                  stroke="url(#shieldStroke)"
                  strokeWidth="1.5"
                />

                {/* Inner glow */}
                <circle cx="100" cy="105" r="50" fill="url(#coreGlow)" opacity="0.3" />

                {/* Medical Cross */}
                <rect x="88" y="72" width="24" height="66" rx="5" fill="white" opacity="0.9" />
                <rect x="67" y="93" width="66" height="24" rx="5" fill="white" opacity="0.9" />

                {/* Heartbeat / pulse line across the cross */}
                <polyline
                  points="55,105 78,105 84,85 92,125 100,95 108,115 114,105 145,105"
                  fill="none"
                  stroke="#0d9488"
                  strokeWidth="3"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  className="pulse-line"
                />

                {/* Orbiting dots */}
                <circle cx="100" cy="105" r="68" fill="none" stroke="rgba(255,255,255,0.08)" strokeWidth="1" strokeDasharray="4 8" />
                <circle r="4" fill="#5eead4" className="orbit-dot">
                  <animateMotion dur="6s" repeatCount="indefinite" path="M100,37 A68,68 0 1 1 99.99,37" />
                </circle>
                <circle r="3" fill="rgba(255,255,255,0.5)" className="orbit-dot-2">
                  <animateMotion dur="8s" repeatCount="indefinite" path="M100,37 A68,68 0 1 0 99.99,37" />
                </circle>
              </svg>

              {/* Soft glow beneath the shield */}
              <div className="absolute -bottom-4 left-1/2 -translate-x-1/2 w-32 h-4 rounded-full bg-teal-300/25 blur-xl" />
            </div>
          </div>
        </div>

        {/* Right: the form */}
        <div className="w-full md:w-7/12 flex flex-col justify-center px-8 py-12 sm:px-14">
          <h1 className="text-2xl font-bold text-slate-800 mb-1">Sign in</h1>
          <p className="text-slate-400 text-sm mb-8">Enter your details to continue.</p>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="identifier" className="block text-sm text-slate-500 mb-1">
                Email Address
              </label>
              <input
                id="identifier"
                type="email"
                required
                autoComplete="username"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="doctor@hospital.com"
                className="w-full border-b border-slate-300 focus:border-teal-500 outline-none py-2 text-slate-700 placeholder:text-slate-300 bg-transparent transition-colors"
              />
            </div>

            <div>
              <div className="flex items-center justify-between mb-1">
                <label htmlFor="password" className="text-sm text-slate-500">
                  Password
                </label>
                <button
                  type="button"
                  className="text-xs text-teal-500 hover:text-teal-600 focus:outline-none focus:ring-2 focus:ring-teal-400 rounded"
                >
                  Forgot password?
                </button>
              </div>
              <div className="relative">
                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  required
                  autoComplete="current-password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full border-b border-slate-300 focus:border-teal-500 outline-none py-2 pr-8 text-slate-700 placeholder:text-slate-300 bg-transparent transition-colors"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword((s) => !s)}
                  aria-label={showPassword ? "Hide password" : "Show password"}
                  className="absolute right-0 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 focus:outline-none focus:ring-2 focus:ring-teal-400 rounded"
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            {error && (
                <div className="rounded-lg bg-red-50 p-3 text-sm font-medium text-red-600">
                    {error}
                </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-teal-500 to-teal-700 hover:opacity-90 text-white font-medium py-3 rounded-full transition-opacity focus:outline-none focus:ring-2 focus:ring-teal-400 focus:ring-offset-2 disabled:opacity-50"
            >
              {loading ? "Signing in..." : "Sign in"}
            </button>
          </form>

        </div>
      </div>
    </div>
  );
}
