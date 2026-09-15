const API_BASE = "http://localhost:8000";

let token = localStorage.getItem("amr_token");

export function getToken() {
    return localStorage.getItem("amr_token");
}

export function setToken(newToken) {
    if (newToken) {
        localStorage.setItem("amr_token", newToken);
        token = newToken;
    } else {
        localStorage.removeItem("amr_token");
        token = null;
    }
}

export function getUserName() {
    return localStorage.getItem("amr_user_name") || "Doctor";
}

export function setUserName(name) {
    if (name) {
        localStorage.setItem("amr_user_name", name);
    } else {
        localStorage.removeItem("amr_user_name");
    }
}

export function logout() {
    setToken(null);
    setUserName(null);
    window.location.href = "/login";
}

export async function login(username, password) {
    let formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);

    const res = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        body: formData,
    });

    if (!res.ok) {
        throw new Error(await res.text());
    }

    const data = await res.json();
    setToken(data.access_token);

    // Fetch the user's profile to store their name
    try {
        const meRes = await fetch(`${API_BASE}/auth/me`, {
            headers: { "Authorization": `Bearer ${data.access_token}` }
        });
        if (meRes.ok) {
            const user = await meRes.json();
            setUserName(user.full_name);
        }
    } catch (e) {
        // Non-critical — name will fallback to "Doctor"
    }

    return data;
}

export async function ensureAuth() {
    if (token) return token;
    throw new Error("Not authenticated");
}

/**
 * Fetch available antimicrobials for the select dropdown.
 */
export async function getMedicines() {
    await ensureAuth();
    const res = await fetch(`${API_BASE}/antimicrobials/`, {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });
    if (!res.ok) {
        console.error("Failed to fetch medicines");
        return [];
    }
    return res.json();
}

/**
 * Read all analyses (mocked for now, or you could fetch from backend)
 */
export function getAnalyses() {
    try {
        const raw = localStorage.getItem("amr_analyses");
        return raw ? JSON.parse(raw) : [];
    } catch (error) {
        return [];
    }
}

/**
 * Save a new analysis by running the full workflow on the backend.
 */
export async function saveAnalysis(data) {
    await ensureAuth();

    const formData = new FormData();
    formData.append("patientId", data.patientId);
    formData.append("age", data.age);
    formData.append("sex", data.sex);
    formData.append("disease", data.disease);
    formData.append("medicine_id", data.medicine_id);
    formData.append("file", data.image);

    const res = await fetch(`${API_BASE}/workflow/analyze`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${token}`
        },
        body: formData,
    });

    if (!res.ok) {
        throw new Error(await res.text());
    }

    const backendResult = await res.json();
    
    // Save to local history for the frontend demo
    const analyses = getAnalyses();
    const record = {
        id: `AMR-${String(backendResult.visit_id).padStart(3, "0")}`,
        patientId: data.patientId,
        disease: data.disease,
        medicine: data.medicine_name,
        imageName: data.image.name,
        results: backendResult.recommendation,
        createdAt: new Date().toISOString(),
    };

    analyses.unshift(record);
    localStorage.setItem("amr_analyses", JSON.stringify(analyses));

    return backendResult;
}

export function deleteAnalysis(id) {
    const analyses = getAnalyses().filter((item) => item.id !== id);
    localStorage.setItem("amr_analyses", JSON.stringify(analyses));
}

export function clearAnalyses() {
    localStorage.removeItem("amr_analyses");
}