import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Dashboard from "./pages/Dashboard.jsx";
import DashboardLayout from "./layouts/DashboardLayout.jsx";
import NewAnalysis from "./pages/NewAnalysis.jsx";
import AnalysisHistory from "./pages/AnalysisHistory.jsx";
import Login from "./pages/Login.jsx";
import { getToken } from "./service/api.js";

function PrivateRoute({ children }) {
    return getToken() ? (
        <DashboardLayout>{children}</DashboardLayout>
    ) : (
        <Navigate to="/login" replace />
    );
}

export default function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/login" element={<Login />} />
                
                <Route
                    path="/"
                    element={
                        <PrivateRoute>
                            <Dashboard />
                        </PrivateRoute>
                    }
                />
                <Route
                    path="/new-analysis"
                    element={
                        <PrivateRoute>
                            <NewAnalysis />
                        </PrivateRoute>
                    }
                />
                <Route
                    path="/history"
                    element={
                        <PrivateRoute>
                            <AnalysisHistory />
                        </PrivateRoute>
                    }
                />
            </Routes>
        </BrowserRouter>
    );
}